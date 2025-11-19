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
                 usar_api_gemini: bool = False, gemini_api_key: Optional[str] = None,
                 usar_ml: bool = False, modelo_ml: str = "gpt2"):
        """
        Inicializa el generador de cuentos.
        
        Args:
            usar_api_openai: Si True, usa OpenAI API. Si False, usa generación basada en plantillas.
            api_key: Clave de API de OpenAI (requerida si usar_api_openai=True)
            usar_api_gemini: Si True, usa Google Gemini API. Si False, usa otros métodos.
            gemini_api_key: Clave de API de Gemini (requerida si usar_api_gemini=True)
            usar_ml: Si True, intenta usar modelo de ML (GPT-2). Requiere transformers instalado.
            modelo_ml: Nombre del modelo ML a usar ("gpt2", "distilgpt2", etc.)
        """
        self.usar_api_openai = usar_api_openai
        self.api_key = api_key
        self.usar_api_gemini = usar_api_gemini
        self.gemini_api_key = gemini_api_key
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
    
    def _generar_con_openai(self, prompt: str, duracion: str = "medio") -> str:
        """
        Genera un cuento usando la API de OpenAI.
        
        Args:
            prompt: Solicitud del usuario
            duracion: Duración del cuento ("corto", "medio", "largo")
            
        Returns:
            Cuento generado
        """
        try:
            from openai import OpenAI
            
            # Limpiar la API key antes de usarla
            api_key_limpia = self.api_key.strip() if self.api_key else None
            if not api_key_limpia:
                raise ValueError("API key de OpenAI no proporcionada")
            
            client = OpenAI(api_key=api_key_limpia)
            
            # Configuraciones según duración
            configuraciones = {
                "corto": {
                    "palabras": "150-200",
                    "max_tokens": 300,
                    "descripcion": "un cuento breve y conciso"
                },
                "medio": {
                    "palabras": "400-500",
                    "max_tokens": 700,
                    "descripcion": "un cuento de longitud media"
                },
                "largo": {
                    "palabras": "800-1000",
                    "max_tokens": 1400,
                    "descripcion": "un cuento extenso y detallado"
                }
            }
            config = configuraciones.get(duracion, configuraciones["medio"])
            
            # Prompt del sistema mejorado para mejor calidad
            prompt_sistema = (
                "Eres un narrador creativo y experto en escribir cuentos. "
                "Genera {descripcion} en español de {palabras} palabras con estructura narrativa completa "
                "(introducción, desarrollo, desenlace). "
                "Requisitos:\n"
                "- Estructura: introducción, desarrollo con conflictos, desenlace satisfactorio\n"
                "- Estilo: descripciones vívidas, diálogos naturales, elementos sensoriales, ritmo variado\n"
                "- Calidad: español fluido, coherencia, originalidad, apropiado para todas las edades\n"
                "- IMPORTANTE: Responde SOLO con el cuento, sin títulos ni explicaciones. Comienza directamente con la narrativa."
            ).format(
                descripcion=config["descripcion"],
                palabras=config["palabras"]
            )
            
            # Prompt del usuario más específico
            prompt_usuario = f"Escribe un cuento creativo sobre: {prompt}"
            
            print(f"[DEBUG] Prompt sistema: {prompt_sistema[:100]}...")
            print(f"[DEBUG] Prompt usuario: {prompt_usuario}")
            print(f"[DEBUG] Duración: {duracion} ({config['palabras']} palabras)")
            
            # Usar gpt-4o-mini (modelo válido y económico)
            modelo = "gpt-4o-mini"
            print(f"[DEBUG] Enviando UNA solicitud con modelo: {modelo}")
            
            try:
                respuesta = client.chat.completions.create(
                    model=modelo,
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": prompt_usuario}
                    ],
                    max_tokens=config["max_tokens"],
                    temperature=0.85  # Balance entre creatividad y coherencia
                )
                
                # Loguear información completa de la primera respuesta
                print(f"\n{'='*60}")
                print(f"[RESPONSE] Información de la respuesta:")
                print(f"{'='*60}")
                print(f"[RESPONSE] Modelo usado: {modelo}")
                print(f"[RESPONSE] ID: {respuesta.id}")
                print(f"[RESPONSE] Objeto: {respuesta.object}")
                print(f"[RESPONSE] Creado: {respuesta.created}")
                
                # Información de uso de tokens
                if hasattr(respuesta, 'usage') and respuesta.usage:
                    print(f"[RESPONSE] Tokens usados:")
                    print(f"  - Prompt tokens: {respuesta.usage.prompt_tokens}")
                    print(f"  - Completion tokens: {respuesta.usage.completion_tokens}")
                    print(f"  - Total tokens: {respuesta.usage.total_tokens}")
                
                # Intentar obtener headers de rate limit si están disponibles
                try:
                    # Los headers pueden estar en la respuesta raw si está disponible
                    if hasattr(respuesta, '_response') and hasattr(respuesta._response, 'headers'):
                        headers = respuesta._response.headers
                        print(f"\n[RESPONSE] Rate Limit Headers:")
                        rate_limit_headers = {
                            'x-ratelimit-limit-requests': headers.get('x-ratelimit-limit-requests', 'N/A'),
                            'x-ratelimit-limit-tokens': headers.get('x-ratelimit-limit-tokens', 'N/A'),
                            'x-ratelimit-remaining-requests': headers.get('x-ratelimit-remaining-requests', 'N/A'),
                            'x-ratelimit-remaining-tokens': headers.get('x-ratelimit-remaining-tokens', 'N/A'),
                            'x-ratelimit-reset-requests': headers.get('x-ratelimit-reset-requests', 'N/A'),
                            'x-ratelimit-reset-tokens': headers.get('x-ratelimit-reset-tokens', 'N/A'),
                        }
                        for key, value in rate_limit_headers.items():
                            print(f"  - {key}: {value}")
                except Exception as e_headers:
                    print(f"[RESPONSE] No se pudieron obtener headers de rate limit: {e_headers}")
                
                print(f"{'='*60}\n")
                
                cuento = respuesta.choices[0].message.content.strip()
                print(f"[OK] Cuento generado ({len(cuento)} caracteres)")
                return cuento
                
            except Exception as e_solicitud:
                # Capturar información detallada del error
                error_msg = str(e_solicitud)
                print(f"\n{'='*60}")
                print(f"[ERROR] Error en la solicitud:")
                print(f"{'='*60}")
                print(f"[ERROR] Mensaje: {error_msg}")
                
                # Intentar extraer información de headers y respuesta del error
                try:
                    if hasattr(e_solicitud, 'response'):
                        response = e_solicitud.response
                        
                        # Headers de rate limit del error
                        if hasattr(response, 'headers'):
                            headers = dict(response.headers)
                            print(f"\n[ERROR] Rate Limit Headers del error:")
                            rate_limit_keys = [
                                'x-ratelimit-limit-requests',
                                'x-ratelimit-limit-tokens',
                                'x-ratelimit-remaining-requests',
                                'x-ratelimit-remaining-tokens',
                                'x-ratelimit-reset-requests',
                                'x-ratelimit-reset-tokens',
                                'retry-after'
                            ]
                            for key in rate_limit_keys:
                                if key in headers:
                                    print(f"  - {key}: {headers[key]}")
                        
                        # Información del error JSON
                        if hasattr(response, 'json'):
                            try:
                                error_json = response.json()
                                print(f"\n[ERROR] Detalles del error JSON:")
                                import json
                                print(json.dumps(error_json, indent=2, ensure_ascii=False))
                                
                                # Distinguir entre rate limit y quota
                                if 'error' in error_json:
                                    error_info = error_json['error']
                                    error_type = error_info.get('type', '')
                                    error_code = error_info.get('code', '')
                                    
                                    if 'rate_limit' in error_type.lower() or 'rate_limit' in error_code.lower():
                                        print(f"\n[DIAGNOSTICO] Error 429 - RATE LIMIT (demasiadas solicitudes)")
                                        print("   Causa: Estás enviando solicitudes demasiado rápido")
                                        print("   Solución: Espera antes de enviar otra solicitud")
                                        if 'retry-after' in headers:
                                            print(f"   Espera {headers['retry-after']} segundos antes de reintentar")
                                    elif 'quota' in error_type.lower() or 'quota' in error_code.lower() or 'insufficient_quota' in error_code.lower():
                                        print(f"\n[DIAGNOSTICO] Error 429 - INSUFFICIENT QUOTA (sin créditos)")
                                        print("   Causa: No hay créditos disponibles o límite de gasto alcanzado")
                                        print("   Solución: Verifica tu cuenta en https://platform.openai.com/account/billing")
                            except:
                                pass
                        
                        # Status code
                        if hasattr(response, 'status_code'):
                            print(f"\n[ERROR] Status Code: {response.status_code}")
                    
                except Exception as e_debug:
                    print(f"[ERROR] No se pudo extraer información detallada: {e_debug}")
                
                print(f"{'='*60}\n")
                raise e_solicitud
            
        except Exception as e:
            # El error ya fue logueado en detalle dentro del try anterior
            # Aquí solo hacemos el fallback
            import traceback
            traceback.print_exc()
            # Fallback a generación con plantillas
            return self._generar_con_plantillas(prompt)
    
    def _generar_con_gemini(self, prompt: str, duracion: str = "medio") -> str:
        """
        Genera un cuento usando la API de Google Gemini.
        
        Args:
            prompt: Solicitud del usuario
            duracion: Duración del cuento ("corto", "medio", "largo")
            
        Returns:
            Cuento generado
        """
        try:
            import google.generativeai as genai
            
            # Limpiar la API key antes de usarla
            api_key_limpia = self.gemini_api_key.strip() if self.gemini_api_key else None
            if not api_key_limpia:
                raise ValueError("API key de Gemini no proporcionada")
            
            # Configurar la API key
            genai.configure(api_key=api_key_limpia)
            
            # Configurar el modelo (gemini-2.5-flash es rápido y eficiente)
            # Alternativas: gemini-pro-latest, gemini-2.5-pro
            modelo_nombre = 'gemini-2.5-flash'
            modelo = genai.GenerativeModel(modelo_nombre)
            
            # Validar y truncar prompt del usuario si es muy largo (máx ~500 caracteres)
            # Esto evita que el prompt del usuario consuma demasiados tokens
            prompt_original = prompt
            if len(prompt) > 500:
                print(f"[ADVERTENCIA] Prompt muy largo ({len(prompt)} caracteres), truncando a 500")
                prompt = prompt[:500].rsplit(' ', 1)[0]  # Truncar en el último espacio completo
                print(f"[INFO] Prompt truncado a: '{prompt}...'")
            
            # Configurar parámetros según duración
            # Nota: gemini-2.5-flash tiene límite de contexto, debemos balancear input/output tokens
            configuraciones = {
                "corto": {
                    "palabras": "150-200",
                    "max_tokens": 300,  # Reducido para dejar espacio al input
                    "descripcion": "un cuento breve y conciso"
                },
                "medio": {
                    "palabras": "400-500",
                    "max_tokens": 700,  # Reducido para dejar espacio al input
                    "descripcion": "un cuento de longitud media"
                },
                "largo": {
                    "palabras": "800-1000",
                    "max_tokens": 1400,  # Reducido para dejar espacio al input
                    "descripcion": "un cuento extenso y detallado"
                }
            }
            
            config = configuraciones.get(duracion, configuraciones["medio"])
            
            # Prompt optimizado y conciso para evitar MAX_TOKENS
            # Mantiene las instrucciones esenciales pero más compacto
            prompt_completo = (
                "Eres un narrador experto. Escribe {descripcion} en español de {palabras} palabras sobre: {prompt}\n\n"
                "Requisitos:\n"
                "- Estructura: introducción, desarrollo con conflictos, desenlace satisfactorio\n"
                "- Estilo: descripciones vívidas, diálogos naturales, elementos sensoriales, ritmo variado\n"
                "- Calidad: español fluido, coherencia, originalidad, apropiado para todas las edades\n"
                "- IMPORTANTE: Responde SOLO con el cuento, sin títulos ni explicaciones. Comienza directamente con la narrativa."
            ).format(
                descripcion=config["descripcion"],
                palabras=config["palabras"],
                prompt=prompt
            )
            
            # Calcular tokens aproximados del prompt (estimación: ~1 token = 4 caracteres en español)
            prompt_tokens_estimados = len(prompt_completo) // 4
            total_estimado = prompt_tokens_estimados + config['max_tokens']
            print(f"[DEBUG] Enviando UNA solicitud a Gemini")
            print(f"[DEBUG] Prompt tokens estimados: ~{prompt_tokens_estimados}")
            print(f"[DEBUG] Max output tokens: {config['max_tokens']}")
            print(f"[DEBUG] Total estimado: ~{total_estimado} tokens")
            
            # Advertencia si el total estimado es muy alto
            if total_estimado > 8000:
                print(f"[ADVERTENCIA] Total de tokens estimado muy alto ({total_estimado}), puede causar MAX_TOKENS")
            
            print(f"[DEBUG] Prompt: '{prompt_completo[:150]}...'")
            
            try:
                # Generar respuesta con configuración según duración
                # Usar max_output_tokens más conservador para evitar límites
                respuesta = modelo.generate_content(
                    prompt_completo,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.85,  # Balance entre creatividad y coherencia
                        top_p=0.95,
                        top_k=40,
                        max_output_tokens=config["max_tokens"],  # Ajustado según duración
                    )
                )
                
                # Loguear información completa de la primera respuesta
                print(f"\n{'='*60}")
                print(f"[RESPONSE] Información de la respuesta:")
                print(f"{'='*60}")
                print(f"[RESPONSE] Modelo usado: {modelo_nombre}")
                
                # Información de uso de tokens si está disponible
                if hasattr(respuesta, 'usage_metadata'):
                    usage = respuesta.usage_metadata
                    print(f"[RESPONSE] Tokens usados:")
                    if hasattr(usage, 'prompt_token_count'):
                        print(f"  - Prompt tokens: {usage.prompt_token_count}")
                    if hasattr(usage, 'candidates_token_count'):
                        print(f"  - Completion tokens: {usage.candidates_token_count}")
                    if hasattr(usage, 'total_token_count'):
                        print(f"  - Total tokens: {usage.total_token_count}")
                
                # Verificar que haya candidatos en la respuesta
                if not respuesta.candidates:
                    raise ValueError("Gemini no generó candidatos")
                
                # Verificar el finish_reason
                candidato = respuesta.candidates[0]
                finish_reason = candidato.finish_reason
                
                # Obtener el texto generado de forma segura desde los candidatos
                # No usar respuesta.text directamente porque puede lanzar error si finish_reason != STOP
                cuento = None
                try:
                    # Intentar obtener texto desde la propiedad text (solo funciona si finish_reason == STOP)
                    if finish_reason == 1:  # STOP
                        cuento = respuesta.text.strip() if respuesta.text else None
                    else:
                        # Si finish_reason no es STOP, extraer texto directamente de las partes del candidato
                        if hasattr(candidato, 'content') and candidato.content:
                            partes_texto = []
                            for parte in candidato.content.parts:
                                if hasattr(parte, 'text') and parte.text:
                                    partes_texto.append(parte.text)
                            if partes_texto:
                                cuento = ' '.join(partes_texto).strip()
                except (ValueError, AttributeError) as e:
                    # Si falla al acceder a respuesta.text, intentar desde candidato.content
                    print(f"[DEBUG] Error al acceder a respuesta.text: {e}, intentando desde candidato.content")
                    if hasattr(candidato, 'content') and candidato.content:
                        partes_texto = []
                        for parte in candidato.content.parts:
                            if hasattr(parte, 'text') and parte.text:
                                partes_texto.append(parte.text)
                        if partes_texto:
                            cuento = ' '.join(partes_texto).strip()
                
                # Procesar el texto obtenido según finish_reason
                if cuento:
                    # Si terminó por MAX_TOKENS pero hay contenido, usar lo generado
                    if finish_reason == 2:  # MAX_TOKENS
                        print(f"[ADVERTENCIA] Generación truncada por límite de tokens")
                        print(f"[INFO] Usando texto parcial generado ({len(cuento)} caracteres)")
                        # Intentar cerrar el cuento si es posible
                        if not cuento.endswith('.') and not cuento.endswith('!') and not cuento.endswith('?'):
                            # Buscar el último punto para cerrar la última oración
                            ultimo_punto = cuento.rfind('.')
                            if ultimo_punto > len(cuento) * 0.7:  # Si el último punto está en el 70% final
                                cuento = cuento[:ultimo_punto + 1]
                            else:
                                cuento += "."
                        print(f"{'='*60}\n")
                        print(f"[OK] Cuento generado (parcial, {len(cuento)} caracteres)")
                        return cuento
                    elif finish_reason == 1:  # STOP (éxito)
                        print(f"{'='*60}\n")
                        print(f"[OK] Cuento generado ({len(cuento)} caracteres)")
                        return cuento
                    else:
                        # Otro finish_reason (SAFETY, etc.) pero hay contenido
                        finish_reasons = {
                            0: "FINISH_REASON_UNSPECIFIED",
                            1: "STOP",
                            2: "MAX_TOKENS",
                            3: "SAFETY",
                            4: "RECITATION",
                            5: "OTHER"
                        }
                        razon = finish_reasons.get(finish_reason, f"UNKNOWN({finish_reason})")
                        print(f"[ADVERTENCIA] Finish reason: {razon}, pero hay contenido generado")
                        print(f"[INFO] Usando texto generado ({len(cuento)} caracteres)")
                        print(f"{'='*60}\n")
                        return cuento
                else:
                    # No hay texto generado
                    finish_reasons = {
                        0: "FINISH_REASON_UNSPECIFIED",
                        1: "STOP",
                        2: "MAX_TOKENS",
                        3: "SAFETY",
                        4: "RECITATION",
                        5: "OTHER"
                    }
                    razon = finish_reasons.get(finish_reason, f"UNKNOWN({finish_reason})")
                    raise ValueError(f"Gemini no generó contenido de texto. Finish reason: {razon}")
                
            except Exception as e_solicitud:
                # Capturar información detallada del error
                error_msg = str(e_solicitud)
                print(f"\n{'='*60}")
                print(f"[ERROR] Error en la solicitud:")
                print(f"{'='*60}")
                print(f"[ERROR] Mensaje: {error_msg}")
                
                # Intentar extraer más información del error
                try:
                    if hasattr(e_solicitud, 'response'):
                        response = e_solicitud.response
                        print(f"[ERROR] Status Code: {getattr(response, 'status_code', 'N/A')}")
                except:
                    pass
                
                print(f"{'='*60}\n")
                raise e_solicitud
            
        except ImportError:
            raise ImportError("google-generativeai no está instalado. Instala con: pip install google-generativeai")
        except Exception as e:
            # El error ya fue logueado en detalle dentro del try anterior
            import traceback
            traceback.print_exc()
            # Fallback a generación con plantillas
            return self._generar_con_plantillas(prompt)
    
    def generar_cuento(self, prompt: str, duracion: str = "medio") -> str:
        """
        Método principal para generar un cuento basado en el prompt.
        Prioridad: OpenAI > ML > Plantillas
        
        Args:
            prompt: Solicitud del usuario
            duracion: Duración del cuento ("corto" ~2min, "medio" ~5min, "largo" ~10min)
            
        Returns:
            Cuento generado con estructura narrativa completa
        """
        if not prompt or len(prompt.strip()) == 0:
            prompt = "una aventura creativa"
        
        print(f"\n{'='*60}")
        print(f"[INFO] Generando cuento con prompt:")
        print(f"       '{prompt}'")
        print(f"[INFO] Duración solicitada: {duracion}")
        print(f"{'='*60}\n")
        
        # Prioridad 1: OpenAI API (principal)
        if self.usar_api_openai and self.api_key:
            print("[INFO] Usando OpenAI API (gpt-4o-mini)")
            print(f"[INFO] Prompt enviado a OpenAI: '{prompt}'")
            print(f"[INFO] Duración: {duracion}")
            try:
                cuento = self._generar_con_openai(prompt, duracion)
                print(f"[OK] Cuento generado con OpenAI ({len(cuento)} caracteres)")
                return cuento
            except Exception as e:
                print(f"[ERROR] Error con OpenAI: {e}, usando respaldo")
        
        # Prioridad 3: Modelo ML (si está disponible)
        if self.usar_ml and self.generador_ml and self.generador_ml.esta_disponible():
            print("[INFO] Usando Modelo ML (GPT-2)")
            print(f"[INFO] Prompt enviado al modelo ML: '{prompt}'")
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
                        print(f"[OK] Cuento generado con ML ({len(cuento_ml)} caracteres)")
                        return cuento_ml
                    else:
                        print(f"[ADVERTENCIA] Cuento generado no parece relacionado con el prompt")
                        print(f"   Palabras comunes: {len(palabras_comunes)}")
                else:
                    print("[ADVERTENCIA] Modelo ML genero texto muy corto, usando respaldo")
            except Exception as e:
                print(f"[ERROR] Error con modelo ML: {e}, usando respaldo")
        
        # Prioridad 3: Plantillas (siempre disponible como respaldo)
        print("[INFO] Usando generacion por plantillas")
        print(f"[INFO] Prompt para plantillas: '{prompt}'")
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

