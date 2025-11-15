# RESUMEN DEL PROYECTO
## Robot Narrativo Generativo - Creatividad

---

## 📋 INFORMACIÓN GENERAL

- **Habilidad Blanda:** Creatividad
- **Nombre del Robot:** Narratron (Robot Narrativo Generativo)
- **Tipo:** Prototipo Digital (aplicación web)
- **Fecha de Entrega:** Jueves 20 de noviembre de 2025

---

## 🎯 OBJETIVO

Demostrar la habilidad blanda de **creatividad** mediante un sistema que genera cuentos originales a partir de prompts del usuario, mostrando capacidad de:
- Generar ideas originales
- Pensamiento divergente
- Combinación innovadora de elementos
- Elaboración de ideas en productos completos
- Adaptabilidad a diferentes contextos

---

## 🏗️ ARQUITECTURA DEL SISTEMA

```
Usuario → Interfaz Web → Generador de Cuento → Validador → TTS → Audio
```

### Componentes:

1. **Interfaz Web (HTML/CSS/JavaScript)**
   - Captura de prompts del usuario
   - Visualización de resultados
   - Control de reproducción de audio

2. **Generador de Cuento (Python)**
   - Procesamiento de prompts
   - Generación de narrativas creativas
   - Dos modos: OpenAI API o plantillas creativas

3. **Sistema TTS (Text-to-Speech)**
   - Conversión de texto a voz
   - Dos métodos: gTTS (online) o pyttsx3 (offline)

4. **Servidor Flask**
   - Coordinación de componentes
   - API REST para comunicación

---

## 🚀 INSTALACIÓN Y USO RÁPIDO

### Requisitos Previos:
- Python 3.8+
- pip (gestor de paquetes)

### Pasos:

1. **Instalar dependencias:**
   ```bash
   cd robot_narrativo
   pip install -r requirements.txt
   ```

2. **Configurar (opcional):**
   - Crear archivo `.env` con `OPENAI_API_KEY=tu_clave` (si quieres usar OpenAI)
   - Si no, el sistema funcionará con plantillas creativas

3. **Ejecutar:**
   ```bash
   python app.py
   ```

4. **Abrir navegador:**
   ```
   http://localhost:5000
   ```

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
robot_narrativo/
├── app.py                      # Aplicación Flask principal
├── generador_cuento.py         # Lógica de generación
├── tts_handler.py              # Manejo de text-to-speech
├── requirements.txt            # Dependencias
├── README.md                   # Documentación técnica
├── templates/
│   └── index.html              # Interfaz web
└── static/
    └── style.css               # Estilos CSS

Documentación/
├── 01_Planificacion_Robot_Narrativo.md    # Planificación completa
├── 02_Justificacion_Conceptual.md         # Justificación para informe
└── 03_Resumen_Proyecto.md                 # Este archivo
```

---

## 🎨 CARACTERÍSTICAS PRINCIPALES

### Funcionalidades:

✅ **Generación Creativa:** Cada cuento es único  
✅ **Estructura Narrativa:** Introducción, desarrollo, desenlace  
✅ **Text-to-Speech:** Narración automática  
✅ **Interfaz Simple:** Fácil de usar y demostrar  
✅ **Flexible:** Funciona con o sin API externa  

### Elementos de Creatividad Demostrados:

- **Originalidad:** Contenido único en cada generación
- **Variabilidad:** Mismo prompt → diferentes resultados
- **Combinación:** Mezcla elementos del prompt con elementos creativos
- **Elaboración:** Desarrolla ideas en narrativas completas
- **Adaptabilidad:** Se ajusta a diferentes tipos de prompts

---

## 📝 PARA LA PRESENTACIÓN (8 minutos)

### Estructura Sugerida:

1. **Introducción (1 min)**
   - Presentar el robot y su propósito
   - Explicar la habilidad blanda (Creatividad)

2. **Demostración (3 min)**
   - Mostrar la interfaz
   - Generar un cuento con un prompt simple
   - Mostrar que es único (generar otro con mismo prompt)

3. **Explicación Técnica (2 min)**
   - Cómo funciona el sistema
   - Componentes principales
   - Elementos de creatividad representados

4. **Demostración Avanzada (1 min)**
   - Generar cuento con prompt diferente
   - Mostrar la narración de voz

5. **Cierre (1 min)**
   - Resumen de cómo representa la creatividad
   - Reflexión sobre la importancia de la habilidad

---

## 📊 CRITERIOS DE EVALUACIÓN

### Comprensión Conceptual (25%)
- ✅ Definición clara de creatividad
- ✅ Componentes identificados
- ✅ Relevancia explicada

### Coherencia Diseño-Habilidad (25%)
- ✅ Correspondencia entre características del robot y creatividad
- ✅ Elementos observables de la habilidad
- ✅ Justificación del diseño

### Creatividad y Originalidad (15%)
- ✅ Innovación en la idea
- ✅ Presentación creativa

### Trabajo en Equipo (20%)
- ✅ Participación equilibrada
- ✅ Organización y cumplimiento de plazos

### Comunicación (15%)
- ✅ Claridad en presentación
- ✅ Informe bien estructurado

---

## 📚 DOCUMENTOS PARA EL INFORME

El informe debe incluir (2-3 páginas):

1. **Definición de la habilidad blanda**
   - Usar contenido de `02_Justificacion_Conceptual.md` sección 1

2. **Descripción del robot**
   - Usar contenido de `02_Justificacion_Conceptual.md` sección 2

3. **Justificación del diseño**
   - Usar contenido de `02_Justificacion_Conceptual.md` sección 3

4. **Reflexión grupal**
   - Usar contenido de `02_Justificacion_Conceptual.md` sección 4

---

## 🔧 CONFIGURACIÓN AVANZADA

### Usar OpenAI API (mejor calidad):

1. Obtener clave de API en: https://platform.openai.com/
2. Crear archivo `.env`:
   ```
   OPENAI_API_KEY=sk-tu-clave-aqui
   ```
3. El sistema usará automáticamente la API

### Usar TTS Offline:

En `app.py`, línea 23, cambiar:
```python
tts_handler = TTSHandler(metodo="pyttsx3", idioma="es")
```

**Nota:** Requiere instalar voces en español en el sistema operativo.

---

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### Error: "ModuleNotFoundError"
**Solución:** `pip install -r requirements.txt`

### Error: "gTTS no funciona"
**Solución:** Verificar conexión a internet o cambiar a pyttsx3

### El audio no se reproduce
**Solución:** Verificar que el archivo se genere en la carpeta temporal

### OpenAI API no funciona
**Solución:** Verificar la clave en `.env` o usar modo plantillas (sin API)

---

## 📞 PRÓXIMOS PASOS

1. ✅ Planificación completada
2. ✅ Prototipo funcional creado
3. ⏳ Probar el sistema completamente
4. ⏳ Preparar presentación (PPT/video)
5. ⏳ Redactar informe final (usar `02_Justificacion_Conceptual.md`)
6. ⏳ Ensayar presentación (8 minutos)

---

## 📖 REFERENCIAS

- **Flask Documentation:** https://flask.palletsprojects.com/
- **OpenAI API:** https://platform.openai.com/docs
- **gTTS:** https://gtts.readthedocs.io/
- **pyttsx3:** https://pyttsx3.readthedocs.io/

---

**¡Éxito con el proyecto! 🚀**

