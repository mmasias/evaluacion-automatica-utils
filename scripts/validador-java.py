#!/usr/bin/env python3
import subprocess
import os
from pathlib import Path

def compilar_java():
    """Compila todos los archivos Java del proyecto"""
    archivos_java = list(Path("src").rglob("*.java"))
    
    if not archivos_java:
        return False, "No se encontraron archivos Java para compilar"
    
    try:
        # Crear directorio de compilación
        Path("build").mkdir(exist_ok=True)
        
        # Compilar todos los archivos Java
        cmd = ["javac", "-d", "build", "-cp", "src"] + [str(f) for f in archivos_java]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True, "Compilación exitosa"
        else:
            return False, f"Errores de compilación:\n{result.stderr}"
    
    except Exception as e:
        return False, f"Error durante la compilación: {str(e)}"

def ejecutar_main():
    """Intenta ejecutar la clase Main del proyecto"""
    try:
        result = subprocess.run(
            ["java", "-cp", "build", "Main"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            return True, f"Ejecución exitosa:\n{result.stdout}"
        else:
            return False, f"Error en ejecución:\n{result.stderr}"
    
    except subprocess.TimeoutExpired:
        return False, "La ejecución excedió el tiempo límite (10 segundos)"
    except Exception as e:
        return False, f"Error durante la ejecución: {str(e)}"

if __name__ == "__main__":
    print("🔨 Compilando código Java...")
    compilacion_ok, mensaje_compilacion = compilar_java()
    
    if not compilacion_ok:
        print(f"❌ {mensaje_compilacion}")
        exit(1)
    
    print(f"✅ {mensaje_compilacion}")
    
    print("🚀 Ejecutando programa...")
    ejecucion_ok, mensaje_ejecucion = ejecutar_main()
    
    if ejecucion_ok:
        print(f"✅ {mensaje_ejecucion}")
    else:
        print(f"⚠️ {mensaje_ejecucion}")
        # Para PRG1, un warning es suficiente
        # Para asignaturas avanzadas, podría ser error crítico