"""
Script para verificar si el modelo fue entrenado correctamente.
"""

import os
from pathlib import Path

def verificar_modelo_entrenado():
    """Verifica si el modelo fue entrenado y está listo para usar."""
    
    print("=" * 60)
    print("🔍 VERIFICACIÓN DEL MODELO ENTRENADO")
    print("=" * 60)
    
    base_dir = Path(__file__).parent
    modelo_dir = base_dir / "modelo_cuentos_entrenado"
    
    if not modelo_dir.exists():
        print("\n❌ El modelo NO ha sido entrenado aún")
        print(f"   Directorio no encontrado: {modelo_dir}")
        print("\n💡 Para entrenar el modelo:")
        print("   python entrenar_modelo_cuentos.py")
        return False
    
    print(f"\n📁 Directorio encontrado: {modelo_dir}")
    
    # Buscar archivos del modelo
    archivos_requeridos = [
        "config.json",
        "tokenizer_config.json",
        "vocab.json",
        "merges.txt"
    ]
    
    archivos_modelo = [
        "pytorch_model.bin",
        "model.safetensors"
    ]
    
    print("\n📋 Verificando archivos del modelo...")
    
    archivos_encontrados = []
    archivos_faltantes = []
    
    for archivo in archivos_requeridos:
        ruta = modelo_dir / archivo
        if ruta.exists():
            tamaño = ruta.stat().st_size / 1024  # KB
            print(f"   ✅ {archivo} ({tamaño:.2f} KB)")
            archivos_encontrados.append(archivo)
        else:
            print(f"   ❌ {archivo} - NO ENCONTRADO")
            archivos_faltantes.append(archivo)
    
    # Buscar archivo del modelo
    modelo_encontrado = False
    for archivo in archivos_modelo:
        ruta = modelo_dir / archivo
        if ruta.exists():
            tamaño = ruta.stat().st_size / (1024 * 1024)  # MB
            print(f"   ✅ {archivo} ({tamaño:.2f} MB)")
            modelo_encontrado = True
            break
    
    if not modelo_encontrado:
        print("   ❌ Archivo del modelo - NO ENCONTRADO")
        print("      (pytorch_model.bin o model.safetensors)")
    
    # Buscar checkpoints
    checkpoints = list(modelo_dir.glob("checkpoint-*"))
    if checkpoints:
        print(f"\n📊 Checkpoints encontrados: {len(checkpoints)}")
        for ckpt in sorted(checkpoints)[-3:]:  # Mostrar últimos 3
            tamaño = sum(f.stat().st_size for f in ckpt.rglob('*') if f.is_file()) / (1024*1024)
            print(f"   - {ckpt.name} ({tamaño:.2f} MB)")
    
    # Calcular tamaño total
    tamaño_total = sum(f.stat().st_size for f in modelo_dir.rglob('*') if f.is_file()) / (1024*1024)
    print(f"\n💾 Tamaño total del modelo: {tamaño_total:.2f} MB")
    
    # Verificar si está completo
    print("\n" + "=" * 60)
    if modelo_encontrado and len(archivos_encontrados) >= 3:
        print("✅ MODELO ENTRENADO Y LISTO PARA USAR")
        print("=" * 60)
        print(f"\n🚀 Para usar el modelo:")
        print(f"   1. En app.py, cambia:")
        print(f"      modelo_ml='./modelo_cuentos_entrenado'")
        print(f"\n   2. Reinicia el servidor:")
        print(f"      python app.py")
        return True
    elif checkpoints:
        print("⚠️  ENTRENAMIENTO EN PROGRESO O INCOMPLETO")
        print("=" * 60)
        print(f"\n   Se encontraron checkpoints pero el modelo final no está completo.")
        print(f"   El entrenamiento puede estar en progreso o se interrumpió.")
        print(f"\n   Puedes:")
        print(f"   1. Esperar a que termine el entrenamiento")
        print(f"   2. O usar el último checkpoint si está suficientemente entrenado")
        return False
    else:
        print("❌ MODELO NO COMPLETO")
        print("=" * 60)
        print(f"\n   El directorio existe pero no tiene los archivos necesarios.")
        print(f"   El entrenamiento puede no haber comenzado o se interrumpió temprano.")
        return False

if __name__ == "__main__":
    verificar_modelo_entrenado()

