"""
Script de ejemplo para descargar un dataset desde Hugging Face.
Ajusta según el dataset que quieras usar.
"""

def descargar_dataset_huggingface(nombre_dataset: str, ruta_salida: str = "data/cuentos_raw.txt"):
    """
    Descarga un dataset desde Hugging Face y lo guarda como texto.
    
    Args:
        nombre_dataset: Nombre del dataset en Hugging Face
        ruta_salida: Ruta donde guardar el archivo
    """
    try:
        from datasets import load_dataset
        
        print(f"📥 Descargando dataset: {nombre_dataset}")
        dataset = load_dataset(nombre_dataset)
        
        print(f"📊 Dataset cargado:")
        print(f"   Divisiones: {list(dataset.keys())}")
        
        # Usar la división de entrenamiento (o la primera disponible)
        split = "train" if "train" in dataset else list(dataset.keys())[0]
        datos = dataset[split]
        
        print(f"   Usando división: {split}")
        print(f"   Total de ejemplos: {len(datos)}")
        
        # Guardar como texto
        print(f"\n💾 Guardando en {ruta_salida}...")
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            for i, item in enumerate(datos):
                # Intentar diferentes campos comunes
                texto = None
                for campo in ['text', 'content', 'story', 'cuento', 'texto', 'content']:
                    if campo in item:
                        texto = item[campo]
                        break
                
                if texto:
                    f.write(str(texto) + '\n\n')
                
                if (i + 1) % 100 == 0:
                    print(f"   Procesados {i + 1}/{len(datos)} ejemplos...")
        
        print(f"✅ Dataset guardado en {ruta_salida}")
        print(f"\n📝 Próximo paso:")
        print(f"   python procesar_dataset.py {ruta_salida}")
        
    except ImportError:
        print("❌ Error: datasets no está instalado")
        print("   Instala con: pip install datasets")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("📥 DESCARGADOR DE DATASETS DE HUGGING FACE")
    print("=" * 60)
    
    print("\n💡 Ejemplos de datasets:")
    print("   - 'wikitext' (texto general)")
    print("   - Busca en https://huggingface.co/datasets")
    print("\n📝 Uso:")
    print("   python descargar_dataset_ejemplo.py")
    print("\n   O modifica este script para usar tu dataset específico")
    
    # Ejemplo: descomentar y ajustar
    # descargar_dataset_huggingface("wikitext", "data/cuentos_raw.txt")


