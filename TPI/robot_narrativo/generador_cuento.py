"""
Módulo Generador de Cuento
Responsable de crear narrativas originales y estructuradas basadas en prompts del usuario.
"""

import random
import re
from typing import Dict, List, Optional


class GeneradorCuento:
    """
    Clase principal para generar cuentos creativos a partir de prompts.
    Implementa lógica de generación con variabilidad y estructura narrativa.
    Soporta múltiples métodos: ML (GPT-2), OpenAI API, o plantillas creativas.
    """
    
    def __init__(self, usar_api_openai: bool = False, api_key: Optional[str] = None,
                 usar_ml: bool = False, modelo_ml: str = "gpt2"):
        """
        Inicializa el generador de cuentos.
        
        Args:
            usar_api_openai: Si True, usa OpenAI API. Si False, usa generación basada en plantillas.
            api_key: Clave de API de OpenAI (requerida si usar_api_openai=True)
            usar_ml: Si True, intenta usar modelo de ML (GPT-2). Requiere transformers instalado.
            modelo_ml: Nombre del modelo ML a usar ("gpt2", "distilgpt2", etc.)
        """
        self.usar_api_openai = usar_api_openai
        self.api_key = api_key
        self.usar_ml = usar_ml
        self.modelo_ml = modelo_ml
        self.generador_ml = None
        
        # Intentar cargar generador ML si está solicitado
        if usar_ml:
            try:
                from generador_ml import GeneradorML
                self.generador_ml = GeneradorML(modelo=modelo_ml, usar_gpu=False)
                if self.generador_ml.esta_disponible():
                    print(f"✅ Modelo ML ({modelo_ml}) cargado correctamente")
                else:
                    print("⚠️  Modelo ML no disponible, usando plantillas")
                    self.usar_ml = False
            except ImportError:
                print("⚠️  transformers no instalado. Instala con: pip install transformers torch")
                print("   Usando generación por plantillas")
                self.usar_ml = False
            except Exception as e:
                print(f"⚠️  Error al cargar modelo ML: {e}")
                print("   Usando generación por plantillas")
                self.usar_ml = False
        
        # Plantillas creativas para generación sin API
        self.introducciones = [
            "Érase una vez",
            "Hace mucho tiempo",
            "En un lugar muy lejano",
            "Cuenta la leyenda que",
            "En tiempos remotos",
        ]
        
        self.desarrollos = [
            "Sin embargo, algo inesperado sucedió",
            "Pero pronto descubrieron que",
            "No obstante, un día",
            "Sin embargo, la situación cambió cuando",
            "Pero entonces ocurrió algo extraordinario",
        ]
        
        self.finales = [
            "Y así fue como",
            "Desde ese día",
            "Y de esta manera",
            "Finalmente",
            "Y así",
        ]
        
        # Temas y elementos creativos
        self.personajes = ["héroe", "explorador", "sabio", "joven aventurero", "curioso investigador"]
        self.lugares = ["bosque encantado", "montaña misteriosa", "ciudad perdida", "isla secreta", "valle oculto"]
        self.objetos = ["llave antigua", "mapa misterioso", "cristal brillante", "libro encantado", "amuleto mágico"]
    
    def _extraer_elementos_prompt(self, prompt: str) -> Dict[str, List[str]]:
        """
        Extrae elementos clave del prompt del usuario.
        
        Args:
            prompt: Texto ingresado por el usuario
            
        Returns:
            Diccionario con elementos extraídos (personajes, lugares, temas, etc.)
        """
        prompt_lower = prompt.lower()
        elementos = {
            "personajes": [],
            "lugares": [],
            "temas": [],
            "acciones": [],
        }
        
        # Detección simple de palabras clave
        palabras_clave = prompt_lower.split()
        
        # Identificar temas comunes
        temas_detectados = []
        if any(palabra in prompt_lower for palabra in ["aventura", "aventurero", "explorar"]):
            temas_detectados.append("aventura")
        if any(palabra in prompt_lower for palabra in ["misterio", "misterioso", "secreto"]):
            temas_detectados.append("misterio")
        if any(palabra in prompt_lower for palabra in ["magia", "mágico", "encantado"]):
            temas_detectados.append("magia")
        if any(palabra in prompt_lower for palabra in ["amistad", "amigo", "compañero"]):
            temas_detectados.append("amistad")
        if any(palabra in prompt_lower for palabra in ["valentía", "valiente", "coraje"]):
            temas_detectados.append("valentía")
        
        elementos["temas"] = temas_detectados if temas_detectados else ["aventura"]
        
        return elementos
    
    def _generar_con_plantillas(self, prompt: str) -> str:
        """
        Genera un cuento usando plantillas creativas y variabilidad.
        
        Args:
            prompt: Solicitud del usuario
            
        Returns:
            Cuento generado con estructura narrativa completa
        """
        elementos = self._extraer_elementos_prompt(prompt)
        
        # Selección creativa de elementos
        personaje = random.choice(self.personajes)
        lugar = random.choice(self.lugares)
        objeto = random.choice(self.objetos)
        tema = elementos["temas"][0] if elementos["temas"] else "aventura"
        
        # Construcción del cuento con estructura narrativa
        introduccion = f"{random.choice(self.introducciones)}, un {personaje} descubrió un {lugar}."
        
        desarrollo = (
            f"{random.choice(self.desarrollos)} encontró un {objeto} que cambiaría todo. "
            f"El {personaje} se embarcó en una {tema} que lo llevaría más allá de lo imaginado. "
            f"En su camino, enfrentó desafíos que pusieron a prueba su determinación y creatividad."
        )
        
        desenlace = (
            f"{random.choice(self.finales)} el {personaje} aprendió que la verdadera {tema} "
            f"está en encontrar soluciones innovadoras a los problemas. "
            f"El {objeto} resultó ser solo el comienzo de una historia mucho mayor."
        )
        
        cuento = f"{introduccion}\n\n{desarrollo}\n\n{desenlace}"
        
        # Añadir variabilidad: cada ejecución puede tener pequeñas diferencias
        if random.random() > 0.5:
            cuento += f"\n\nY así, el {personaje} demostró que la creatividad puede transformar cualquier situación."
        
        return cuento
    
    def _generar_con_openai(self, prompt: str) -> str:
        """
        Genera un cuento usando la API de OpenAI.
        
        Args:
            prompt: Solicitud del usuario
            
        Returns:
            Cuento generado
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            prompt_sistema = (
                "Eres un narrador creativo. Genera un cuento original en español con estructura narrativa completa "
                "(introducción, desarrollo, desenlace). El cuento debe tener entre 150 y 300 palabras, "
                "ser creativo, original y tener un formato de cuento tradicional. "
                "Responde SOLO con el cuento, sin explicaciones adicionales."
            )
            
            respuesta = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": f"Genera un cuento sobre: {prompt}"}
                ],
                max_tokens=400,
                temperature=0.8  # Mayor creatividad
            )
            
            cuento = respuesta.choices[0].message.content.strip()
            return cuento
            
        except Exception as e:
            print(f"Error al generar con OpenAI: {e}")
            # Fallback a generación con plantillas
            return self._generar_con_plantillas(prompt)
    
    def generar_cuento(self, prompt: str) -> str:
        """
        Método principal para generar un cuento basado en el prompt.
        Prioridad: ML > OpenAI > Plantillas
        
        Args:
            prompt: Solicitud del usuario
            
        Returns:
            Cuento generado con estructura narrativa completa
        """
        if not prompt or len(prompt.strip()) == 0:
            prompt = "una aventura creativa"
        
        # Prioridad 1: Modelo ML (si está disponible)
        if self.usar_ml and self.generador_ml and self.generador_ml.esta_disponible():
            try:
                cuento_ml = self.generador_ml.generar_cuento(
                    prompt, 
                    max_length=250,
                    temperature=0.8,
                    top_p=0.9
                )
                # Validar que el cuento generado sea razonable
                if cuento_ml and len(cuento_ml.strip()) > 50:
                    return cuento_ml
                else:
                    print("⚠️  Modelo ML generó texto muy corto, usando respaldo")
            except Exception as e:
                print(f"⚠️  Error con modelo ML: {e}, usando respaldo")
        
        # Prioridad 2: OpenAI API
        if self.usar_api_openai and self.api_key:
            return self._generar_con_openai(prompt)
        
        # Prioridad 3: Plantillas (siempre disponible como respaldo)
        return self._generar_con_plantillas(prompt)
    
    def validar_estructura_cuento(self, cuento: str) -> bool:
        """
        Valida que el cuento tenga una estructura narrativa adecuada.
        
        Args:
            cuento: Texto del cuento a validar
            
        Returns:
            True si tiene estructura válida, False en caso contrario
        """
        if not cuento or len(cuento.strip()) < 100:
            return False
        
        # Verificar que tenga al menos algunos elementos de estructura narrativa
        tiene_introduccion = any(palabra in cuento.lower() for palabra in 
                                ["érase", "había", "era", "cuenta", "hace"])
        tiene_desarrollo = len(cuento.split(".")) >= 3
        tiene_cierre = any(palabra in cuento.lower() for palabra in 
                          ["finalmente", "así", "desde", "entonces"])
        
        return tiene_introduccion and tiene_desarrollo

