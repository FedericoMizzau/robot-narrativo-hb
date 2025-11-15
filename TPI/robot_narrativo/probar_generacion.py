"""
Script para probar la generación de cuentos con el modelo entrenado.
Verifica que genera cuentos diferentes cada vez.
"""

import sys
import io

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from generador_cuento import GeneradorCuento

print("=" * 60)
print("PRUEBA DE GENERACION DE CUENTOS")
print("=" * 60)

# Inicializar generador con modelo entrenado
print("\nCargando generador con modelo entrenado...")
generador = GeneradorCuento(
    usar_ml=True,
    modelo_ml="./modelo_cuentos_entrenado"
)

if not generador.usar_ml or not generador.generador_ml:
    print("[ADVERTENCIA] Modelo ML no disponible, usando plantillas")
else:
    print("[OK] Modelo ML cargado correctamente")

# Probar con diferentes prompts
prompts = [
    "un robot creativo",
    "una aventura en el espacio",
    "un misterio en el bosque",
    "un cuento sobre amistad"
]

print("\n" + "=" * 60)
print("GENERANDO CUENTOS DE PRUEBA")
print("=" * 60)

for i, prompt in enumerate(prompts, 1):
    print(f"\n--- Cuento {i}: '{prompt}' ---")
    try:
        cuento = generador.generar_cuento(prompt)
        # Mostrar solo los primeros 200 caracteres
        preview = cuento[:200] + "..." if len(cuento) > 200 else cuento
        print(preview)
        print(f"Longitud: {len(cuento)} caracteres")
    except Exception as e:
        print(f"[ERROR] {e}")

print("\n" + "=" * 60)
print("[OK] PRUEBA COMPLETADA")
print("=" * 60)
print("\nSi los cuentos son diferentes, el sistema esta funcionando correctamente!")
print("Si son muy similares, el modelo puede necesitar mas entrenamiento.")

