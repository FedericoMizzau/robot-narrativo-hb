# 🤖 Robot Narrativo Generativo

## Representación de la Habilidad Blanda: CREATIVIDAD

Sistema interactivo que demuestra creatividad mediante la generación de cuentos originales a partir de prompts del usuario. El robot recibe órdenes/peticiones en texto, procesa la información de manera creativa, genera un cuento completo con estructura narrativa, y lo narra mediante síntesis de voz.

---

## 🚀 Características

- **Generación Creativa:** Cada cuento es único, incluso con el mismo prompt
- **Estructura Narrativa:** Cuentos completos con introducción, desarrollo y desenlace
- **Text-to-Speech:** Narración automática de los cuentos generados
- **Interfaz Simple:** Fácil de usar, ideal para demostración
- **Flexible:** Funciona con o sin API de OpenAI

---

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

---

## 🔧 Instalación

1. **Clonar o descargar el proyecto:**
   ```bash
   cd robot_narrativo
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno (opcional):**
   ```bash
   cp .env.example .env
   ```
   
   Editar `.env` y agregar tu clave de API de OpenAI si deseas usar generación con IA:
   ```
   OPENAI_API_KEY=tu_clave_aqui
   ```

   **Nota:** Si no configuras la API de OpenAI, el sistema usará generación basada en plantillas creativas (funciona sin internet).

---

## 🎯 Uso

1. **Iniciar el servidor:**
   ```bash
   python app.py
   ```

2. **Abrir en el navegador:**
   ```
   http://localhost:5000
   ```

3. **Usar el robot:**
   - Ingresa un prompt o solicitud en el campo de texto
   - Ejemplo: "Un cuento sobre un robot que descubre la creatividad"
   - Haz clic en "Generar Cuento"
   - Espera a que se genere el cuento
   - Lee el cuento generado
   - Haz clic en "Escuchar Narración" para oír el cuento

---

## 🏗️ Arquitectura

```
robot_narrativo/
├── app.py                 # Aplicación Flask principal
├── generador_cuento.py    # Lógica de generación de cuentos
├── tts_handler.py         # Manejo de text-to-speech
├── templates/
│   └── index.html         # Interfaz web
├── static/
│   └── style.css          # Estilos CSS
├── requirements.txt       # Dependencias Python
└── README.md              # Este archivo
```

---

## 🧩 Componentes Principales

### 1. GeneradorCuento (`generador_cuento.py`)
- Genera cuentos creativos basados en prompts
- Soporta dos modos:
  - **Con OpenAI API:** Generación más sofisticada y variada
  - **Con plantillas:** Generación basada en plantillas creativas (sin internet)

### 2. TTSHandler (`tts_handler.py`)
- Convierte texto a voz
- Soporta dos métodos:
  - **gTTS (Google TTS):** Requiere internet, mejor calidad
  - **pyttsx3:** Funciona offline, requiere voces del sistema

### 3. Aplicación Flask (`app.py`)
- Servidor web que coordina todos los componentes
- Endpoints:
  - `/`: Interfaz principal
  - `/generar`: Genera un cuento
  - `/reproducir`: Reproduce el audio
  - `/health`: Verificación del sistema

---

## 🎨 Personalización

### Cambiar método de TTS

En `app.py`, línea 23:
```python
tts_handler = TTSHandler(metodo="pyttsx3", idioma="es")  # Para offline
```

### Ajustar creatividad

En `generador_cuento.py`, puedes modificar:
- Plantillas de introducción, desarrollo y desenlace
- Personajes, lugares y objetos disponibles
- Lógica de variabilidad

---

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
**Solución:** Instala las dependencias: `pip install -r requirements.txt`

### Error: "gTTS no funciona"
**Solución:** Verifica tu conexión a internet o cambia a `pyttsx3` en `app.py`

### Error: "pyttsx3 no tiene voz en español"
**Solución:** Instala voces en español en tu sistema operativo

### El audio no se reproduce
**Solución:** Verifica que el archivo de audio se genere correctamente en la carpeta temporal

---

## 📝 Notas para la Presentación

1. **Demostración (8 minutos):**
   - Mostrar la interfaz (1 min)
   - Generar un cuento con un prompt simple (2 min)
   - Explicar cómo funciona (2 min)
   - Generar otro cuento con prompt diferente (2 min)
   - Mostrar la narración (1 min)

2. **Puntos clave a destacar:**
   - Cada cuento es único (creatividad)
   - Estructura narrativa completa
   - Adaptación a diferentes prompts
   - Integración de múltiples tecnologías

---

## 📚 Referencias y Tecnologías

- **Flask:** Framework web para Python
- **OpenAI API:** Generación de texto con IA (opcional)
- **gTTS:** Google Text-to-Speech
- **pyttsx3:** Text-to-Speech offline

---

## 👥 Autores

Grupo de Trabajo Práctico - Habilidades Blandas
UTN FRC - Ingeniería en Sistemas de Información

---

## 📄 Licencia

Este proyecto es parte de un trabajo práctico académico.

