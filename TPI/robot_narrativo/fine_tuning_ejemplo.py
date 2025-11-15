"""
Ejemplo de script para fine-tuning de GPT-2 con cuentos en español.
NOTA: Esto requiere GPU para ser práctico, o mucho tiempo en CPU.
"""

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from transformers import TextDataset, DataCollatorForLanguageModeling
import os


def preparar_dataset(ruta_archivo: str):
    """
    Prepara el dataset de cuentos para entrenamiento.
    
    Formato esperado: Un cuento por línea, o archivo de texto con cuentos separados.
    """
    # Leer cuentos
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        cuentos = f.read()
    
    # Dividir en ejemplos (cada cuento debe estar separado)
    # Ajustar según tu formato de datos
    ejemplos = cuentos.split('\n\n')  # Si están separados por líneas vacías
    
    return ejemplos


def fine_tune_modelo(ruta_dataset: str, modelo_base: str = "gpt2", 
                     output_dir: str = "./modelo_fine_tuned"):
    """
    Hace fine-tuning de GPT-2 con el dataset de cuentos.
    
    Args:
        ruta_dataset: Ruta al archivo con cuentos
        modelo_base: Modelo base a usar
        output_dir: Directorio donde guardar el modelo entrenado
    """
    
    print("📥 Cargando modelo base...")
    tokenizer = GPT2Tokenizer.from_pretrained(modelo_base)
    model = GPT2LMHeadModel.from_pretrained(modelo_base)
    
    # Configurar tokenizer
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    print("📚 Preparando dataset...")
    # Preparar dataset
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=ruta_dataset,
        block_size=128
    )
    
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    print("🚀 Iniciando entrenamiento...")
    # Configurar entrenamiento
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=3,  # Ajustar según necesites
        per_device_train_batch_size=4,  # Reducir si no tienes GPU
        save_steps=500,
        save_total_limit=2,
        prediction_loss_only=True,
        remove_unused_columns=False,
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
    )
    
    # Entrenar
    trainer.train()
    
    # Guardar modelo
    print(f"💾 Guardando modelo en {output_dir}...")
    trainer.save_model()
    tokenizer.save_pretrained(output_dir)
    
    print("✅ Fine-tuning completado!")
    return output_dir


if __name__ == "__main__":
    print("""
    ⚠️  ADVERTENCIA: Fine-tuning requiere:
    
    1. Dataset de cuentos en español (50-200 cuentos mínimo)
    2. GPU recomendada (o mucho tiempo en CPU)
    3. Al menos 2-3 horas de tiempo
    
    Para usar este script:
    
    1. Prepara un archivo de texto con cuentos (uno por línea o separados)
    2. Ejecuta:
       python fine_tuning_ejemplo.py
    
    3. El modelo entrenado se guardará en ./modelo_fine_tuned
    
    Ejemplo de formato de dataset:
    Érase una vez un héroe que...
    
    Hace mucho tiempo, en un lugar lejano...
    
    (Cada cuento separado por línea vacía)
    """)
    
    # Descomentar para usar:
    # fine_tune_modelo("cuentos.txt", output_dir="./modelo_cuentos")

