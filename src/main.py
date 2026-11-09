import sys
from pathlib import Path

# 1. Al estar dentro de src/, la raíz del proyecto es parents[1] (dos niveles arriba)
RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.append(str(RAIZ_PROYECTO))

from notebook.exportaciones.exportar_empresas import exportar_empresas_crudos
from notebook.limpieza.limpieza_empresas import (
    RUTA_SALIDA as RUTA_LIMPIO,
    leer_csv,
    limpiar,
    imprimir_diagnostico,
    guardar as guardar_limpio,
)
from notebook.consultas.consultas_empresas import (
    cargar_datos as cargar_datos_consultas,
    consulta_1_activas,
    consulta_2_sector,
    consulta_3_conteo,
    consulta_4_groupby,
    consulta_5_groupby_doble,
    guardar as guardar_consulta,
)
from notebook.reportes.reporte_empresas import (
    cargar_datos as cargar_datos_reportes,
    grafica_1_por_sector,
    grafica_2_activas,
    grafica_3_apiladas,
    imprimir_conclusiones,
)


def ejecutar_pipeline_master():
    print("=== 1. INICIANDO SIMULACIÓN Y EXPORTACIÓN (HU F01 / X01) ===")
    rutas_crudos = exportar_empresas_crudos()
    for ruta in rutas_crudos:
        print(f"  - {ruta}")

    print("\n=== 2. INICIANDO LIMPIEZA DE DATOS (HU L01) ===")
    ruta_csv_sucio = RAIZ_PROYECTO / "data" / "crudo" / "empresas_sucio.csv"
    df_sucio = leer_csv(ruta_csv_sucio)
    filas_antes = len(df_sucio)
    imprimir_diagnostico(df_sucio, "DIAGNÓSTICO ANTES DE LIMPIAR")
    df_limpio = limpiar(df_sucio)
    imprimir_diagnostico(df_limpio, "DIAGNÓSTICO DESPUÉS DE LIMPIAR")
    print(
        f"\nFilas eliminadas: {filas_antes - len(df_limpio)} ({filas_antes} -> {len(df_limpio)})"
    )
    guardar_limpio(df_limpio, RUTA_LIMPIO)

    print("\n=== 3. INICIANDO CONSULTAS DE INFORMACIÓN (HU Q01) ===")
    df_consultas = cargar_datos_consultas(RUTA_LIMPIO)
    carpeta_destino = RUTA_LIMPIO.parent
    resultados = [
        consulta_1_activas(df_consultas),
        consulta_2_sector(df_consultas, "Logistica"),
        consulta_3_conteo(df_consultas),
        consulta_4_groupby(df_consultas),
        consulta_5_groupby_doble(df_consultas),
    ]
    for num, res in enumerate(resultados, start=1):
        guardar_consulta(res, carpeta_destino, num)

    print("\n=== 4. INICIANDO REPORTE GRÁFICO Y CONCLUSIONES (HU G01) ===")
    df_reporte = cargar_datos_reportes(RUTA_LIMPIO)
    r1, por_sector = grafica_1_por_sector(df_reporte)
    r2, conteo_activa = grafica_2_activas(df_reporte)
    r3, tabla = grafica_3_apiladas(df_reporte)
    print(f"Gráficas creadas en data/reportes:\n  - {r1}\n  - {r2}\n  - {r3}")
    imprimir_conclusiones(df_reporte, por_sector, conteo_activa, tabla)

    print("\n=== PIPELINE INTEGRAL COMPLETO CON ÉXITO ===")


if __name__ == "__main__":
    ejecutar_pipeline_master()