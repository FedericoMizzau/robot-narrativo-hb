"""
Módulo de traducción para mejorar la generación de cuentos.
Traduce prompts de español a inglés para mejor generación con GPT-2,
y luego traduce los cuentos generados de vuelta a español.
"""

import sys
import io

# Configurar encoding para Windows
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass


class Traductor:
    """
    Clase para manejar traducciones español <-> inglés.
    Usa deep-translator como primera opción, con fallback a googletrans.
    """
    
    def __init__(self):
        """Inicializa el traductor con la mejor librería disponible."""
        self.traductor_activo = None
        self.metodo = None
        self._inicializar_traductor()
    
    def _inicializar_traductor(self):
        """Intenta cargar una librería de traducción disponible."""
        # Intentar deep-translator primero (más robusto)
        try:
            from deep_translator import GoogleTranslator
            self.traductor_activo = GoogleTranslator
            self.metodo = "deep-translator"
            print("[OK] Traductor inicializado: deep-translator")
            return
        except ImportError:
            pass
        
        # Fallback a googletrans
        try:
            from googletrans import Translator
            self.traductor_activo = Translator()
            self.metodo = "googletrans"
            print("[OK] Traductor inicializado: googletrans")
            return
        except ImportError:
            pass
        
        # Si no hay traductor disponible
        print("[ADVERTENCIA] No se encontro libreria de traduccion")
        print("   Instala una de estas opciones:")
        print("   - pip install deep-translator (recomendado)")
        print("   - pip install googletrans==4.0.0rc1")
        self.traductor_activo = None
        self.metodo = None
    
    def traducir_a_ingles(self, texto: str) -> str:
        """
        Traduce texto de español a inglés.
        
        Args:
            texto: Texto en español
            
        Returns:
            Texto traducido a inglés, o el texto original si falla
        """
        if not self.traductor_activo or not texto:
            return texto
        
        try:
            if self.metodo == "deep-translator":
                traductor = self.traductor_activo(source='es', target='en')
                resultado = traductor.translate(texto)
                print(f"[INFO] Prompt traducido a ingles ({len(resultado)} caracteres)")
                return resultado
            elif self.metodo == "googletrans":
                resultado = self.traductor_activo.translate(texto, src='es', dest='en')
                print(f"[INFO] Prompt traducido a ingles ({len(resultado.text)} caracteres)")
                return resultado.text
        except Exception as e:
            print(f"[ADVERTENCIA] Error al traducir a ingles: {e}")
            print("   Usando texto original")
            return texto
        
        return texto
    
    def traducir_a_espanol(self, texto: str) -> str:
        """
        Traduce texto de inglés a español.
        
        Args:
            texto: Texto en inglés
            
        Returns:
            Texto traducido a español, o el texto original si falla
        """
        if not self.traductor_activo or not texto:
            return texto
        
        try:
            if self.metodo == "deep-translator":
                traductor = self.traductor_activo(source='en', target='es')
                resultado = traductor.translate(texto)
                print(f"[INFO] Cuento traducido a espanol ({len(resultado)} caracteres)")
                return resultado
            elif self.metodo == "googletrans":
                resultado = self.traductor_activo.translate(texto, src='en', dest='es')
                print(f"[INFO] Cuento traducido a espanol ({len(resultado.text)} caracteres)")
                return resultado.text
        except Exception as e:
            print(f"[ADVERTENCIA] Error al traducir a espanol: {e}")
            print("   Usando texto original")
            return texto
        
        return texto
    
    def esta_disponible(self) -> bool:
        """Verifica si el traductor está disponible."""
        return self.traductor_activo is not None


# Instancia global del traductor
_traductor_instancia = None

def obtener_traductor() -> Traductor:
    """Obtiene la instancia global del traductor."""
    global _traductor_instancia
    if _traductor_instancia is None:
        _traductor_instancia = Traductor()
    return _traductor_instancia

