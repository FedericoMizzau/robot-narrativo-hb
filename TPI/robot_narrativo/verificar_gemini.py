"""
Script para verificar la configuración de Gemini y probar la generación.
"""

import sys
import io
import os
from dotenv import load_dotenv

# Configurar encoding para Windows
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

# Cargar variables de entorno
load_dotenv()

print("=" * 60)
print("VERIFICACION DE CONFIGURACION GEMINI")
print("=" * 60)

# Verificar archivo .env
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    print(f"[OK] Archivo .env encontrado: {env_path}")
else:
    print(f"[ADVERTENCIA] Archivo .env no encontrado en: {env_path}")
    print("   Crea un archivo .env con: GEMINI_API_KEY=tu_clave_aqui")

# Verificar API Key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    print(f"[OK] GEMINI_API_KEY encontrada")
    print(f"     Longitud: {len(GEMINI_API_KEY)} caracteres")
    print(f"     Prefijo: {GEMINI_API_KEY[:7]}...")
    print(f"     Sufijo: ...{GEMINI_API_KEY[-4:]}")
else:
    print("[ERROR] GEMINI_API_KEY no encontrada en .env")
    print("   Agrega: GEMINI_API_KEY=tu-clave-aqui")
    print("\n   Para obtener una API key:")
    print("   1. Ve a https://makersuite.google.com/app/apikey")
    print("   2. Crea una nueva API key")
    print("   3. Copia la clave y agrégala al archivo .env")

# Probar conexión con Gemini
if GEMINI_API_KEY:
    print("\n" + "=" * 60)
    print("PROBANDO CONEXION CON GEMINI")
    print("=" * 60)
    
    # Limpiar la API key (eliminar espacios, saltos de línea, etc.)
    GEMINI_API_KEY = GEMINI_API_KEY.strip()
    print(f"[INFO] API Key limpiada (longitud: {len(GEMINI_API_KEY)} caracteres)")
    
    try:
        import google.generativeai as genai
        
        # Configurar la API key
        genai.configure(api_key=GEMINI_API_KEY)
        print("[INFO] Cliente Gemini inicializado")
        
        # Enviar SOLO UNA solicitud con gemini-2.5-flash
        modelo_nombre = "gemini-2.5-flash"
        print(f"\n[INFO] Enviando UNA solicitud con modelo: {modelo_nombre}")
        
        try:
            modelo = genai.GenerativeModel(modelo_nombre)
            respuesta = modelo.generate_content(
                "Di 'Hola' en una palabra.",
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=50
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
            
            print(f"{'='*60}\n")
            
            # Verificar candidatos y finish_reason
            if respuesta.candidates:
                candidato = respuesta.candidates[0]
                finish_reason = candidato.finish_reason
                
                if finish_reason == 1:  # STOP (éxito)
                    if respuesta.text:
                        resultado = respuesta.text.strip()
                        print(f"[OK] Conexion exitosa con {modelo_nombre}!")
                        print(f"     Respuesta: {resultado}")
                        print(f"[OK] Gemini API esta funcionando correctamente")
                    else:
                        print("[ADVERTENCIA] Gemini no generó contenido de texto")
                else:
                    finish_reasons = {
                        0: "FINISH_REASON_UNSPECIFIED",
                        1: "STOP",
                        2: "MAX_TOKENS",
                        3: "SAFETY (bloqueado por seguridad)",
                        4: "RECITATION",
                        5: "OTHER"
                    }
                    razon = finish_reasons.get(finish_reason, f"UNKNOWN({finish_reason})")
                    print(f"[ADVERTENCIA] Generación bloqueada. Finish reason: {razon}")
                    if finish_reason == 3:
                        print("   El contenido fue bloqueado por filtros de seguridad de Gemini")
                        print("   Esto es normal para algunos prompts, prueba con otro texto")
            else:
                print("[ADVERTENCIA] Gemini no generó candidatos")
                
        except Exception as e:
            error_msg = str(e)
            print(f"\n{'='*60}")
            print(f"[ERROR] Error en la solicitud:")
            print(f"{'='*60}")
            print(f"[ERROR] Mensaje: {error_msg}")
            
            # Intentar extraer más información del error
            try:
                if hasattr(e, 'response'):
                    response = e.response
                    print(f"[ERROR] Status Code: {getattr(response, 'status_code', 'N/A')}")
            except:
                pass
            
            print(f"{'='*60}\n")
            raise
        
    except ImportError:
        print("\n[ERROR] google-generativeai no está instalado")
        print("   Instala con: pip install google-generativeai")
        print("   O ejecuta: pip install -r requirements.txt")
    except Exception as e:
        error_msg = str(e)
        print(f"\n[ERROR] Error al conectar con Gemini: {error_msg}")
        
        # Diagnóstico de errores comunes
        if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower():
            print("\n[DIAGNOSTICO] API Key inválida:")
            print("   - Verifica que la clave sea correcta")
            print("   - Asegúrate de que no tenga espacios al inicio o final")
            print("   - Obtén una nueva clave en: https://makersuite.google.com/app/apikey")
        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
            print("\n[DIAGNOSTICO] Límite de cuota alcanzado:")
            print("   - Verifica tu uso en: https://makersuite.google.com/")
            print("   - Gemini tiene límites de uso gratuito")
        elif "permission" in error_msg.lower() or "forbidden" in error_msg.lower():
            print("\n[DIAGNOSTICO] Permisos insuficientes:")
            print("   - Verifica que la API key tenga los permisos correctos")
            print("   - Asegúrate de que la API esté habilitada en tu cuenta")
        
        print("\n[DEBUG] Detalles completos del error:")
        import traceback
        traceback.print_exc()
        
        print("\n" + "=" * 60)
        print("VERIFICANDO INFORMACION DE CUENTA")
        print("=" * 60)
        print("[INFO] La API key está configurada correctamente")
        print("[INFO] El error puede indicar un problema de configuración o cuota")
        
        print("\n[RECOMENDACIONES]:")
        print("1. Verifica en https://makersuite.google.com/app/apikey:")
        print("   - Que la API key sea válida")
        print("   - Que no haya expirado")
        print("   - Que tengas permisos para usarla")
        print("2. Verifica límites de uso:")
        print("   - Gemini tiene límites de uso gratuito")
        print("   - Revisa tu cuota en: https://makersuite.google.com/")
        print("3. Prueba crear una nueva API key si el problema persiste")
        
else:
    print("\n[INFO] No se puede probar la conexión sin una API key")
    print("   Agrega GEMINI_API_KEY a tu archivo .env")

print("\n" + "=" * 60)
print("FIN DE VERIFICACION")
print("=" * 60)

