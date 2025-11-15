"""
Módulo Generador de Cuento con Modelo de Machine Learning
Implementa generación usando modelos pre-entrenados (GPT-2, etc.)
Usa ejemplos de cuentos para mejorar la calidad de la generación mediante prompt engineering.
"""

import torch
import json
import os
from typing import Optional, Dict, List
import warnings
warnings.filterwarnings('ignore')


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
                print(f"✅ Cargados {len(self.cuentos_ejemplo)} cuentos de ejemplo")
            else:
                print("⚠️  No se encontró archivo de cuentos de ejemplo")
                self.cuentos_ejemplo = {}
        except Exception as e:
            print(f"⚠️  Error al cargar cuentos de ejemplo: {e}")
            self.cuentos_ejemplo = {}
    
    def _cargar_modelo(self):
        """Carga el modelo y tokenizer."""
        try:
            from transformers import GPT2LMHeadModel, GPT2Tokenizer
            
            print(f"📥 Cargando modelo {self.modelo_nombre}...")
            
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
                print("✅ Modelo cargado en GPU")
            else:
                print("✅ Modelo cargado en CPU")
            
            print(f"✅ Modelo {self.modelo_nombre} listo")
            
        except ImportError:
            raise ImportError(
                "transformers no está instalado. Instala con: pip install transformers torch"
            )
        except Exception as e:
            print(f"⚠️  Error al cargar modelo: {e}")
            print("   El sistema usará generación por plantillas como respaldo")
            self.model = None
            self.tokenizer = None
    
    def generar_cuento(self, prompt: str, max_length: int = 300, 
                       temperature: float = 0.85, top_p: float = 0.9) -> str:
        """
        Genera un cuento basado en el prompt.
        
        Args:
            prompt: Texto inicial o solicitud del usuario
            max_length: Longitud máxima del texto generado
            temperature: Controla la creatividad (0.1-1.5, mayor = más creativo)
            top_p: Nucleus sampling (0.1-1.0)
            
        Returns:
            Cuento generado
        """
        if not self.model or not self.tokenizer:
            raise RuntimeError("Modelo no está cargado")
        
        # Preparar prompt en español
        prompt_espanol = self._preparar_prompt(prompt)
        
        try:
            # Tokenizar
            inputs = self.tokenizer.encode(prompt_espanol, return_tensors="pt")
            
            # Mover a GPU si está disponible
            if self.usar_gpu:
                inputs = inputs.cuda()
            
            # Generar con parámetros optimizados
            with torch.no_grad():  # No calcular gradientes (más rápido)
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    min_length=100,  # Longitud mínima para asegurar cuento completo
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=True,  # Muestra aleatoria (más creativo)
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.3,  # Evitar repeticiones (aumentado)
                    length_penalty=1.2,  # Favorecer textos más largos
                    num_return_sequences=1,
                    no_repeat_ngram_size=3  # Evitar repetición de trigramas
                )
            
            # Decodificar
            texto_generado = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Limpiar y formatear
            cuento = self._limpiar_texto(texto_generado, prompt_espanol)
            
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
    
    def _preparar_prompt(self, prompt: str) -> str:
        """
        Prepara el prompt mejorado usando ejemplos de cuentos para guiar al modelo.
        Usa prompt engineering con few-shot learning.
        
        Args:
            prompt: Prompt original del usuario
            
        Returns:
            Prompt mejorado con ejemplos
        """
        # Detectar tema
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
        
        # Buscar marcadores comunes que indican inicio del cuento
        marcadores_inicio = ["cuento:", "cuento", "érase", "hace", "en un", "cuenta"]
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
        
        # Remover prefijos comunes que el modelo puede añadir
        prefijos_a_remover = [
            "el cuento es:", "el cuento:", "cuento:", 
            "aquí está el cuento:", "generado:"
        ]
        texto_lower = texto.lower()
        for prefijo in prefijos_a_remover:
            if texto_lower.startswith(prefijo):
                texto = texto[len(prefijo):].strip()
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

