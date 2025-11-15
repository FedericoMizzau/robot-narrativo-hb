"""
Script para procesar un dataset de cuentos reales y prepararlo para fine-tuning.
Soporta múltiples formatos: TXT, JSON, CSV
"""

import json
import os
import re
from typing import List, Dict
from pathlib import Path


class ProcesadorDataset:
    """
    Procesa datasets de cuentos y los prepara para fine-tuning.
    """
    
    def __init__(self):
        self.cuentos_procesados = []
    
    def procesar_archivo_txt(self, ruta_archivo: str, separador: str = "\n\n") -> List[str]:
        """
        Procesa un archivo de texto con cuentos.
        
        Args:
            ruta_archivo: Ruta al archivo de texto
            separador: Separador entre cuentos (por defecto línea vacía)
            
        Returns:
            Lista de cuentos procesados
        """
        print(f"📖 Procesando archivo TXT: {ruta_archivo}")
        
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Dividir por separador
        cuentos = contenido.split(separador)
        
        # Limpiar y filtrar
        cuentos_limpios = []
        for cuento in cuentos:
            cuento_limpio = self._limpiar_cuento(cuento)
            if self._es_cuento_valido(cuento_limpio):
                cuentos_limpios.append(cuento_limpio)
        
        print(f"✅ Procesados {len(cuentos_limpios)} cuentos válidos de {len(cuentos)} totales")
        return cuentos_limpios
    
    def procesar_archivo_json(self, ruta_archivo: str, campo_texto: str = "text") -> List[str]:
        """
        Procesa un archivo JSON con cuentos.
        
        Args:
            ruta_archivo: Ruta al archivo JSON
            campo_texto: Nombre del campo que contiene el texto del cuento
            
        Returns:
            Lista de cuentos procesados
        """
        print(f"📖 Procesando archivo JSON: {ruta_archivo}")
        
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        cuentos = []
        
        # Si es una lista
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    texto = item.get(campo_texto, item.get('cuento', item.get('story', '')))
                else:
                    texto = str(item)
                cuento_limpio = self._limpiar_cuento(texto)
                if self._es_cuento_valido(cuento_limpio):
                    cuentos.append(cuento_limpio)
        
        # Si es un diccionario
        elif isinstance(data, dict):
            if 'cuentos' in data:
                for cuento in data['cuentos']:
                    texto = cuento.get(campo_texto, cuento.get('texto', cuento.get('text', '')))
                    cuento_limpio = self._limpiar_cuento(texto)
                    if self._es_cuento_valido(cuento_limpio):
                        cuentos.append(cuento_limpio)
            else:
                # Buscar cualquier campo que parezca contener cuentos
                for key, value in data.items():
                    if isinstance(value, (list, str)):
                        if isinstance(value, str):
                            cuento_limpio = self._limpiar_cuento(value)
                            if self._es_cuento_valido(cuento_limpio):
                                cuentos.append(cuento_limpio)
        
        print(f"✅ Procesados {len(cuentos)} cuentos válidos")
        return cuentos
    
    def procesar_directorio(self, directorio: str, extension: str = ".txt") -> List[str]:
        """
        Procesa todos los archivos de un directorio.
        
        Args:
            directorio: Ruta al directorio
            extension: Extensión de archivos a procesar (.txt, .json, etc.)
            
        Returns:
            Lista de todos los cuentos procesados
        """
        print(f"📁 Procesando directorio: {directorio}")
        
        todos_cuentos = []
        archivos = list(Path(directorio).glob(f"*{extension}"))
        
        for archivo in archivos:
            try:
                if extension == ".txt":
                    cuentos = self.procesar_archivo_txt(str(archivo))
                elif extension == ".json":
                    cuentos = self.procesar_archivo_json(str(archivo))
                else:
                    continue
                todos_cuentos.extend(cuentos)
            except Exception as e:
                print(f"⚠️  Error procesando {archivo}: {e}")
        
        print(f"✅ Total de cuentos procesados: {len(todos_cuentos)}")
        return todos_cuentos
    
    def _limpiar_cuento(self, texto: str) -> str:
        """
        Limpia un cuento: remueve espacios extra, normaliza, etc.
        
        Args:
            texto: Texto del cuento
            
        Returns:
            Texto limpio
        """
        if not texto:
            return ""
        
        # Remover espacios múltiples
        texto = re.sub(r'\s+', ' ', texto)
        
        # Remover saltos de línea múltiples
        texto = re.sub(r'\n+', ' ', texto)
        
        # Remover caracteres especiales problemáticos (mantener puntuación básica)
        texto = re.sub(r'[^\w\s\.\,\!\?\;\:\-áéíóúñÁÉÍÓÚÑ]', '', texto)
        
        # Normalizar espacios alrededor de puntuación
        texto = re.sub(r'\s+([\.\,\!\?\;\:])', r'\1', texto)
        texto = re.sub(r'([\.\,\!\?\;\:])\s*', r'\1 ', texto)
        
        return texto.strip()
    
    def _es_cuento_valido(self, cuento: str, min_palabras: int = 50, max_palabras: int = 2000) -> bool:
        """
        Valida que un cuento sea adecuado para entrenamiento.
        
        Args:
            cuento: Texto del cuento
            min_palabras: Mínimo de palabras requeridas
            max_palabras: Máximo de palabras permitidas
            
        Returns:
            True si el cuento es válido
        """
        if not cuento:
            return False
        
        palabras = cuento.split()
        num_palabras = len(palabras)
        
        # Validar longitud
        if num_palabras < min_palabras or num_palabras > max_palabras:
            return False
        
        # Validar que tenga puntuación (indica texto completo)
        if not re.search(r'[\.\!\?]', cuento):
            return False
        
        # Validar que no sea solo números o caracteres especiales
        if not re.search(r'[a-zA-ZáéíóúñÁÉÍÓÚÑ]', cuento):
            return False
        
        return True
    
    def guardar_para_entrenamiento(self, cuentos: List[str], ruta_salida: str):
        """
        Guarda los cuentos procesados en formato para fine-tuning.
        
        Args:
            cuentos: Lista de cuentos procesados
            ruta_salida: Ruta donde guardar el archivo
        """
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(ruta_salida) if os.path.dirname(ruta_salida) else '.', exist_ok=True)
        
        # Guardar como texto (un cuento por línea, separados por línea vacía)
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            for cuento in cuentos:
                f.write(cuento + '\n\n')
        
        print(f"✅ Guardados {len(cuentos)} cuentos en {ruta_salida}")
        print(f"   Tamaño del archivo: {os.path.getsize(ruta_salida) / 1024:.2f} KB")
    
    def guardar_json(self, cuentos: List[str], ruta_salida: str):
        """
        Guarda los cuentos en formato JSON.
        
        Args:
            cuentos: Lista de cuentos procesados
            ruta_salida: Ruta donde guardar el archivo
        """
        data = {
            "cuentos": [
                {"texto": cuento, "palabras": len(cuento.split())}
                for cuento in cuentos
            ],
            "total": len(cuentos)
        }
        
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Guardados {len(cuentos)} cuentos en JSON: {ruta_salida}")


def main():
    """
    Función principal para procesar un dataset.
    """
    import sys
    
    print("=" * 60)
    print("📚 PROCESADOR DE DATASET DE CUENTOS")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\nUso:")
        print("  python procesar_dataset.py <archivo_o_directorio> [formato]")
        print("\nEjemplos:")
        print("  python procesar_dataset.py cuentos.txt")
        print("  python procesar_dataset.py cuentos.json json")
        print("  python procesar_dataset.py ./datasets/ txt")
        print("\nFormatos soportados: txt, json")
        return
    
    ruta_entrada = sys.argv[1]
    formato = sys.argv[2] if len(sys.argv) > 2 else None
    
    procesador = ProcesadorDataset()
    cuentos = []
    
    # Detectar formato
    if os.path.isdir(ruta_entrada):
        # Es un directorio
        extension = formato if formato else ".txt"
        cuentos = procesador.procesar_directorio(ruta_entrada, extension)
    elif os.path.isfile(ruta_entrada):
        # Es un archivo
        extension = os.path.splitext(ruta_entrada)[1].lower()
        
        if extension == ".txt" or formato == "txt":
            cuentos = procesador.procesar_archivo_txt(ruta_entrada)
        elif extension == ".json" or formato == "json":
            cuentos = procesador.procesar_archivo_json(ruta_entrada)
        else:
            print(f"❌ Formato no soportado: {extension}")
            return
    else:
        print(f"❌ No se encontró: {ruta_entrada}")
        return
    
    if not cuentos:
        print("❌ No se encontraron cuentos válidos")
        return
    
    # Guardar resultado
    ruta_salida = "data/cuentos_procesados.txt"
    procesador.guardar_para_entrenamiento(cuentos, ruta_salida)
    
    # También guardar JSON para referencia
    procesador.guardar_json(cuentos, "data/cuentos_procesados.json")
    
    print("\n" + "=" * 60)
    print("✅ PROCESAMIENTO COMPLETADO")
    print("=" * 60)
    print(f"\n📊 Estadísticas:")
    print(f"   Total de cuentos: {len(cuentos)}")
    total_palabras = sum(len(c.split()) for c in cuentos)
    print(f"   Total de palabras: {total_palabras:,}")
    print(f"   Promedio palabras/cuento: {total_palabras // len(cuentos)}")
    print(f"\n💾 Archivos guardados:")
    print(f"   - {ruta_salida} (para entrenamiento)")
    print(f"   - data/cuentos_procesados.json (referencia)")


if __name__ == "__main__":
    main()


