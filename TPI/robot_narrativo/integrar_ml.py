"""
Script para integrar el modelo de ML con el sistema actual.
Muestra cómo modificar generador_cuento.py para usar el modelo ML.
"""

# Este es un ejemplo de cómo modificar generador_cuento.py

# En generador_cuento.py, añadir al inicio:
"""
from generador_ml import GeneradorML

# En el __init__ de GeneradorCuento:
def __init__(self, usar_api_openai: bool = False, api_key: Optional[str] = None,
             usar_ml: bool = True, modelo_ml: str = "gpt2"):
    # ... código existente ...
    
    # Añadir generador ML
    self.usar_ml = usar_ml
    if usar_ml:
        try:
            self.generador_ml = GeneradorML(modelo=modelo_ml, usar_gpu=False)
            if self.generador_ml.esta_disponible():
                print("✅ Modelo ML cargado correctamente")
            else:
                print("⚠️  Modelo ML no disponible, usando plantillas")
                self.usar_ml = False
        except Exception as e:
            print(f"⚠️  Error al cargar modelo ML: {e}")
            print("   Usando generación por plantillas")
            self.usar_ml = False
    else:
        self.generador_ml = None

# Modificar el método generar_cuento:
def generar_cuento(self, prompt: str) -> str:
    if not prompt or len(prompt.strip()) == 0:
        prompt = "una aventura creativa"
    
    # Prioridad: ML > OpenAI > Plantillas
    if self.usar_ml and self.generador_ml and self.generador_ml.esta_disponible():
        try:
            return self.generador_ml.generar_cuento(prompt, max_length=250)
        except Exception as e:
            print(f"Error con modelo ML: {e}, usando respaldo")
    
    if self.usar_api_openai and self.api_key:
        return self._generar_con_openai(prompt)
    else:
        return self._generar_con_plantillas(prompt)
"""

print("""
📝 INSTRUCCIONES PARA INTEGRAR MODELO ML:

1. Instalar dependencias:
   pip install transformers torch

2. El archivo generador_ml.py ya está creado

3. Modificar generador_cuento.py según el ejemplo arriba

4. En app.py, cambiar la inicialización:
   generador = GeneradorCuento(usar_ml=True, modelo_ml="gpt2")

5. Probar el sistema
""")

