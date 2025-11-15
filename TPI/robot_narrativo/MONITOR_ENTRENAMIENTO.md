# 📊 MONITOR DEL ENTRENAMIENTO

## 🎓 Entrenamiento en Progreso

El modelo está siendo entrenado con **1,827 cuentos reales** de tus datasets.

---

## ⏱️ Estado Actual

- **Estado:** ✅ Entrenamiento iniciado
- **Hardware:** CPU
- **Tiempo estimado:** ~2 horas
- **Progreso:** En curso...

---

## 🔍 Cómo Verificar el Progreso

### Verificar si hay checkpoints:

```bash
cd robot_narrativo
source venv/Scripts/activate
python verificar_entrenamiento.py
```

O manualmente:
```bash
ls modelo_cuentos_entrenado/
```

Si ves carpetas `checkpoint-500`, `checkpoint-1000`, etc., el entrenamiento está progresando.

---

## 📈 Progreso Esperado

| Tiempo | Checkpoint Esperado |
|--------|---------------------|
| ~30-40 min | checkpoint-500 |
| ~1 hora | checkpoint-1000 |
| ~1.5 horas | checkpoint-1500 |
| ~2 horas | Modelo final |

---

## 💻 Uso de Recursos

Durante el entrenamiento:
- **CPU:** Alto uso (normal)
- **RAM:** ~4-8 GB
- **Disco:** ~2-3 GB (para el modelo)

---

## ⚠️ Si el Entrenamiento se Interrumpe

No te preocupes, el último checkpoint se guarda automáticamente. Puedes:
1. Verificar el último checkpoint guardado
2. Reanudar desde ahí si es necesario
3. O usar el modelo parcial si está suficientemente entrenado

---

## ✅ Cuando Termine

Verás un mensaje como:
```
✅ FINE-TUNING COMPLETADO!
📁 Modelo guardado en: modelo_cuentos_entrenado
```

Luego actualiza `app.py` para usar el modelo entrenado.

---

**El entrenamiento está corriendo. Puedes dejarlo ejecutándose. 🚀**

