# 📚 SISTEMA PARA USAR DATASETS REALES - COMPLETADO

## ✅ Lo que se ha Implementado

### 1. Procesador de Datasets (`procesar_dataset.py`)
- ✅ Soporta múltiples formatos: TXT, JSON
- ✅ Procesa archivos individuales o directorios completos
- ✅ Limpia y normaliza el texto automáticamente
- ✅ Valida que los cuentos sean adecuados (50-2000 palabras)
- ✅ Guarda en formato optimizado para entrenamiento

### 2. Script de Fine-Tuning Mejorado (`fine_tuning.py`)
- ✅ Interfaz de línea de comandos fácil de usar
- ✅ Detección automática de GPU/CPU
- ✅ Parámetros configurables (épocas, batch size, etc.)
- ✅ Manejo de errores y checkpoints
- ✅ Optimizado para diferentes hardware

### 3. Descargador de Datasets (`descargar_dataset_ejemplo.py`)
- ✅ Ejemplo para descargar desde Hugging Face
- ✅ Fácil de adaptar a otros datasets

### 4. Guía Completa (`GUIA_DATASETS.md`)
- ✅ Dónde conseguir datasets
- ✅ Cómo procesarlos
- ✅ Cómo entrenar
- ✅ Cómo usar el modelo entrenado

### 5. Integración con Sistema Actual
- ✅ `generador_ml.py` actualizado para usar modelos fine-tuneados
- ✅ Soporta rutas a modelos propios
- ✅ Fallback automático si el modelo no está disponible

---

## 🚀 Flujo Completo de Uso

### Paso 1: Conseguir Dataset
```bash
# Opción A: Desde Hugging Face (requiere: pip install datasets)
python descargar_dataset_ejemplo.py

# Opción B: Usar archivo propio
# Simplemente coloca tu archivo de cuentos en el proyecto
```

### Paso 2: Procesar Dataset
```bash
source venv/Scripts/activate

# Procesar archivo
python procesar_dataset.py mi_dataset.txt

# O procesar directorio
python procesar_dataset.py ./mis_cuentos/ txt
```

**Resultado:** `data/cuentos_procesados.txt` listo para entrenar

### Paso 3: Entrenar Modelo
```bash
# Entrenamiento básico
python fine_tuning.py data/cuentos_procesados.txt

# Con opciones
python fine_tuning.py data/cuentos_procesados.txt \
    --epochs 5 \
    --batch 2 \
    --output ./mi_modelo
```

**Resultado:** Modelo entrenado en `./modelo_cuentos` (o directorio especificado)

### Paso 4: Usar Modelo Entrenado
```python
# En app.py, cambiar:
generador = GeneradorCuento(
    usar_ml=True,
    modelo_ml="./modelo_cuentos"  # Ruta a tu modelo
)
```

---

## 📊 Requisitos y Tiempos

### Dataset Mínimo:
- **50-100 cuentos** para empezar
- **200-500 cuentos** para mejor calidad
- **1000+ cuentos** para resultados óptimos

### Tiempos Estimados de Entrenamiento:

| Hardware | 100 cuentos | 500 cuentos | 1000 cuentos |
|----------|-------------|-------------|--------------|
| **GPU NVIDIA** | 10-20 min | 30-60 min | 1-2 horas |
| **CPU** | 2-4 horas | 8-12 horas | 16-24 horas |

### Memoria Requerida:
- **GPU:** 4-8 GB VRAM
- **CPU:** 8-16 GB RAM
- **Disco:** ~2-5 GB (modelo + dataset)

---

## 🎯 Dónde Conseguir Datasets

### 1. Hugging Face (Recomendado)
- URL: https://huggingface.co/datasets
- Buscar: "spanish stories", "cuentos", "fairy tales"
- Instalar: `pip install datasets`

### 2. Proyecto Gutenberg
- URL: https://www.gutenberg.org/
- Libros y cuentos en dominio público
- Muchos en español

### 3. Kaggle
- URL: https://www.kaggle.com/datasets
- Buscar: "spanish stories", "cuentos"

### 4. Recopilar Propios
- Wikipedia (artículos sobre cuentos)
- Bibliotecas digitales
- Crear propios

---

## 📝 Ejemplo Rápido

```bash
# 1. Procesar tu dataset
python procesar_dataset.py mis_cuentos.txt

# 2. Entrenar (con GPU si está disponible)
python fine_tuning.py data/cuentos_procesados.txt --epochs 3

# 3. El modelo se guarda en ./modelo_cuentos

# 4. Actualizar app.py:
#    modelo_ml="./modelo_cuentos"

# 5. Probar
python app.py
```

---

## ⚙️ Configuración Avanzada

### Ajustar Parámetros de Entrenamiento:

```bash
# Más épocas (mejor calidad, más tiempo)
python fine_tuning.py data/cuentos_procesados.txt --epochs 5

# Batch más pequeño (si hay problemas de memoria)
python fine_tuning.py data/cuentos_procesados.txt --batch 1

# Modelo base diferente
python fine_tuning.py data/cuentos_procesados.txt --model distilgpt2

# Forzar CPU
python fine_tuning.py data/cuentos_procesados.txt --cpu
```

---

## 🔍 Verificar Calidad

### Antes de Entrenar:
```python
from procesar_dataset import ProcesadorDataset

procesador = ProcesadorDataset()
cuentos = procesador.procesar_archivo_txt("data/cuentos_procesados.txt")

print(f"Total: {len(cuentos)} cuentos")
print(f"Promedio: {sum(len(c.split()) for c in cuentos) / len(cuentos):.0f} palabras")
```

### Después de Entrenar:
```python
from generador_ml import GeneradorML

gen = GeneradorML(modelo="./modelo_cuentos")
cuento = gen.generar_cuento("Un cuento sobre...")
print(cuento)
```

---

## 📁 Archivos Creados

- ✅ `procesar_dataset.py` - Procesador de datasets
- ✅ `fine_tuning.py` - Script de fine-tuning mejorado
- ✅ `descargar_dataset_ejemplo.py` - Ejemplo para Hugging Face
- ✅ `GUIA_DATASETS.md` - Guía completa
- ✅ `06_USAR_DATASETS_REALES.md` - Este resumen

---

## ✅ Estado Actual

- ✅ **Sistema completo para usar datasets reales**
- ✅ **Procesador de datasets funcionando**
- ✅ **Script de fine-tuning optimizado**
- ✅ **Integración con sistema actual**
- ✅ **Documentación completa**

---

## 🎓 Próximos Pasos

1. **Conseguir dataset** de cuentos en español
2. **Procesar** con `procesar_dataset.py`
3. **Entrenar** con `fine_tuning.py`
4. **Usar** el modelo entrenado en el sistema

---

**¡El sistema está listo para usar datasets reales y mejorar la calidad de los cuentos generados! 🚀**


