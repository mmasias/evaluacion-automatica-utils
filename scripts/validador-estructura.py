#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

def cargar_configuracion(asignatura, repo_config):
    """Carga la configuración específica de la asignatura"""
    config_path = f"configs/criterios-{asignatura.lower()}.json"
    
    # Descargar config desde el repo central
    import urllib.request
    config_url = f"https://raw.githubusercontent.com/mmasias/evaluacion-automatica-utils/main/{config_path}"
    
    with urllib.request.urlopen(config_url) as response:
        criterios_base = json.loads(response.read().decode())
    
    # Combinar con configuración específica del repo
    criterios_base.update(repo_config)
    return criterios_base

def validar_estructura_carpetas(criterios):
    """Valida que existan las carpetas requeridas"""
    errores = []
    carpetas_requeridas = criterios.get("carpetas_requeridas", [])
    
    for carpeta in carpetas_requeridas:
        if not Path(carpeta).exists():
            errores.append(f"❌ Falta la carpeta requerida: {carpeta}")
        else:
            print(f"✅ Carpeta encontrada: {carpeta}")
    
    return errores

def validar_archivos_obligatorios(criterios):
    """Valida que existan los archivos obligatorios"""
    errores = []
    archivos_requeridos = criterios.get("archivos_requeridos", [])
    
    for archivo in archivos_requeridos:
        if not Path(archivo).exists():
            errores.append(f"❌ Falta el archivo requerido: {archivo}")
        else:
            print(f"✅ Archivo encontrado: {archivo}")
    
    return errores

def validar_nomenclatura(criterios):
    """Valida nomenclatura de archivos según patrones"""
    errores = []
    patrones = criterios.get("patrones_nomenclatura", {})
    
    for patron, descripcion in patrones.items():
        archivos = list(Path().glob(patron))
        if not archivos:
            errores.append(f"❌ No se encontraron archivos que sigan el patrón: {patron} ({descripcion})")
    
    return errores

def main():
    # Leer configuración del repo actual
    with open('.github/evaluacion-config.json', 'r') as f:
        repo_config = json.load(f)
    
    asignatura = repo_config['asignatura']
    criterios = cargar_configuracion(asignatura, repo_config)
    
    print(f"🔍 Iniciando validación para {asignatura}")
    print("=" * 50)
    
    todos_los_errores = []
    
    # Ejecutar validaciones
    todos_los_errores.extend(validar_estructura_carpetas(criterios))
    todos_los_errores.extend(validar_archivos_obligatorios(criterios))
    todos_los_errores.extend(validar_nomenclatura(criterios))
    
    if todos_los_errores:
        print("\n💥 ERRORES ENCONTRADOS:")
        for error in todos_los_errores:
            print(error)
        
        # Crear comentario para el PR
        comentario = generar_comentario_rechazo(todos_los_errores, asignatura)
        with open('pr_comment.txt', 'w') as f:
            f.write(comentario)
        
        sys.exit(1)
    else:
        print("\n🎉 ¡Todas las validaciones pasaron correctamente!")
        
        comentario = generar_comentario_aprobacion(asignatura)
        with open('pr_comment.txt', 'w') as f:
            f.write(comentario)

def generar_comentario_rechazo(errores, asignatura):
    return f"""## ❌ Validación Automática Fallida - {asignatura.upper()}

Tu trabajo no cumple con algunos requisitos básicos. Por favor, corrige los siguientes problemas y vuelve a hacer el pull request:

### Errores Encontrados:
{chr(10).join(['- ' + error for error in errores])}

### 📝 Recordatorio:
- Revisa la estructura de carpetas del template
- Verifica que todos los archivos requeridos estén presentes
- Asegúrate de seguir las convenciones de nomenclatura

Una vez corregidos estos problemas, puedes cerrar este PR, hacer los cambios en tu rama, y crear un nuevo PR.

---
*Validación automática realizada por el sistema de evaluación de {asignatura}*
"""

def generar_comentario_aprobacion(asignatura):
    return f"""## ✅ Validación Automática Exitosa - {asignatura.upper()}

¡Excelente! Tu trabajo cumple con todos los requisitos estructurales básicos.

### Validaciones Completadas:
- ✅ Estructura de carpetas correcta
- ✅ Archivos obligatorios presentes
- ✅ Nomenclatura adecuada

Tu trabajo ahora será revisado manualmente por el profesor.

---
*Validación automática realizada por el sistema de evaluación de {asignatura}*
"""

if __name__ == "__main__":
    main()