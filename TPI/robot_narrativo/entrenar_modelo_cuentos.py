"""
Script optimizado para entrenar el modelo con los cuentos procesados.
Incluye opciones para diferentes configuraciones según hardware disponible.
"""

import os
import sys
import io
from pathlib import Path

def main():
    # Configurar encoding para Windows
    if sys.platform == 'win32':
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except:
            pass
    
    print("=" * 60)
    print("ENTRENAMIENTO DEL MODELO CON CUENTOS REALES")
    print("=" * 60)
    
    # Ruta al dataset procesado
    base_dir = Path(__file__).parent
    dataset_path = base_dir / "data" / "cuentos_procesados.txt"
    
    if not dataset_path.exists():
        print(f"[ERROR] No se encontro el dataset: {dataset_path}")
        print("   Ejecuta primero: python procesar_datasets_existentes.py")
        return
    
    print(f"\nDataset encontrado:")
    print(f"   Archivo: {dataset_path}")
    tamaño = dataset_path.stat().st_size / (1024 * 1024)  # MB
    print(f"   Tamaño: {tamaño:.2f} MB")
    
    # Leer estadísticas del dataset
    with open(dataset_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
        cuentos = contenido.split('\n\n')
        cuentos = [c for c in cuentos if c.strip()]
        total_palabras = sum(len(c.split()) for c in cuentos)
    
    print(f"   Cuentos: {len(cuentos)}")
    print(f"   Palabras totales: {total_palabras:,}")
    print(f"   Promedio: {total_palabras // len(cuentos) if cuentos else 0} palabras/cuento")
    
    # Detectar hardware
    import torch
    tiene_gpu = torch.cuda.is_available()
    
    print(f"\nHardware detectado:")
    if tiene_gpu:
        print(f"   [OK] GPU disponible: {torch.cuda.get_device_name(0)}")
        print(f"   Memoria: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        batch_size = 4
        num_epochs = 3
        usar_gpu = True
    else:
        print(f"   [INFO] Solo CPU disponible (sera mas lento)")
        batch_size = 2  # Más pequeño para CPU
        num_epochs = 2  # Menos épocas para CPU
        usar_gpu = False
    
    # Configuración recomendada
    print(f"\nConfiguracion recomendada:")
    print(f"   Epocas: {num_epochs}")
    print(f"   Batch size: {batch_size}")
    print(f"   Dispositivo: {'GPU' if usar_gpu else 'CPU'}")
    
    # Estimar tiempo
    if usar_gpu:
        tiempo_estimado = len(cuentos) * num_epochs * 0.5 / 60  # minutos aproximados
        print(f"   Tiempo estimado: {tiempo_estimado:.1f} minutos")
    else:
        tiempo_estimado = len(cuentos) * num_epochs * 2 / 60  # minutos aproximados
        print(f"   Tiempo estimado: {tiempo_estimado:.1f} minutos ({tiempo_estimado/60:.1f} horas)")
    
    # Confirmar (auto-continuar si se ejecuta desde script)
    print(f"\nIniciando entrenamiento automaticamente...")
    print(f"   (Para cancelar, presiona Ctrl+C)")
    
    # Importar y ejecutar fine-tuning
    from fine_tuning import fine_tune_modelo
    
    output_dir = base_dir / "modelo_cuentos_entrenado"
    
    print(f"\nIniciando entrenamiento...")
    print("=" * 60)
    
    try:
        fine_tune_modelo(
            ruta_dataset=str(dataset_path),
            modelo_base="gpt2",
            output_dir=str(output_dir),
            num_epochs=num_epochs,
            batch_size=batch_size,
            usar_gpu=usar_gpu
        )
        
        print("\n" + "=" * 60)
        print("[OK] ENTRENAMIENTO COMPLETADO")
        print("=" * 60)
        print(f"\nModelo guardado en: {output_dir}")
        print(f"\nPara usar el modelo entrenado:")
        print(f"   1. En app.py, cambia:")
        print(f"      modelo_ml='{output_dir}'")
        print(f"\n   2. O reinicia el servidor:")
        print(f"      python app.py")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n[INFO] Entrenamiento interrumpido")
        print(f"El modelo parcial se guardo en: {output_dir}")
    except Exception as e:
        print(f"\n[ERROR] Error durante el entrenamiento: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

