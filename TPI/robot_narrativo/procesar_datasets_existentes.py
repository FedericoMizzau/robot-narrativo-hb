"""
Script específico para procesar los datasets encontrados en la carpeta data/
- merged_clean.txt: Archivo grande con cuentos
- fairy_tales/: Carpeta con 1651 archivos .txt individuales
- folk_tales_deduplicated.csv: CSV con cuentos
"""

import os
import csv
from pathlib import Path
from procesar_dataset import ProcesadorDataset


def procesar_merged_clean(ruta_archivo: str, procesador: ProcesadorDataset) -> list:
    """
    Procesa merged_clean.txt que tiene cuentos separados por títulos.
    """
    print(f"\n📖 Procesando merged_clean.txt...")
    
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Los cuentos parecen estar separados por títulos (líneas con solo texto en mayúsculas)
    # Dividir por líneas vacías dobles o triples
    partes = contenido.split('\n\n\n')
    
    cuentos = []
    cuento_actual = []
    
    for parte in partes:
        lineas = parte.strip().split('\n')
        if not lineas:
            continue
        
        # Si la primera línea parece un título (corta, mayúsculas, sin punto)
        primera_linea = lineas[0].strip()
        if len(primera_linea) < 100 and not primera_linea.endswith('.'):
            # Es un título, empezar nuevo cuento
            if cuento_actual:
                cuento_texto = ' '.join(cuento_actual)
                cuento_limpio = procesador._limpiar_cuento(cuento_texto)
                if procesador._es_cuento_valido(cuento_limpio):
                    cuentos.append(cuento_limpio)
            cuento_actual = lineas[1:] if len(lineas) > 1 else []
        else:
            # Continuación del cuento
            cuento_actual.extend(lineas)
    
    # Agregar último cuento
    if cuento_actual:
        cuento_texto = ' '.join(cuento_actual)
        cuento_limpio = procesador._limpiar_cuento(cuento_texto)
        if procesador._es_cuento_valido(cuento_limpio):
            cuentos.append(cuento_limpio)
    
    print(f"✅ Procesados {len(cuentos)} cuentos de merged_clean.txt")
    return cuentos


def procesar_fairy_tales(ruta_directorio: str, procesador: ProcesadorDataset) -> list:
    """
    Procesa todos los archivos .txt de la carpeta fairy_tales/
    """
    print(f"\n📁 Procesando carpeta fairy_tales/...")
    
    directorio = Path(ruta_directorio)
    archivos_txt = list(directorio.glob("*.txt"))
    
    print(f"   Encontrados {len(archivos_txt)} archivos .txt")
    
    cuentos = []
    procesados = 0
    errores = 0
    
    for archivo in archivos_txt:
        try:
            with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read().strip()
            
            if contenido:
                cuento_limpio = procesador._limpiar_cuento(contenido)
                if procesador._es_cuento_valido(cuento_limpio):
                    cuentos.append(cuento_limpio)
                    procesados += 1
                else:
                    errores += 1
        except Exception as e:
            errores += 1
            if errores <= 5:  # Mostrar solo primeros 5 errores
                print(f"   ⚠️  Error en {archivo.name}: {e}")
        
        if procesados % 100 == 0:
            print(f"   Procesados {procesados}/{len(archivos_txt)} archivos...")
    
    print(f"✅ Procesados {procesados} cuentos válidos de {len(archivos_txt)} archivos")
    if errores > 0:
        print(f"   ⚠️  {errores} archivos no válidos o con errores")
    
    return cuentos


def procesar_folk_tales_csv(ruta_archivo: str, procesador: ProcesadorDataset) -> list:
    """
    Procesa el archivo CSV de folk tales.
    """
    print(f"\n📊 Procesando folk_tales_deduplicated.csv...")
    
    cuentos = []
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as f:
            # Intentar detectar delimitador
            primera_linea = f.readline()
            f.seek(0)
            
            # Probar diferentes delimitadores
            delimitador = ','
            if ';' in primera_linea:
                delimitador = ';'
            elif '\t' in primera_linea:
                delimitador = '\t'
            
            reader = csv.DictReader(f, delimiter=delimitador)
            
            # Buscar columna con texto
            columnas = reader.fieldnames
            columna_texto = None
            
            for col in ['text', 'story', 'cuento', 'texto', 'content', 'tale']:
                if col in columnas:
                    columna_texto = col
                    break
            
            if not columna_texto:
                # Usar la primera columna que no sea ID o índice
                for col in columnas:
                    if col.lower() not in ['id', 'index', 'idx', 'number']:
                        columna_texto = col
                        break
            
            print(f"   Usando columna: {columna_texto}")
            
            for i, row in enumerate(reader):
                if columna_texto and columna_texto in row:
                    texto = row[columna_texto]
                    if texto:
                        cuento_limpio = procesador._limpiar_cuento(str(texto))
                        if procesador._es_cuento_valido(cuento_limpio):
                            cuentos.append(cuento_limpio)
                
                if (i + 1) % 1000 == 0:
                    print(f"   Procesadas {i + 1} filas...")
        
        print(f"✅ Procesados {len(cuentos)} cuentos del CSV")
        
    except Exception as e:
        print(f"❌ Error procesando CSV: {e}")
        print("   Intentando método alternativo...")
        
        # Método alternativo: leer como texto
        try:
            with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read()
                # Dividir por líneas y procesar
                lineas = contenido.split('\n')[1:]  # Saltar header
                for linea in lineas:
                    if linea.strip():
                        # Extraer texto entre comillas o después de comas
                        partes = linea.split(',')
                        for parte in partes:
                            texto = parte.strip().strip('"').strip("'")
                            if len(texto) > 100:  # Probablemente es un cuento
                                cuento_limpio = procesador._limpiar_cuento(texto)
                                if procesador._es_cuento_valido(cuento_limpio):
                                    cuentos.append(cuento_limpio)
                                    break
            print(f"✅ Procesados {len(cuentos)} cuentos (método alternativo)")
        except Exception as e2:
            print(f"❌ Error en método alternativo: {e2}")
    
    return cuentos


def main():
    """
    Procesa todos los datasets y los combina.
    """
    print("=" * 60)
    print("📚 PROCESADOR DE DATASETS EXISTENTES")
    print("=" * 60)
    
    # Rutas base
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data"
    
    procesador = ProcesadorDataset()
    todos_cuentos = []
    
    # 1. Procesar merged_clean.txt
    merged_file = data_dir / "merged_clean.txt"
    if merged_file.exists():
        cuentos_merged = procesar_merged_clean(str(merged_file), procesador)
        todos_cuentos.extend(cuentos_merged)
    else:
        print("⚠️  No se encontró merged_clean.txt")
    
    # 2. Procesar fairy_tales/
    fairy_tales_dir = data_dir / "fairy_tales"
    if fairy_tales_dir.exists():
        cuentos_fairy = procesar_fairy_tales(str(fairy_tales_dir), procesador)
        todos_cuentos.extend(cuentos_fairy)
    else:
        print("⚠️  No se encontró carpeta fairy_tales/")
    
    # 3. Procesar CSV (opcional, puede ser muy grande)
    csv_file = data_dir / "folk_tales_deduplicated.csv"
    if csv_file.exists():
        print("\n💡 El CSV es grande (26MB), ¿procesarlo? (puede tardar)")
        print("   Si quieres procesarlo, descomenta la siguiente línea en el código")
        # cuentos_csv = procesar_folk_tales_csv(str(csv_file), procesador)
        # todos_cuentos.extend(cuentos_csv)
    else:
        print("⚠️  No se encontró folk_tales_deduplicated.csv")
    
    # Eliminar duplicados (aproximados)
    print(f"\n🔄 Eliminando duplicados...")
    cuentos_unicos = []
    textos_vistos = set()
    
    for cuento in todos_cuentos:
        # Usar hash de las primeras 200 palabras para detectar duplicados
        palabras_inicio = ' '.join(cuento.split()[:50])
        hash_corto = hash(palabras_inicio)
        
        if hash_corto not in textos_vistos:
            textos_vistos.add(hash_corto)
            cuentos_unicos.append(cuento)
    
    print(f"✅ {len(cuentos_unicos)} cuentos únicos de {len(todos_cuentos)} totales")
    
    if not cuentos_unicos:
        print("❌ No se encontraron cuentos válidos")
        return
    
    # Guardar resultado
    output_dir = base_dir / "robot_narrativo" / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    ruta_salida = output_dir / "cuentos_procesados.txt"
    procesador.guardar_para_entrenamiento(cuentos_unicos, str(ruta_salida))
    
    # Estadísticas
    print("\n" + "=" * 60)
    print("📊 ESTADÍSTICAS FINALES")
    print("=" * 60)
    print(f"Total de cuentos: {len(cuentos_unicos)}")
    total_palabras = sum(len(c.split()) for c in cuentos_unicos)
    print(f"Total de palabras: {total_palabras:,}")
    print(f"Promedio palabras/cuento: {total_palabras // len(cuentos_unicos) if cuentos_unicos else 0}")
    print(f"\n💾 Archivo guardado en: {ruta_salida}")
    print(f"\n🚀 Próximo paso: Entrenar el modelo")
    print(f"   python fine_tuning.py {ruta_salida}")
    print("=" * 60)


if __name__ == "__main__":
    main()

