import os
import sys
import importlib
import inspect
from pathlib import Path

# Agregar la raíz del proyecto a sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))


def obtener_funcion(path_modulo, *nombres_posibles):
    """Busca dinámicamente la función a ejecutar en un módulo."""
    try:
        mod = importlib.import_module(path_modulo)
        for nombre in nombres_posibles:
            if hasattr(mod, nombre):
                func = getattr(mod, nombre)
                if callable(func):
                    return func
        if hasattr(mod, "main") and callable(mod.main):
            return mod.main
    except Exception as e:
        print(f"  ⚠️ Error al cargar módulo '{path_modulo}': {e}")
    return None


def ejecutar_seguro(func, ruta_defecto=None):
    """Ejecuta la función protegiendo el pipeline contra sys.exit() y pasando rutas por defecto."""
    argv_original = list(sys.argv)
    if ruta_defecto:
        sys.argv = [sys.argv[0], str(ruta_defecto)]
    
    try:
        sig = inspect.signature(func)
        params_requeridos = [p for p in sig.parameters.values() if p.default == p.empty]
        if len(params_requeridos) > 0 and ruta_defecto:
            func(str(ruta_defecto))
        else:
            func()
    except SystemExit:
        pass  # Evita que sys.exit() dentro de un módulo tumbe main.py
    finally:
        sys.argv = argv_original


def crear_directorios():
    """Garantiza la existencia de la estructura data/"""
    for subcarpeta in ["crudo", "limpio", "graficas"]:
        os.makedirs(ROOT_DIR / "data" / subcarpeta, exist_ok=True)


def ejecutar_paso(nombre_paso, tareas):
    print(f"\n--- {nombre_paso} ---")
    for item in tareas:
        nombre_tarea = item[0]
        path_modulo = item[1]
        nombres_posibles = item[2]
        ruta_defecto = item[3] if len(item) > 3 else None

        func = obtener_funcion(path_modulo, *nombres_posibles)
        if func:
            try:
                ejecutar_seguro(func, ruta_defecto)
                print(f"  ✓ {nombre_tarea} ejecutado correctamente.")
            except Exception as e:
                print(f"  ⚠️ Error en {nombre_tarea}: {e}")
        else:
            print(f"  ℹ️ {nombre_tarea} omitido (función no encontrada en {path_modulo}).")


def main():
    print("=" * 60)
    print("   EJECUCIÓN PIPELINE PROYECTO INTEGRADOR (KAIZEN)   ")
    print("=" * 60)

    crear_directorios()

    ejecutar_paso("1. SIMULACIÓN DE DATOS (F01)", [
        ("Empresas", "notebook.simulaciones.simular_empresas", ["generar_empresas", "simular_empresas"]),
        ("Categorías", "notebook.simulaciones.simular_categorias", ["generar_categorias", "simular_categorias"]),
        ("Registros", "notebook.simulaciones.simular_registros", ["generar_registros", "simular_registros"]),
        ("Retos", "notebook.simulaciones.simular_retos", ["generar_retos", "simular_retos"]),
    ])

    ejecutar_paso("2. EXPORTACIÓN DE ARCHIVOS CRUDOS (X01)", [
        ("Empresas Crudos", "notebook.exportaciones.exportar_empresas", ["exportar_empresas_crudos", "exportar_empresas"]),
        ("Categorías Crudos", "notebook.exportaciones.exportar_categorias", ["exportar_categorias", "exportar_categorias_crudos"]),
        ("Registros Crudos", "notebook.exportaciones.exportar_registros", ["exportar_registros", "exportar_registros_crudos"]),
        ("Retos Crudos", "notebook.exportaciones.exportar_retos", ["exportar_retos", "exportar_retos_crudos"]),
    ])

    ejecutar_paso("3. LIMPIEZA DE DATOS (L01)", [
        ("Limpieza Empresas", "notebook.limpieza.limpieza_empresas", ["main", "limpiar_empresas", "limpieza_empresas"], ROOT_DIR / "data" / "crudo" / "empresas_sucio.csv"),
        ("Limpieza Categorías", "notebook.limpieza.limpiar_categorias", ["main", "limpieza_categorias", "limpiar_categorias"], ROOT_DIR / "data" / "crudo" / "categorias_sucio.csv"),
        ("Limpieza Registros", "notebook.limpieza.limpieza_registros", ["main", "limpieza_registros", "limpiar_registros"], ROOT_DIR / "data" / "crudo" / "registros_sucio.csv"),
        ("Limpieza Retos", "notebook.limpieza.limpieza_retos", ["main", "limpieza_retos", "limpiar_retos"], ROOT_DIR / "data" / "crudo" / "retos_sucio.csv"),
    ])

    ejecutar_paso("4. CONSULTAS Y ANÁLISIS (Q01)", [
        ("Consultas Registros", "notebook.consultas.consultas_registros", ["main", "consultar_registros", "consultas_registros"]),
        ("Consultas Retos", "notebook.consultas.consultas_retos", ["main", "consultar_retos", "consultas_retos"]),
    ])

    ejecutar_paso("5. REPORTES GRÁFICOS (G01)", [
        ("Gráficas Empresas", "notebook.graficas.graficar_empresas", ["main", "graficar_empresas"]),
        ("Gráficas Categorías", "notebook.graficas.reporte_categorias", ["main", "reporte_categorias"]),
        ("Gráficas Registros", "notebook.graficas.graficar_registros", ["main", "graficar_registros"]),
        ("Gráficas Retos", "notebook.graficas.graficar_retos", ["main", "graficar_retos"]),
    ])

    print("\n" + "=" * 60)
    print("   ✓ EJECUCIÓN DEL PIPELINE CONCLUIDA   ")
    print("=" * 60)


if __name__ == "__main__":
    main()