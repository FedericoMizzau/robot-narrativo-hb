#!/usr/bin/env python3
"""
Script para probar el generador ML con diferentes prompts
"""

from generador_ml import GeneradorML
import time

def probar_generacion():
    print("=" * 60)
    print("🧪 PRUEBA DEL GENERADOR ML CON GPT-2")
    print("=" * 60)
    
    # Crear generador
    print("\n📥 Inicializando generador...")
    gen = GeneradorML(modelo="gpt2", usar_gpu=False)
    
    if not gen.esta_disponible():
        print("❌ El modelo no está disponible")
        return
    
    # Prompts de prueba
    prompts = [
        "Un cuento sobre un robot que descubre la creatividad",
        "Una aventura en un bosque mágico",
        "Un misterio en una biblioteca antigua"
    ]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n{'='*60}")
        print(f"📝 Prueba {i}: {prompt}")
        print("=" * 60)
        
        inicio = time.time()
        try:
            cuento = gen.generar_cuento(prompt, max_length=250, temperature=0.85)
            tiempo = time.time() - inicio
            
            print(f"\n⏱️  Tiempo de generación: {tiempo:.2f} segundos")
            print(f"\n📖 Cuento generado ({len(cuento)} caracteres):")
            print("-" * 60)
            print(cuento)
            print("-" * 60)
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")
    print("=" * 60)

if __name__ == "__main__":
    probar_generacion()


