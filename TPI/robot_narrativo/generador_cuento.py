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
        
        # Temas y elementos creativos (expandidos para más variabilidad)
        self.personajes = [
            "héroe", "explorador", "sabio", "joven aventurero", "curioso investigador",
            "valiente guerrero", "astuto inventor", "sabia anciana", "niño curioso", 
            "artista soñador", "científico intrépido", "mago aprendiz", "viajero incansable"
        ]
        self.lugares = [
            "bosque encantado", "montaña misteriosa", "ciudad perdida", "isla secreta", "valle oculto",
            "castillo abandonado", "cueva profunda", "templo antiguo", "jardín mágico", "desierto infinito",
            "océano desconocido", "laberinto interminable", "torre solitaria", "puente entre mundos"
        ]
        self.objetos = [
            "llave antigua", "mapa misterioso", "cristal brillante", "libro encantado", "amuleto mágico",
            "espejo mágico", "piedra luminosa", "flauta encantada", "diario secreto", "brújula dorada",
            "espada legendaria", "corona perdida", "pergamino antiguo", "gema brillante"
        ]
    
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
        Mejorado para usar mejor el prompt del usuario y generar cuentos más únicos.
        
        Args:
            prompt: Solicitud del usuario
            
        Returns:
            Cuento generado con estructura narrativa completa
        """
        elementos = self._extraer_elementos_prompt(prompt)
        
        # Extraer palabras clave del prompt para personalizar el cuento
        palabras_prompt = [p.lower() for p in prompt.split() if len(p) > 3]
        palabras_unicas = list(set(palabras_prompt))[:5]  # Máximo 5 palabras únicas
        
        # Selección creativa de elementos con más variabilidad
        personaje = random.choice(self.personajes)
        lugar = random.choice(self.lugares)
        objeto = random.choice(self.objetos)
        tema = elementos["temas"][0] if elementos["temas"] else "aventura"
        
        # Incorporar palabras del prompt en el cuento
        palabra_contexto = random.choice(palabras_unicas) if palabras_unicas else None
        
        # Variaciones más creativas de introducciones
        introducciones_variadas = [
            f"{random.choice(self.introducciones)}, un {personaje} descubrió un {lugar}.",
            f"{random.choice(self.introducciones)}, en un {lugar}, vivía un {personaje}.",
            f"{random.choice(self.introducciones)}, un {personaje} se encontró en un {lugar} misterioso.",
            f"En un {lugar} lejano, {random.choice(self.introducciones).lower()} un {personaje}.",
        ]
        
        introduccion = random.choice(introducciones_variadas)
        
        # Si hay palabras del prompt, integrarlas creativamente
        if palabra_contexto and palabra_contexto not in [personaje, lugar, objeto]:
            introduccion = introduccion.replace("descubrió", f"descubrió algo relacionado con {palabra_contexto}")
        
        # Desarrollos más variados
        desarrollos_variados = [
            f"{random.choice(self.desarrollos)} encontró un {objeto} que cambiaría todo. "
            f"El {personaje} se embarcó en una {tema} que lo llevaría más allá de lo imaginado. "
            f"En su camino, enfrentó desafíos que pusieron a prueba su determinación y creatividad.",
            
            f"{random.choice(self.desarrollos)} el {personaje} descubrió que el {lugar} guardaba secretos increíbles. "
            f"Con el {objeto} en sus manos, comenzó una {tema} llena de sorpresas y descubrimientos.",
            
            f"El {personaje} pronto se dio cuenta de que el {lugar} no era lo que parecía. "
            f"{random.choice(self.desarrollos)} encontró un {objeto} que despertó su curiosidad. "
            f"Así comenzó una {tema} que transformaría su vida para siempre.",
        ]
        
        desarrollo = random.choice(desarrollos_variados)
        
        # Desenlaces más variados
        desenlaces_variados = [
            f"{random.choice(self.finales)} el {personaje} aprendió que la verdadera {tema} "
            f"está en encontrar soluciones innovadoras a los problemas. "
            f"El {objeto} resultó ser solo el comienzo de una historia mucho mayor.",
            
            f"{random.choice(self.finales)} el {personaje} comprendió que cada {tema} "
            f"es una oportunidad para demostrar creatividad. "
            f"El {lugar} y el {objeto} fueron solo el inicio de algo extraordinario.",
            
            f"Al final, el {personaje} descubrió que la {tema} no era solo sobre el {objeto}, "
            f"sino sobre el viaje mismo. {random.choice(self.finales)} todo cambió para mejor.",
        ]
        
        desenlace = random.choice(desenlaces_variados)
        
        # Construir el cuento
        cuento = f"{introduccion}\n\n{desarrollo}\n\n{desenlace}"
        
        # Añadir variabilidad adicional con frases finales opcionales
        frases_finales = [
            f"\n\nY así, el {personaje} demostró que la creatividad puede transformar cualquier situación.",
            f"\n\nDesde entonces, el {personaje} supo que cada desafío es una oportunidad para crear algo nuevo.",
            f"\n\nEl {personaje} aprendió que la verdadera magia está en ver las cosas de manera diferente.",
            f"\n\nY de esta forma, el {personaje} se convirtió en un ejemplo de cómo la creatividad puede cambiar el mundo.",
        ]
        
        if random.random() > 0.3:  # 70% de probabilidad de añadir frase final
            cuento += random.choice(frases_finales)
        
        # Añadir un toque único basado en el prompt
        if palabras_unicas and random.random() > 0.7:  # 30% de probabilidad
            palabra_extra = random.choice(palabras_unicas)
            if palabra_extra not in cuento.lower():
                cuento = cuento.replace(".", f", relacionado con {palabra_extra}.", 1)
        
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
                    max_length=400,  # Aumentado para cuentos más completos
                    temperature=0.9,  # Más creatividad
                    top_p=0.95,
                    traducir=True  # Activar traducción para mejor calidad
                )
                # Validar que el cuento generado sea razonable y relevante
                if cuento_ml and len(cuento_ml.strip()) > 100:  # Mínimo aumentado
                    # Verificar que el cuento tenga relación con el prompt
                    palabras_prompt = set(prompt.lower().split())
                    palabras_cuento = set(cuento_ml.lower().split())
                    # Al menos algunas palabras del prompt deben aparecer en el cuento
                    palabras_comunes = palabras_prompt.intersection(palabras_cuento)
                    if len(palabras_comunes) >= 2 or len(cuento_ml.strip()) > 200:
                        return cuento_ml
                    else:
                        print(f"[ADVERTENCIA] Cuento generado no parece relacionado con el prompt")
                        print(f"   Palabras comunes: {len(palabras_comunes)}")
                else:
                    print("[ADVERTENCIA] Modelo ML genero texto muy corto, usando respaldo")
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
        Validación más flexible para permitir más variaciones.
        
        Args:
            cuento: Texto del cuento a validar
            
        Returns:
            True si tiene estructura válida, False en caso contrario
        """
        if not cuento or len(cuento.strip()) < 50:  # Reducido de 100 a 50
            return False
        
        # Verificar que tenga contenido sustancial (más de 3 oraciones)
        oraciones = [s.strip() for s in cuento.split('.') if s.strip()]
        if len(oraciones) < 3:
            return False
        
        # Verificar que tenga al menos algunos elementos de estructura narrativa
        # Más flexible: solo necesita tener algunas palabras narrativas
        palabras_narrativas = [
            "érase", "había", "era", "cuenta", "hace", "una vez",
            "entonces", "después", "finalmente", "así", "desde",
            "personaje", "protagonista", "aventura", "historia"
        ]
        tiene_elementos_narrativos = any(
            palabra in cuento.lower() for palabra in palabras_narrativas
        )
        
        # Si tiene elementos narrativos y suficientes oraciones, es válido
        return tiene_elementos_narrativos or len(oraciones) >= 5

