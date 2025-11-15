"""
Script completo para fine-tuning de GPT-2 con dataset de cuentos reales.
Mejorado y optimizado para uso práctico.
"""

import torch
import os
from pathlib import Path
from transformers import (
    GPT2LMHeadModel, 
    GPT2Tokenizer, 
    Trainer, 
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from transformers import TextDataset
import warnings
warnings.filterwarnings('ignore')


def fine_tune_modelo(
    ruta_dataset: str,
    modelo_base: str = "gpt2",
    output_dir: str = "./modelo_cuentos",
    num_epochs: int = 3,
    batch_size: int = 4,
    usar_gpu: bool = None
):
    """
    Hace fine-tuning de GPT-2 con un dataset de cuentos.
    
    Args:
        ruta_dataset: Ruta al archivo de texto con cuentos procesados
        modelo_base: Modelo base a usar ("gpt2" o "distilgpt2")
        output_dir: Directorio donde guardar el modelo entrenado
        num_epochs: Número de épocas de entrenamiento
        batch_size: Tamaño del batch (reducir si hay problemas de memoria)
        usar_gpu: Si True usa GPU, si False usa CPU, si None detecta automáticamente
    """
    
    # Detectar GPU
    if usar_gpu is None:
        usar_gpu = torch.cuda.is_available()
    
    device = "cuda" if usar_gpu else "cpu"
    print(f"Usando dispositivo: {device.upper()}")
    
    if usar_gpu:
        print(f"   GPU: {torch.cuda.get_device_name(0)}")
        print(f"   Memoria disponible: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    else:
        print("   [INFO] Usando CPU (sera mas lento)")
    
    # Verificar que el dataset existe
    if not os.path.exists(ruta_dataset):
        raise FileNotFoundError(f"No se encontró el dataset: {ruta_dataset}")
    
    # Verificar tamaño del dataset
    tamaño = os.path.getsize(ruta_dataset) / 1024  # KB
    print(f"\nDataset: {ruta_dataset}")
    print(f"   Tamaño: {tamaño:.2f} KB")
    
    if tamaño < 10:
        print("[ADVERTENCIA] Dataset muy pequeño. Se recomienda al menos 50-100 cuentos.")
    
    print(f"\nCargando modelo base: {modelo_base}...")
    tokenizer = GPT2Tokenizer.from_pretrained(modelo_base)
    model = GPT2LMHeadModel.from_pretrained(modelo_base)
    
    # Configurar tokenizer
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Mover modelo a dispositivo
    model = model.to(device)
    
    print("Preparando dataset...")
    try:
        # Crear dataset
        train_dataset = TextDataset(
            tokenizer=tokenizer,
            file_path=ruta_dataset,
            block_size=128  # Tamaño del bloque de texto
        )
        
        print(f"   [OK] Dataset cargado: {len(train_dataset)} bloques de texto")
        
    except Exception as e:
        print(f"❌ Error al cargar dataset: {e}")
        print("\n💡 Asegúrate de que el archivo tenga el formato correcto:")
        print("   - Cuentos separados por líneas vacías (\\n\\n)")
        print("   - Cada cuento debe ser texto completo")
        raise
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False  # No usar masked language modeling
    )
    
    print("\nConfigurando entrenamiento...")
    # Configurar entrenamiento
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        save_steps=500,
        save_total_limit=2,
        logging_steps=50,
        prediction_loss_only=True,
        remove_unused_columns=False,
        fp16=usar_gpu,  # Usar precisión mixta si hay GPU
        dataloader_num_workers=0 if not usar_gpu else 2,
        report_to="none",  # No reportar a wandb/tensorboard
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
    )
    
    print("\nIniciando fine-tuning...")
    print("   Esto puede tardar varios minutos u horas dependiendo del hardware...")
    print("   Presiona Ctrl+C para cancelar (el modelo se guardara en el ultimo checkpoint)\n")
    
    try:
        # Entrenar
        trainer.train()
        
        # Guardar modelo final
        print(f"\nGuardando modelo en {output_dir}...")
        trainer.save_model()
        tokenizer.save_pretrained(output_dir)
        
        print("\n" + "=" * 60)
        print("[OK] FINE-TUNING COMPLETADO!")
        print("=" * 60)
        print(f"\nModelo guardado en: {output_dir}")
        print(f"\nPara usar el modelo entrenado:")
        print(f"   1. En app.py, cambia modelo_ml a: '{output_dir}'")
        print(f"   2. O en generador_ml.py, usa: GeneradorML(modelo='{output_dir}')")
        
        return output_dir
        
    except KeyboardInterrupt:
        print("\n\n[INFO] Entrenamiento interrumpido por el usuario")
        print("Guardando checkpoint actual...")
        trainer.save_model()
        tokenizer.save_pretrained(output_dir)
        print(f"[OK] Checkpoint guardado en: {output_dir}")
        return output_dir
    except Exception as e:
        print(f"\n❌ Error durante el entrenamiento: {e}")
        raise


def main():
    """
    Función principal con interfaz de línea de comandos.
    """
    import sys
    
    import sys
    import io
    # Configurar encoding para Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 60)
    print("FINE-TUNING DE GPT-2 CON CUENTOS")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\n📖 Uso:")
        print("  python fine_tuning.py <ruta_dataset> [opciones]")
        print("\n📝 Ejemplos:")
        print("  python fine_tuning.py data/cuentos_procesados.txt")
        print("  python fine_tuning.py data/cuentos_procesados.txt --epochs 5 --batch 2")
        print("\n⚙️  Opciones:")
        print("  --epochs N        Número de épocas (default: 3)")
        print("  --batch N         Tamaño del batch (default: 4)")
        print("  --output DIR      Directorio de salida (default: ./modelo_cuentos)")
        print("  --model MODELO    Modelo base (default: gpt2)")
        print("  --cpu             Forzar uso de CPU")
        print("\n💡 Primero procesa tu dataset con:")
        print("  python procesar_dataset.py <tu_dataset>")
        return
    
    ruta_dataset = sys.argv[1]
    
    # Parsear argumentos
    num_epochs = 3
    batch_size = 4
    output_dir = "./modelo_cuentos"
    modelo_base = "gpt2"
    usar_gpu = None
    
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--epochs" and i + 1 < len(sys.argv):
            num_epochs = int(sys.argv[i + 1])
            i += 2
        elif arg == "--batch" and i + 1 < len(sys.argv):
            batch_size = int(sys.argv[i + 1])
            i += 2
        elif arg == "--output" and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
            i += 2
        elif arg == "--model" and i + 1 < len(sys.argv):
            modelo_base = sys.argv[i + 1]
            i += 2
        elif arg == "--cpu":
            usar_gpu = False
            i += 1
        else:
            i += 1
    
    # Ejecutar fine-tuning
    try:
        fine_tune_modelo(
            ruta_dataset=ruta_dataset,
            modelo_base=modelo_base,
            output_dir=output_dir,
            num_epochs=num_epochs,
            batch_size=batch_size,
            usar_gpu=usar_gpu
        )
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


