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
# Configuración: usar OpenAI API si está disponible, sino usar plantillas
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
usar_openai = OPENAI_API_KEY is not None and len(OPENAI_API_KEY.strip()) > 0

# Configurar generador: Prioridad ML > OpenAI > Plantillas
# Cambiar usar_ml=True para activar GPT-2
generador = GeneradorCuento(
    usar_api_openai=usar_openai, 
    api_key=OPENAI_API_KEY,
    usar_ml=True,  # Activar modelo ML (GPT-2)
    modelo_ml="gpt2"  # Puedes cambiar a "distilgpt2" para versión más rápida
)

# Intentar usar gTTS, si no está disponible usar pyttsx3
try:
    from gtts import gTTS
    metodo_tts = "gtts"
except ImportError:
    metodo_tts = "pyttsx3"
    print("⚠️  gTTS no disponible, usando pyttsx3 (offline)")

tts_handler = TTSHandler(metodo=metodo_tts, idioma="es")


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
        
        if not prompt:
            return jsonify({
                'error': 'Por favor, ingresa un prompt o solicitud.'
            }), 400
        
        # Generar cuento
        cuento = generador.generar_cuento(prompt)
        
        # Validar estructura
        if not generador.validar_estructura_cuento(cuento):
            return jsonify({
                'error': 'No se pudo generar un cuento con estructura válida. Intenta con otro prompt.'
            }), 500
        
        # Generar audio
        ruta_audio = tts_handler.texto_a_audio(cuento, guardar_archivo=True)
        
        respuesta = {
            'cuento': cuento,
            'prompt': prompt,
            'audio_generado': ruta_audio is not None,
        }
        
        if ruta_audio:
            respuesta['audio_path'] = ruta_audio
        
        return jsonify(respuesta), 200
        
    except Exception as e:
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
    print("🤖 ROBOT NARRATIVO GENERATIVO - Iniciando...")
    print("=" * 60)
    print(f"📝 Generador: {'OpenAI API' if usar_openai else 'Plantillas creativas'}")
    print(f"🔊 TTS: {tts_handler.metodo.upper()}")
    print("=" * 60)
    print("\n🌐 Servidor disponible en: http://localhost:5000")
    print("📖 Abre tu navegador y navega a la URL anterior\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

