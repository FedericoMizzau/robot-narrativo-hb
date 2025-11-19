"""
Aplicación Principal del Robot Narrativo Generativo
Sistema que demuestra creatividad mediante la generación y narración de cuentos.
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from generador_cuento import GeneradorCuento
from tts_handler import TTSHandler

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'robot-narrativo-secret-key')

# Inicializar componentes
# Configuración: Prioridad OpenAI > ML > Plantillas

# Verificar OpenAI API (prioridad 1)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_API_KEY:
    OPENAI_API_KEY = OPENAI_API_KEY.strip()
usar_openai = OPENAI_API_KEY is not None and len(OPENAI_API_KEY) > 0

# Gemini desactivado (API key removida)
usar_gemini = False
GEMINI_API_KEY = None

# Configurar generador: Prioridad OpenAI > ML > Plantillas
modelo_entrenado_path = "./modelo_cuentos_entrenado"
usar_modelo_entrenado = False  # Desactivado temporalmente para mejor calidad

# Verificar estado de APIs
if usar_openai:
    print("=" * 60)
    print("[OK] OpenAI API configurada - Se usara gpt-4o-mini (principal)")
    print(f"[INFO] API Key: {'*' * 20}...{OPENAI_API_KEY[-4:] if len(OPENAI_API_KEY) > 4 else '****'}")
    print("     Prioridad: OpenAI > ML > Plantillas")
    print("=" * 60)
else:
    print("[INFO] OpenAI API no configurada - Se usara modelo ML o plantillas")

generador = GeneradorCuento(
    usar_api_gemini=False,  # Gemini desactivado
    gemini_api_key=None,
    usar_api_openai=usar_openai, 
    api_key=OPENAI_API_KEY,
    usar_ml=not usar_openai,  # Solo usar ML si no hay OpenAI disponible
    modelo_ml="gpt2" if not usar_modelo_entrenado else modelo_entrenado_path
)

# Intentar usar gTTS, si no está disponible usar pyttsx3
try:
    from gtts import gTTS
    metodo_tts = "gtts"
except ImportError:
    metodo_tts = "pyttsx3"
    print("⚠️  gTTS no disponible, usando pyttsx3 (offline)")

# Configuración de TTS (puedes ajustar estos valores)
tts_handler = TTSHandler(
    metodo=metodo_tts, 
    idioma="es",
    velocidad="normal",  # Opciones: "lenta", "normal", "rapida"
    volumen=0.9,  # Rango: 0.0 a 1.0
    tipo_voz="masculina"  # Opciones: "femenina", "masculina", "neutra" (solo pyttsx3)
)


@app.route('/')
def index():
    """Página principal con la interfaz del robot."""
    return render_template('index.html')


@app.route('/generar', methods=['POST'])
def generar_cuento():
    """
    Endpoint para generar un cuento basado en el prompt del usuario.
    
    Returns:
        JSON con el cuento generado y la ruta del audio (si se generó)
    """
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        duracion = data.get('duracion', 'medio').strip().lower()
        
        # Validar duración
        duraciones_validas = ['corto', 'medio', 'largo']
        if duracion not in duraciones_validas:
            duracion = 'medio'  # Valor por defecto
        
        if not prompt:
            return jsonify({
                'error': 'Por favor, ingresa un prompt o solicitud.'
            }), 400
        
        # Generar cuento (sin truncar el prompt)
        try:
            cuento = generador.generar_cuento(prompt, duracion)
        except Exception as gen_error:
            print(f"[ERROR] Error en generación: {gen_error}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': f'Error al generar el cuento: {str(gen_error)}. Intenta con un prompt más corto o diferente.'
            }), 500
        
        # Validar que el cuento tenga contenido válido
        if not cuento or len(cuento.strip()) < 50:
            return jsonify({
                'error': 'El cuento generado es muy corto o está vacío. Intenta con otro prompt.'
            }), 500
        
        # Validar estructura (más flexible)
        if not generador.validar_estructura_cuento(cuento):
            # Si no pasa la validación pero tiene contenido, permitirlo de todas formas
            print(f"[ADVERTENCIA] Cuento no pasó validación estricta, pero se permite: {len(cuento)} caracteres")
        
        # Generar audio
        try:
            ruta_audio = tts_handler.texto_a_audio(cuento, guardar_archivo=True)
        except Exception as tts_error:
            print(f"[ERROR] Error en TTS: {tts_error}")
            ruta_audio = None
        
        respuesta = {
            'cuento': cuento,
            'prompt': prompt,
            'duracion': duracion,
            'audio_generado': ruta_audio is not None,
        }
        
        if ruta_audio:
            respuesta['audio_path'] = ruta_audio
        
        return jsonify(respuesta), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[ERROR] Error completo: {error_trace}")
        return jsonify({
            'error': f'Error al generar el cuento: {str(e)}'
        }), 500


@app.route('/reproducir', methods=['POST'])
def reproducir_audio():
    """
    Endpoint para reproducir el audio del cuento.
    
    Returns:
        JSON con el estado de la reproducción
    """
    try:
        data = request.get_json()
        ruta_audio = data.get('audio_path', '')
        
        if not ruta_audio or not os.path.exists(ruta_audio):
            return jsonify({
                'error': 'Archivo de audio no encontrado.'
            }), 404
        
        exito = tts_handler.reproducir_audio(ruta_audio)
        
        if exito:
            return jsonify({
                'mensaje': 'Audio reproducido correctamente.',
                'audio_path': ruta_audio
            }), 200
        else:
            return jsonify({
                'error': 'No se pudo reproducir el audio.'
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': f'Error al reproducir audio: {str(e)}'
        }), 500


@app.route('/static/audio/<filename>')
def servir_audio(filename):
    """
    Sirve archivos de audio desde el directorio temporal.
    """
    from flask import send_from_directory
    return send_from_directory(tts_handler.temp_dir, filename)


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificación de salud del sistema."""
    return jsonify({
        'status': 'ok',
        'generador': 'activo',
        'tts': 'activo',
        'openai_habilitado': usar_openai
    }), 200


if __name__ == '__main__':
    print("=" * 60)
    print("ROBOT NARRATIVO GENERATIVO - Iniciando...")
    print("=" * 60)
    
    # Mostrar configuración del generador
    if usar_openai:
        print(f"[OK] Generador: OpenAI API (gpt-4o-mini)")
        print(f"     Prioridad: OpenAI > ML > Plantillas")
    elif usar_modelo_entrenado:
        print(f"[INFO] Generador: Modelo ML Entrenado ({modelo_entrenado_path})")
        print(f"     Prioridad: ML > Plantillas")
    else:
        print(f"[INFO] Generador: Modelo ML Base (GPT-2)")
        print(f"     Prioridad: ML > Plantillas")
    
    print(f"[OK] TTS: {tts_handler.metodo.upper()}")
    print("=" * 60)
    print("\n[INFO] Servidor disponible en: http://localhost:5000")
    print("[INFO] Abre tu navegador y navega a la URL anterior")
    print("[INFO] Los prompts y metodos usados se mostraran en la consola\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

