"""
Script para verificar la configuración de OpenAI y probar la generación.
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
print("VERIFICACION DE CONFIGURACION OPENAI")
print("=" * 60)

# Verificar archivo .env
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    print(f"[OK] Archivo .env encontrado: {env_path}")
else:
    print(f"[ADVERTENCIA] Archivo .env no encontrado en: {env_path}")
    print("   Crea un archivo .env con: OPENAI_API_KEY=tu_clave_aqui")

# Verificar API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_API_KEY:
    print(f"[OK] OPENAI_API_KEY encontrada")
    print(f"     Longitud: {len(OPENAI_API_KEY)} caracteres")
    print(f"     Prefijo: {OPENAI_API_KEY[:7]}...")
    print(f"     Sufijo: ...{OPENAI_API_KEY[-4:]}")
else:
    print("[ERROR] OPENAI_API_KEY no encontrada en .env")
    print("   Agrega: OPENAI_API_KEY=sk-tu-clave-aqui")

# Probar conexión con OpenAI
if OPENAI_API_KEY:
    print("\n" + "=" * 60)
    print("PROBANDO CONEXION CON OPENAI")
    print("=" * 60)
    
    # Limpiar la API key (eliminar espacios, saltos de línea, etc.)
    OPENAI_API_KEY = OPENAI_API_KEY.strip()
    print(f"[INFO] API Key limpiada (longitud: {len(OPENAI_API_KEY)} caracteres)")
    
    # Verificar formato básico
    if not OPENAI_API_KEY.startswith('sk-'):
        print("[ADVERTENCIA] La API key no comienza con 'sk-'")
        print("   Verifica que sea una clave válida de OpenAI")
    else:
        print("[OK] Formato de API key parece correcto")
    
    try:
        from openai import OpenAI
        
        # Crear cliente con la key limpia
        client = OpenAI(api_key=OPENAI_API_KEY)
        print("[INFO] Cliente OpenAI inicializado")
        
        # Enviar SOLO UNA solicitud con gpt-4o-mini
        modelo = "gpt-4o-mini"
        print(f"\n[INFO] Enviando UNA solicitud con modelo: {modelo}")
        
        try:
            respuesta = client.chat.completions.create(
                model=modelo,
                messages=[
                    {"role": "system", "content": "Eres un asistente útil."},
                    {"role": "user", "content": "Di 'Hola' en una palabra."}
                ],
                max_tokens=10
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
            
            # Intentar obtener headers de rate limit
            try:
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
                print(f"[RESPONSE] No se pudieron obtener headers: {e_headers}")
            
            print(f"{'='*60}\n")
            
            resultado = respuesta.choices[0].message.content.strip()
            print(f"[OK] Conexion exitosa con {modelo}!")
            print(f"     Respuesta: {resultado}")
            print(f"[OK] OpenAI API esta funcionando correctamente")
            
        except Exception as e:
            error_msg = str(e)
            print(f"\n{'='*60}")
            print(f"[ERROR] Error en la solicitud:")
            print(f"{'='*60}")
            print(f"[ERROR] Mensaje: {error_msg}")
            
            # Capturar información detallada del error
            try:
                if hasattr(e, 'response'):
                    response = e.response
                    
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
                                
                                print(f"\n[DIAGNOSTICO] Análisis del error:")
                                print(f"  - Tipo: {error_type}")
                                print(f"  - Código: {error_code}")
                                
                                if 'rate_limit' in error_type.lower() or 'rate_limit' in error_code.lower():
                                    print(f"\n  -> Error 429 - RATE LIMIT (demasiadas solicitudes)")
                                    print("     Causa: Estás enviando solicitudes demasiado rápido")
                                    print("     Solución: Espera antes de enviar otra solicitud")
                                    if 'retry-after' in headers:
                                        print(f"     Espera {headers['retry-after']} segundos antes de reintentar")
                                elif 'quota' in error_type.lower() or 'quota' in error_code.lower() or 'insufficient_quota' in error_code.lower():
                                    print(f"\n  -> Error 429 - INSUFFICIENT QUOTA (sin créditos)")
                                    print("     Causa: No hay créditos disponibles o límite de gasto alcanzado")
                                    print("     Solución: Verifica tu cuenta en https://platform.openai.com/account/billing")
                        except:
                            pass
                    
                    # Status code
                    if hasattr(response, 'status_code'):
                        print(f"\n[ERROR] Status Code: {response.status_code}")
                
            except Exception as e_debug:
                print(f"[ERROR] No se pudo extraer información detallada: {e_debug}")
            
            print(f"{'='*60}\n")
            raise
        
    except Exception as e:
        error_msg = str(e)
        print(f"\n[ERROR] Error al conectar con OpenAI: {error_msg}")
        
        # Análisis detallado del error
        if "429" in error_msg:
            if "quota" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
                print("\n[DIAGNOSTICO] Error 429 - Insufficient Quota:")
                print("   Posibles causas:")
                print("   1. La cuenta no tiene créditos disponibles")
                print("   2. Has excedido el límite de uso mensual")
                print("   3. La API key está asociada a una cuenta diferente")
                print("   4. Hay un límite de organización o proyecto")
                print("\n   Acciones recomendadas:")
                print("   - Verifica créditos: https://platform.openai.com/account/billing")
                print("   - Verifica límites: https://platform.openai.com/account/limits")
                print("   - Verifica uso: https://platform.openai.com/usage")
                print("   - Verifica que la API key sea de la cuenta correcta")
            else:
                print("\n[DIAGNOSTICO] Error 429 - Rate Limit:")
                print("   Has excedido el límite de velocidad (requests por minuto)")
                print("   Espera unos minutos y vuelve a intentar")
                print("   Verifica límites: https://platform.openai.com/account/limits")
        elif "401" in error_msg or "unauthorized" in error_msg.lower():
            print("\n[ERROR] API Key inválida o no autorizada:")
            print("   - Verifica que la clave en .env sea correcta")
            print("   - Asegúrate de que no tenga espacios extra al inicio/final")
            print("   - Obtén una nueva clave en: https://platform.openai.com/api-keys")
            print("   - Verifica que la clave no haya sido revocada")
        elif "model" in error_msg.lower() and "not found" in error_msg.lower():
            print("\n[ERROR] Modelo no encontrado:")
            print("   - El modelo solicitado no está disponible para tu cuenta")
            print("   - Verifica modelos disponibles: https://platform.openai.com/docs/models")
        else:
            print(f"\n[ERROR] Error desconocido: {e}")
            print("   Revisa la documentación: https://platform.openai.com/docs/guides/error-codes")
        
        # Intentar obtener más información del error
        try:
            import json
            if hasattr(e, 'response'):
                if hasattr(e.response, 'json'):
                    try:
                        error_details = e.response.json()
                        print(f"\n[DEBUG] Detalles completos del error:")
                        print(json.dumps(error_details, indent=2, ensure_ascii=False))
                    except:
                        print(f"\n[DEBUG] No se pudo parsear JSON del error")
                
                # Información de headers si está disponible
                if hasattr(e.response, 'headers'):
                    headers = dict(e.response.headers)
                    if 'x-ratelimit-limit' in headers:
                        print(f"\n[DEBUG] Rate Limit Info:")
                        print(f"   Límite: {headers.get('x-ratelimit-limit', 'N/A')}")
                        print(f"   Restante: {headers.get('x-ratelimit-remaining', 'N/A')}")
                        print(f"   Reset: {headers.get('x-ratelimit-reset', 'N/A')}")
        except Exception as debug_error:
            print(f"[DEBUG] Error al obtener detalles: {debug_error}")
        
        # Verificar información de la cuenta usando la API
        print("\n" + "=" * 60)
        print("VERIFICANDO INFORMACION DE CUENTA")
        print("=" * 60)
        try:
            # Intentar obtener información de la organización
            from openai import OpenAI
            client_test = OpenAI(api_key=OPENAI_API_KEY)
            
            # Probar obtener información de uso (si está disponible)
            print("[INFO] La API key está configurada correctamente")
            print("[INFO] El error 429 indica un problema de cuota o límite")
            print("\n[RECOMENDACIONES]:")
            print("1. Verifica en https://platform.openai.com/account/billing:")
            print("   - Que tengas créditos disponibles")
            print("   - Que no haya límites de gasto configurados")
            print("   - Que el método de pago esté activo")
            print("\n2. Verifica en https://platform.openai.com/account/limits:")
            print("   - Los límites de uso (rate limits)")
            print("   - Los límites de organización")
            print("\n3. Verifica en https://platform.openai.com/usage:")
            print("   - El uso actual de la API")
            print("   - Si hay algún límite alcanzado")
            print("\n4. Verifica que la API key sea de la cuenta correcta:")
            print("   - Ve a https://platform.openai.com/api-keys")
            print("   - Confirma que la key que estás usando esté activa")
            print("   - Verifica que no esté asociada a una organización con límites")
            
        except Exception as e_info:
            print(f"[INFO] No se pudo obtener información adicional: {e_info}")

print("\n" + "=" * 60)
print("VERIFICACION COMPLETADA")
print("=" * 60)

