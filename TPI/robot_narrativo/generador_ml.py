"""
Módulo Generador de Cuento con Modelo de Machine Learning
Implementa generación usando modelos pre-entrenados (GPT-2, etc.)
Usa ejemplos de cuentos para mejorar la calidad de la generación mediante prompt engineering.
"""

import torch
import json
import os
import sys
import io
from typing import Optional, Dict, List
import warnings
warnings.filterwarnings('ignore')

# Configurar encoding para Windows
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass


class GeneradorML:
    """
    Generador de cuentos usando modelos de lenguaje pre-entrenados.
    Soporta GPT-2 y otros modelos de Hugging Face.
    """
    
    def __init__(self, modelo: str = "gpt2", usar_gpu: bool = False):
        """
        Inicializa el generador con modelo de ML.
        
        Args:
            modelo: Nombre del modelo a usar
                   - "gpt2": GPT-2 base (inglés, pero funciona)
                   - "gpt2-spanish": Si está disponible
                   - "distilgpt2": Versión más ligera
                   - "./modelo_cuentos": Ruta a modelo fine-tuneado propio
            usar_gpu: Si True, intenta usar GPU (CUDA)
        """
        self.modelo_nombre = modelo
        self.usar_gpu = usar_gpu and torch.cuda.is_available()
        self.tokenizer = None
        self.model = None
        self.cuentos_ejemplo = {}
        self._cargar_cuentos_ejemplo()
        self._cargar_modelo()
    
    def _cargar_cuentos_ejemplo(self):
        """Carga los cuentos de ejemplo desde el archivo JSON."""
        try:
            # Buscar el archivo de cuentos de ejemplo
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ruta_cuentos = os.path.join(base_dir, "robot_narrativo", "data", "cuentos_ejemplo.json")
            
            # Si no está ahí, intentar ruta relativa
            if not os.path.exists(ruta_cuentos):
                ruta_cuentos = os.path.join(os.path.dirname(__file__), "data", "cuentos_ejemplo.json")
            
            if os.path.exists(ruta_cuentos):
                with open(ruta_cuentos, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Organizar por tema para acceso rápido
                    for cuento in data.get('cuentos', []):
                        tema = cuento.get('tema', 'generico')
                        self.cuentos_ejemplo[tema] = cuento.get('ejemplo', '')
                print(f"[OK] Cargados {len(self.cuentos_ejemplo)} cuentos de ejemplo")
            else:
                print("[ADVERTENCIA] No se encontro archivo de cuentos de ejemplo")
                self.cuentos_ejemplo = {}
        except Exception as e:
            print(f"[ADVERTENCIA] Error al cargar cuentos de ejemplo: {e}")
            self.cuentos_ejemplo = {}
    
    def _cargar_modelo(self):
        """Carga el modelo y tokenizer."""
        try:
            from transformers import GPT2LMHeadModel, GPT2Tokenizer
            
            print(f"[INFO] Cargando modelo {self.modelo_nombre}...")
            
            # Cargar tokenizer
            self.tokenizer = GPT2Tokenizer.from_pretrained(self.modelo_nombre)
            
            # Añadir token de padding si no existe
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Cargar modelo
            self.model = GPT2LMHeadModel.from_pretrained(self.modelo_nombre)
            self.model.eval()  # Modo evaluación (no entrenamiento)
            
            # Mover a GPU si está disponible
            if self.usar_gpu:
                self.model = self.model.cuda()
                print("[OK] Modelo cargado en GPU")
            else:
                print("[OK] Modelo cargado en CPU")
            
            print(f"[OK] Modelo {self.modelo_nombre} listo")
            
        except ImportError:
            raise ImportError(
                "transformers no esta instalado. Instala con: pip install transformers torch"
            )
        except Exception as e:
            print(f"[ADVERTENCIA] Error al cargar modelo: {e}")
            print("   El sistema usara generacion por plantillas como respaldo")
            self.model = None
            self.tokenizer = None
    
    def generar_cuento(self, prompt: str, max_length: int = 300, 
                       temperature: float = 0.85, top_p: float = 0.9,
                       traducir: bool = True) -> str:
        """
        Genera un cuento basado en el prompt.
        
        Args:
            prompt: Texto inicial o solicitud del usuario (en español)
            max_length: Longitud máxima del texto generado
            temperature: Controla la creatividad (0.1-1.5, mayor = más creativo)
            top_p: Nucleus sampling (0.1-1.0)
            traducir: Si True, traduce el prompt a inglés y el resultado a español
            
        Returns:
            Cuento generado (en español)
        """
        if not self.model or not self.tokenizer:
            raise RuntimeError("Modelo no está cargado")
        
        # Traducir prompt a inglés si está habilitado
        prompt_original = prompt
        if traducir:
            try:
                from traductor import obtener_traductor
                traductor = obtener_traductor()
                if traductor.esta_disponible():
                    # Traducir el prompt directamente, manteniendo el contexto
                    prompt_ingles = traductor.traducir_a_ingles(prompt)
                    print(f"[INFO] Prompt original: {prompt_original[:100]}...")
                    print(f"[INFO] Prompt traducido: {prompt_ingles[:100]}...")
                    prompt = prompt_ingles
                else:
                    print("[ADVERTENCIA] Traductor no disponible, usando prompt original")
            except Exception as e:
                print(f"[ADVERTENCIA] Error al traducir prompt: {e}, usando original")
        
        # Preparar prompt (ahora puede estar en inglés)
        prompt_preparado = self._preparar_prompt(prompt, en_ingles=traducir)
        
        try:
            # Tokenizar con attention_mask
            inputs_dict = self.tokenizer(
                prompt_preparado, 
                return_tensors="pt",
                truncation=True,
                max_length=512  # Limitar longitud del prompt
            )
            inputs = inputs_dict['input_ids']
            attention_mask = inputs_dict.get('attention_mask', None)
            
            # Mover a GPU si está disponible
            if self.usar_gpu:
                inputs = inputs.cuda()
                if attention_mask is not None:
                    attention_mask = attention_mask.cuda()
            
            # Generar con parámetros optimizados
            # Calcular max_new_tokens basado en la longitud del input
            input_length = inputs.shape[1]
            # Generar más tokens para cuentos más completos (300-400 tokens nuevos)
            max_new_tokens = max(300, min(400, max_length - input_length))
            
            with torch.no_grad():  # No calcular gradientes (más rápido)
                generate_kwargs = {
                    'max_new_tokens': max_new_tokens,  # Usar max_new_tokens en lugar de max_length
                    'min_new_tokens': 200,  # Longitud mínima aumentada para cuentos más completos
                    'temperature': 0.8,  # Balance entre creatividad y coherencia
                    'top_p': 0.9,  # Nucleus sampling
                    'top_k': 40,  # Top-k sampling para mejor control
                    'do_sample': True,  # Muestra aleatoria (más creativo)
                    'pad_token_id': self.tokenizer.eos_token_id,
                    'eos_token_id': self.tokenizer.eos_token_id,
                    'repetition_penalty': 1.2,  # Penalización de repetición moderada
                    'num_return_sequences': 1,
                    'no_repeat_ngram_size': 2,  # Evitar repetición de bigramas
                    'early_stopping': True  # Detener cuando encuentra EOS token
                }
                
                # Añadir attention_mask si está disponible
                if attention_mask is not None:
                    generate_kwargs['attention_mask'] = attention_mask
                
                outputs = self.model.generate(inputs, **generate_kwargs)
            
            # Decodificar
            texto_generado = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Limpiar y formatear (puede estar en inglés)
            cuento = self._limpiar_texto(texto_generado, prompt_preparado)
            
            # Traducir de vuelta a español si se tradujo el prompt
            if traducir:
                try:
                    from traductor import obtener_traductor
                    traductor = obtener_traductor()
                    if traductor.esta_disponible():
                        # Limpiar el cuento antes de traducir para mejor resultado
                        cuento_limpio = cuento.strip()
                        # Asegurar que tenga contenido sustancial antes de traducir
                        if len(cuento_limpio) > 50:
                            cuento_traducido = traductor.traducir_a_espanol(cuento_limpio)
                            if cuento_traducido and len(cuento_traducido.strip()) > 50:
                                cuento = cuento_traducido
                                print(f"[OK] Cuento traducido exitosamente ({len(cuento)} caracteres)")
                            else:
                                print("[ADVERTENCIA] Traduccion muy corta, usando original")
                        else:
                            print("[ADVERTENCIA] Cuento muy corto para traducir")
                    else:
                        print("[ADVERTENCIA] Traductor no disponible, devolviendo cuento en ingles")
                except Exception as e:
                    print(f"[ADVERTENCIA] Error al traducir cuento a espanol: {e}")
                    print("   Devolviendo cuento en ingles")
            
            return cuento
            
        except Exception as e:
            print(f"Error al generar con modelo: {e}")
            raise
    
    def _detectar_tema(self, prompt: str) -> str:
        """
        Detecta el tema del prompt para seleccionar el ejemplo más relevante.
        
        Args:
            prompt: Prompt del usuario
            
        Returns:
            Tema detectado
        """
        prompt_lower = prompt.lower()
        
        temas_keywords = {
            "aventura": ["aventura", "explorar", "viaje", "expedición", "descubrir"],
            "misterio": ["misterio", "misterioso", "secreto", "enigma", "investigar"],
            "magia": ["magia", "mágico", "hechizo", "encantado", "brujo"],
            "amistad": ["amistad", "amigo", "compañero", "amistoso"],
            "valentía": ["valentía", "valiente", "coraje", "brave", "heroico"],
            "creatividad": ["creatividad", "creativo", "innovador", "inventar"],
            "perseverancia": ["perseverancia", "perseverar", "esfuerzo", "constancia"]
        }
        
        for tema, keywords in temas_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return tema
        
        return "generico"
    
    def _preparar_prompt(self, prompt: str, en_ingles: bool = False) -> str:
        """
        Prepara el prompt mejorado usando ejemplos de cuentos para guiar al modelo.
        Usa prompt engineering con few-shot learning.
        
        Args:
            prompt: Prompt original del usuario (puede estar en inglés si se tradujo)
            en_ingles: Si True, el prompt está en inglés y se debe generar en inglés
            
        Returns:
            Prompt mejorado con ejemplos
        """
        if en_ingles:
            # Prompt en inglés para mejor generación con GPT-2
            # MUY directo: empezar el cuento directamente con el tema
            # Esto fuerza al modelo a generar sobre el tema específico
            prompt_mejorado = f"""Once upon a time, {prompt}. """
        else:
            # Detectar tema (solo si está en español)
        tema = self._detectar_tema(prompt)
        
        # Obtener ejemplo relevante
        ejemplo_cuento = self.cuentos_ejemplo.get(tema, self.cuentos_ejemplo.get("generico", ""))
        
        # Construir prompt mejorado con few-shot learning
        if ejemplo_cuento:
            # Prompt con ejemplo (few-shot learning)
            prompt_mejorado = f"""Eres un narrador creativo de cuentos en español. Genera un cuento original con estructura narrativa completa (introducción, desarrollo, desenlace).

Ejemplo de cuento:
{ejemplo_cuento}

Ahora genera un cuento nuevo sobre: {prompt}

Cuento:"""
        else:
            # Prompt sin ejemplo (fallback)
            prompt_mejorado = f"""Eres un narrador creativo. Genera un cuento original en español con estructura narrativa completa (introducción, desarrollo, desenlace). El cuento debe tener entre 150 y 300 palabras.

Tema: {prompt}

Cuento:"""
        
        return prompt_mejorado
    
    def _limpiar_texto(self, texto: str, prompt_original: str) -> str:
        """
        Limpia y formatea el texto generado, extrayendo solo el cuento.
        Funciona tanto para español como inglés.
        
        Args:
            texto: Texto generado por el modelo
            prompt_original: Prompt original para remover duplicado
            
        Returns:
            Texto limpio y formateado (solo el cuento)
        """
        import re
        
        # Remover el prompt original si aparece al inicio
        if texto.startswith(prompt_original):
            texto = texto[len(prompt_original):].strip()
        
        # Buscar marcadores comunes que indican inicio del cuento (español e inglés)
        marcadores_inicio_es = ["cuento:", "cuento", "érase", "hace", "en un", "cuenta", "story:", "story"]
        marcadores_inicio_en = ["story:", "story", "once", "there", "in a", "tale"]
        marcadores_inicio = marcadores_inicio_es + marcadores_inicio_en
        
        for marcador in marcadores_inicio:
            idx = texto.lower().find(marcador)
            if idx >= 0 and idx < 50:  # Si está cerca del inicio
                texto = texto[idx + len(marcador):].strip()
                # Limpiar dos puntos o espacios extra
                texto = re.sub(r'^[:]\s*', '', texto)
                break
        
        # Limpiar espacios múltiples y saltos de línea
        texto = re.sub(r'\s+', ' ', texto)
        texto = re.sub(r'\n+', ' ', texto)
        
        # Remover prefijos comunes que el modelo puede añadir (español e inglés)
        prefijos_a_remover_es = [
            "el cuento es:", "el cuento:", "cuento:", 
            "aquí está el cuento:", "generado:", "historia:", "la historia:",
            "este libro", "este texto", "esta historia"
        ]
        prefijos_a_remover_en = [
            "the story is:", "the story:", "story:", 
            "here is the story:", "generated:", "narrative:",
            "this book", "this text", "this story describes"
        ]
        prefijos_a_remover = prefijos_a_remover_es + prefijos_a_remover_en
        
        texto_lower = texto.lower()
        for prefijo in prefijos_a_remover:
            if texto_lower.startswith(prefijo):
                texto = texto[len(prefijo):].strip()
                break
        
        # Remover el prompt completo si aparece al inicio (más agresivo)
        # Buscar y remover el tema/prompt traducido
        if "topic:" in texto_lower or "tema:" in texto_lower or "about:" in texto_lower:
            # Encontrar donde termina el prompt y comienza el cuento
            idx_topic = texto_lower.find("topic:")
            idx_tema = texto_lower.find("tema:")
            idx_about = texto_lower.find("about:")
            idx = min(
                idx_topic if idx_topic >= 0 else len(texto), 
                idx_tema if idx_tema >= 0 else len(texto),
                idx_about if idx_about >= 0 else len(texto)
            )
            if idx < len(texto):
                # Buscar "story:" o "cuento:" después del topic
                idx_story = texto_lower.find("story:", idx)
                idx_cuento = texto_lower.find("cuento:", idx)
                if idx_story >= 0:
                    texto = texto[idx_story + len("story:"):].strip()
                elif idx_cuento >= 0:
                    texto = texto[idx_cuento + len("cuento:"):].strip()
                else:
                    # Si no encuentra marcador, tomar desde después de "topic:" o "about:"
                    partes = texto[idx:].split("\n", 1)
                    if len(partes) > 1:
                        texto = partes[1].strip()
                    else:
                        # Buscar la primera oración que empiece con mayúscula después del prompt
                        texto_restante = texto[idx:]
                        oraciones = texto_restante.split('.')
                        if len(oraciones) > 1:
                            # Tomar desde la segunda oración
                            texto = '.'.join(oraciones[1:]).strip()
        
        # Remover frases comunes que no son parte del cuento
        frases_a_remover = [
            "this book describes", "este libro describe", "this text describes",
            "the following story", "la siguiente historia", "requirements:",
            "requisitos:", "complete narrative", "estructura narrativa"
        ]
        for frase in frases_a_remover:
            if frase in texto_lower:
                idx = texto_lower.find(frase)
                # Buscar el siguiente punto o salto de línea
                idx_punto = texto.find('.', idx)
                idx_nueva_linea = texto.find('\n', idx)
                idx_fin = min(
                    idx_punto if idx_punto >= 0 else len(texto),
                    idx_nueva_linea if idx_nueva_linea >= 0 else len(texto)
                )
                if idx_fin < len(texto):
                    texto = texto[:idx] + texto[idx_fin+1:].strip()
                break
        
        # Asegurar que empiece con mayúscula
        if texto and texto[0].islower():
            texto = texto[0].upper() + texto[1:]
        
        # Asegurar que termine con punto
        texto = texto.strip()
        if texto and not texto[-1] in '.!?':
            texto += '.'
        
        # Limitar longitud (aproximadamente 300 palabras)
        palabras = texto.split()
        if len(palabras) > 300:
            # Encontrar el último punto antes de 300 palabras
            texto_corto = ' '.join(palabras[:300])
            ultimo_punto = texto_corto.rfind('.')
            if ultimo_punto > 0:
                texto = texto_corto[:ultimo_punto + 1]
            else:
                texto = texto_corto + '.'
        
        return texto
    
    def esta_disponible(self) -> bool:
        """Verifica si el modelo está cargado y disponible."""
        return self.model is not None and self.tokenizer is not None

