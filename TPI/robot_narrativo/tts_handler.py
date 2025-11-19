"""
Módulo Text-to-Speech Handler
Maneja la conversión de texto a voz y la reproducción de audio.
"""

import os
import tempfile
from typing import Optional
from pathlib import Path


class TTSHandler:
    """
    Clase para manejar la síntesis de voz (Text-to-Speech).
    Soporta múltiples métodos: gTTS (online) y pyttsx3 (offline).
    """
    
    def __init__(self, metodo: str = "gtts", idioma: str = "es", 
                 velocidad: str = "normal", volumen: float = 0.9, 
                 tipo_voz: str = "femenina"):
        """
        Inicializa el manejador de TTS.
        
        Args:
            metodo: "gtts" para Google TTS (requiere internet) o "pyttsx3" para offline
            idioma: Código de idioma (por defecto "es" para español)
            velocidad: "lenta", "normal", o "rapida"
            volumen: Volumen de 0.0 a 1.0 (por defecto 0.9)
            tipo_voz: "femenina", "masculina", o "neutra" (solo para pyttsx3)
        """
        self.metodo = metodo
        self.idioma = idioma
        self.velocidad = velocidad
        self.volumen = max(0.0, min(1.0, volumen))  # Asegurar rango válido
        self.tipo_voz = tipo_voz
        self.temp_dir = Path(tempfile.gettempdir()) / "robot_narrativo_audio"
        self.temp_dir.mkdir(exist_ok=True)
    
    def _generar_audio_gtts(self, texto: str, output_path: str) -> bool:
        """
        Genera audio usando Google Text-to-Speech (gTTS).
        
        Args:
            texto: Texto a convertir a voz
            output_path: Ruta donde guardar el archivo de audio
            
        Returns:
            True si se generó correctamente, False en caso contrario
        """
        try:
            from gtts import gTTS
            import io
            
            # gTTS solo soporta slow (True/False), no tiene control fino de velocidad
            # Convertir nuestra velocidad a slow
            slow = self.velocidad == "lenta"
            
            tts = gTTS(text=texto, lang=self.idioma, slow=slow)
            tts.save(output_path)
            return True
        except Exception as e:
            print(f"Error con gTTS: {e}")
            return False
    
    def _generar_audio_pyttsx3(self, texto: str, output_path: str) -> bool:
        """
        Genera audio usando pyttsx3 (offline, requiere instalación de voces del sistema).
        
        Args:
            texto: Texto a convertir a voz
            output_path: Ruta donde guardar el archivo de audio
            
        Returns:
            True si se generó correctamente, False en caso contrario
        """
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            
            # Configurar propiedades de voz
            voices = engine.getProperty('voices')
            
            # Buscar voz según tipo solicitado y idioma
            voz_encontrada = False
            for voice in voices:
                nombre_voz = voice.name.lower()
                es_espanol = 'spanish' in nombre_voz or 'español' in nombre_voz or 'es-' in nombre_voz
                
                if es_espanol:
                    # Filtrar por tipo de voz si está disponible
                    if self.tipo_voz == "femenina":
                        if 'female' in nombre_voz or 'femenina' in nombre_voz or 'mujer' in nombre_voz:
                            engine.setProperty('voice', voice.id)
                            voz_encontrada = True
                            break
                    elif self.tipo_voz == "masculina":
                        if 'male' in nombre_voz or 'masculina' in nombre_voz or 'hombre' in nombre_voz:
                            engine.setProperty('voice', voice.id)
                            voz_encontrada = True
                            break
                    else:  # neutra o cualquier voz en español
                        if not voz_encontrada:
                            engine.setProperty('voice', voice.id)
                            voz_encontrada = True
            
            # Si no se encontró voz en español, usar la primera disponible
            if not voz_encontrada and voices:
                engine.setProperty('voice', voices[0].id)
            
            # Configurar velocidad según parámetro
            velocidades = {
                "lenta": 100,
                "normal": 150,
                "rapida": 200
            }
            rate = velocidades.get(self.velocidad, 150)
            engine.setProperty('rate', rate)
            
            # Configurar volumen
            engine.setProperty('volume', self.volumen)
            
            # Guardar en archivo
            engine.save_to_file(texto, output_path)
            engine.runAndWait()
            
            return os.path.exists(output_path)
        except Exception as e:
            print(f"Error con pyttsx3: {e}")
            return False
    
    def texto_a_audio(self, texto: str, guardar_archivo: bool = True) -> Optional[str]:
        """
        Convierte texto a audio y retorna la ruta del archivo.
        
        Args:
            texto: Texto a convertir
            guardar_archivo: Si True, guarda el archivo. Si False, solo reproduce
            
        Returns:
            Ruta del archivo de audio generado, o None si hay error
        """
        if not texto or len(texto.strip()) == 0:
            return None
        
        # Limpiar texto para mejor síntesis
        texto_limpio = self._limpiar_texto(texto)
        
        if guardar_archivo:
            # Generar nombre único para el archivo
            import hashlib
            hash_texto = hashlib.md5(texto_limpio.encode()).hexdigest()[:8]
            output_path = str(self.temp_dir / f"cuento_{hash_texto}.mp3")
        else:
            output_path = str(self.temp_dir / "cuento_temp.mp3")
        
        # Generar audio según el método seleccionado
        exito = False
        if self.metodo == "gtts":
            exito = self._generar_audio_gtts(texto_limpio, output_path)
        elif self.metodo == "pyttsx3":
            exito = self._generar_audio_pyttsx3(texto_limpio, output_path)
        
        if exito and os.path.exists(output_path):
            return output_path
        else:
            # Fallback: intentar con el otro método
            if self.metodo == "gtts":
                print("Intentando con pyttsx3 como fallback...")
                exito = self._generar_audio_pyttsx3(texto_limpio, output_path)
            else:
                print("Intentando con gTTS como fallback...")
                exito = self._generar_audio_gtts(texto_limpio, output_path)
            
            if exito and os.path.exists(output_path):
                return output_path
        
        return None
    
    def _limpiar_texto(self, texto: str) -> str:
        """
        Limpia el texto para mejorar la calidad de la síntesis de voz.
        
        Args:
            texto: Texto original
            
        Returns:
            Texto limpio
        """
        # Remover caracteres especiales problemáticos
        texto = texto.replace("\n\n", ". ")
        texto = texto.replace("\n", " ")
        
        # Asegurar puntos al final de oraciones
        if not texto.strip().endswith((".", "!", "?")):
            texto = texto.strip() + "."
        return texto
    
    def reproducir_audio(self, ruta_audio: str) -> bool:
        """
        Reproduce un archivo de audio.
        
        Args:
            ruta_audio: Ruta del archivo de audio
            
        Returns:
            True si se reprodujo correctamente, False en caso contrario
        """
        if not os.path.exists(ruta_audio):
            return False
        
        try:
            import platform
            sistema = platform.system()
            
            if sistema == "Windows":
                os.startfile(ruta_audio)
            elif sistema == "Darwin":  # macOS
                os.system(f"afplay '{ruta_audio}'")
            else:  # Linux
                os.system(f"aplay '{ruta_audio}'")
            
            return True
        except Exception as e:
            print(f"Error al reproducir audio: {e}")
            return False

