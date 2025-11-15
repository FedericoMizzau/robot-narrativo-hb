# PLANIFICACIÓN: ROBOT NARRATIVO GENERATIVO
## Representación de la Habilidad Blanda: CREATIVIDAD

---

## PASO 1: DEFINICIÓN DE LA IDEA ESPECÍFICA Y ALCANCE TÉCNICO

### 1.1 Concepto General

**Nombre del Robot:** "Narratron" o "Cuentista Creativo"

**Descripción:**
Un sistema interactivo que demuestra creatividad mediante la generación de cuentos originales a partir de prompts del usuario. El robot recibe órdenes/peticiones en texto, procesa la información de manera creativa, genera un cuento completo con estructura narrativa (inicio, desarrollo, desenlace), y lo narra mediante síntesis de voz.

### 1.2 Características de la Creatividad Representadas

1. **Generación de ideas originales:** Cada cuento es único, incluso con el mismo prompt
2. **Pensamiento divergente:** Múltiples interpretaciones posibles de un mismo input
3. **Combinación innovadora:** Mezcla elementos del prompt con elementos creativos propios
4. **Producción de contenido estructurado:** Crea narrativas completas con coherencia
5. **Adaptabilidad:** Se ajusta a diferentes tipos de solicitudes

### 1.3 Alcance Técnico

#### Componentes Principales:

1. **Interfaz de Entrada:**
   - Campo de texto simple para recibir prompts
   - Botón de "Generar cuento"
   - Indicador visual de procesamiento

2. **Motor de Generación:**
   - Procesamiento del prompt (análisis de palabras clave, intención)
   - Generación de cuento con estructura narrativa:
     - Introducción/Contexto
     - Desarrollo/Conflicto
     - Desenlace/Resolución
   - Longitud: 150-300 palabras (aprox. 1-2 minutos de narración)

3. **Sistema de Text-to-Speech (TTS):**
   - Conversión del texto generado a audio
   - Voz natural y expresiva
   - Reproducción mediante altavoz/auriculares

4. **Interfaz Visual (Opcional pero recomendado):**
   - Display del cuento generado
   - Indicadores de estado (procesando, generando, narrando)
   - Posible visualización de elementos creativos

#### Tecnologías Sugeridas:

**Opción A - Implementación Web (Recomendada para prototipo rápido):**
- Frontend: HTML/CSS/JavaScript (interfaz simple)
- Backend: Python (Flask/FastAPI)
- Generación: OpenAI API o modelo local (GPT-2, GPT-3.5-turbo, o similar)
- TTS: Google Text-to-Speech (gTTS) o pyttsx3 (offline)
- Despliegue: Local o servidor simple

**Opción B - Implementación Desktop:**
- Framework: Python con Tkinter o PyQt
- Generación: API de OpenAI o modelo local
- TTS: pyttsx3 o gTTS

**Opción C - Implementación con Hardware (Más "robótica"):**
- Microcontrolador: Raspberry Pi
- Display: Pantalla LCD o e-ink
- Audio: Altavoz USB o salida de audio
- Interfaz: Teclado físico o pantalla táctil

### 1.4 Requisitos Funcionales

1. **RF-1:** El sistema debe recibir texto de entrada (prompt) del usuario
2. **RF-2:** El sistema debe generar un cuento original basado en el prompt
3. **RF-3:** El cuento generado debe tener estructura narrativa completa
4. **RF-4:** El sistema debe narrar el cuento mediante síntesis de voz
5. **RF-5:** El sistema debe mostrar el cuento generado en texto
6. **RF-6:** El sistema debe manejar diferentes tipos de prompts (órdenes, peticiones, temas)

### 1.5 Requisitos No Funcionales

1. **RNF-1:** Tiempo de generación: < 30 segundos
2. **RNF-2:** Calidad de voz: Comprensible y natural
3. **RNF-3:** Interfaz: Simple e intuitiva
4. **RNF-4:** Robustez: Manejo de errores y casos límite

### 1.6 Limitaciones y Consideraciones

- **Presupuesto:** Considerar APIs gratuitas o de bajo costo
- **Conectividad:** Si usa API externa, requiere internet
- **Idioma:** Español (prioritario)
- **Complejidad:** Debe ser demostrable en 8 minutos
- **Originalidad:** Cada generación debe ser única

---

## PASO 2: ARQUITECTURA DEL SISTEMA

### 2.1 Diagrama de Flujo General

```
[Usuario] 
    ↓
[Interfaz de Entrada] → Recibe prompt
    ↓
[Procesador de Prompt] → Analiza y estructura la solicitud
    ↓
[Generador de Cuento] → Crea narrativa creativa
    ↓
[Validador de Estructura] → Verifica formato de cuento
    ↓
[Display de Texto] → Muestra cuento generado
    ↓
[Conversor TTS] → Convierte texto a audio
    ↓
[Reproductor de Audio] → Narra el cuento
    ↓
[Usuario] → Escucha y ve el resultado
```

### 2.2 Componentes Detallados

#### 2.2.1 Módulo de Interfaz de Usuario
- **Responsabilidad:** Capturar input del usuario y mostrar resultados
- **Tecnología:** HTML/CSS/JS o Tkinter
- **Entradas:** Texto del prompt
- **Salidas:** Cuento generado (texto), audio (reproducción)

#### 2.2.2 Módulo de Procesamiento de Prompt
- **Responsabilidad:** Analizar y estructurar la solicitud del usuario
- **Funciones:**
  - Extracción de palabras clave
  - Identificación de tipo de solicitud (tema, personaje, situación)
  - Preparación del prompt para el generador

#### 2.2.3 Módulo Generador de Cuento
- **Responsabilidad:** Crear narrativa original y estructurada
- **Estrategia:**
  - Usar modelo de lenguaje (API o local)
  - Prompt engineering para asegurar estructura de cuento
  - Inyección de creatividad mediante variabilidad

#### 2.2.4 Módulo de Text-to-Speech
- **Responsabilidad:** Convertir texto a voz natural
- **Tecnología:** gTTS (online) o pyttsx3 (offline)
- **Configuración:** Voz en español, velocidad adecuada

---

## PASO 3: PROTOTIPO BÁSICO FUNCIONAL

### 3.1 Estructura de Archivos Propuesta

```
robot_narrativo/
├── app.py                 # Aplicación principal
├── generador_cuento.py    # Lógica de generación
├── tts_handler.py         # Manejo de text-to-speech
├── templates/
│   └── index.html         # Interfaz web
├── static/
│   └── style.css          # Estilos
├── requirements.txt       # Dependencias
└── README.md              # Documentación
```

### 3.2 Dependencias Principales

```python
# requirements.txt
flask>=2.3.0
openai>=1.0.0  # O alternativa gratuita
gtts>=2.3.0
pyttsx3>=2.90  # Alternativa offline
python-dotenv>=1.0.0
```

---

## PASO 4: JUSTIFICACIÓN CONCEPTUAL

### 4.1 ¿Por qué este diseño representa la Creatividad?

1. **Generación Original:** Cada cuento es único, demostrando capacidad de crear contenido nuevo
2. **Pensamiento Adaptativo:** Interpreta prompts de diferentes maneras
3. **Producción Estructurada:** Combina libertad creativa con coherencia narrativa
4. **Expresión Multimodal:** Crea tanto texto como audio, mostrando versatilidad

### 4.2 Elementos Observables de Creatividad

- **Variabilidad:** Mismo prompt → diferentes cuentos
- **Originalidad:** No repite exactamente el mismo contenido
- **Estructuración:** Organiza ideas en narrativa coherente
- **Adaptación:** Se ajusta al tipo de solicitud recibida

---

## PRÓXIMOS PASOS INMEDIATOS

1. ✅ Definir idea específica y alcance técnico
2. ⏳ Diseñar arquitectura detallada
3. ⏳ Crear prototipo básico funcional
4. ⏳ Documentar proceso y justificación

---

**Nota:** Este documento será la base para el desarrollo y el informe final.

