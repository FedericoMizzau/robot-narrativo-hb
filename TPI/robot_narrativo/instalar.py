#!/usr/bin/env python3
"""
Script de instalación y verificación del Robot Narrativo Generativo
"""

import sys
import subprocess
import os

def verificar_python():
    """Verifica que Python esté instalado y sea la versión correcta."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def instalar_dependencias():
    """Instala las dependencias del proyecto."""
    print("\n📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error al instalar dependencias")
        return False

def verificar_dependencias():
    """Verifica que las dependencias principales estén instaladas."""
    print("\n🔍 Verificando dependencias...")
    dependencias = ['flask', 'gtts', 'pyttsx3', 'dotenv']
    faltantes = []
    
    for dep in dependencias:
        try:
            if dep == 'dotenv':
                __import__('dotenv')
            else:
                __import__(dep)
            print(f"✅ {dep} instalado")
        except ImportError:
            print(f"❌ {dep} no encontrado")
            faltantes.append(dep)
    
    return len(faltantes) == 0

def crear_archivo_env():
    """Crea el archivo .env si no existe."""
    if not os.path.exists('.env'):
        print("\n📝 Creando archivo .env...")
        with open('.env', 'w') as f:
            f.write("# Configuración del Robot Narrativo Generativo\n")
            f.write("# Clave de API de OpenAI (opcional)\n")
            f.write("# OPENAI_API_KEY=tu_clave_aqui\n")
            f.write("\n# Clave secreta para Flask (opcional)\n")
            f.write("SECRET_KEY=robot-narrativo-secret-key-change-in-production\n")
        print("✅ Archivo .env creado")
        print("   💡 Puedes agregar tu OPENAI_API_KEY en el archivo .env si lo deseas")
    else:
        print("✅ Archivo .env ya existe")

def main():
    """Función principal del script de instalación."""
    print("=" * 60)
    print("🤖 INSTALACIÓN DEL ROBOT NARRATIVO GENERATIVO")
    print("=" * 60)
    
    # Verificar Python
    if not verificar_python():
        sys.exit(1)
    
    # Instalar dependencias
    if not instalar_dependencias():
        print("\n⚠️  Intenta instalar manualmente: pip install -r requirements.txt")
        sys.exit(1)
    
    # Verificar dependencias
    if not verificar_dependencias():
        print("\n⚠️  Algunas dependencias no se instalaron correctamente")
        print("   Intenta: pip install -r requirements.txt")
    
    # Crear archivo .env
    crear_archivo_env()
    
    print("\n" + "=" * 60)
    print("✅ INSTALACIÓN COMPLETADA")
    print("=" * 60)
    print("\n🚀 Para iniciar el robot, ejecuta:")
    print("   python app.py")
    print("\n🌐 Luego abre tu navegador en:")
    print("   http://localhost:5000")
    print("\n💡 Nota: Si quieres usar OpenAI API, agrega tu clave en .env")
    print("=" * 60)

if __name__ == "__main__":
    main()

