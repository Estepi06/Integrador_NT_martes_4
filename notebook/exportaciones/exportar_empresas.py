import os
import sys
from pathlib import Path
import pandas as pd

# Garantizar que la raíz del proyecto esté en sys.path para importaciones relativas
CARPETA_EXPORTACIONES = Path(__file__).resolve().parent
CARPETA_PROYECTO = CARPETA_EXPORTACIONES.parents[1]
if str(CARPETA_PROYECTO) not in sys.path:
    sys.path.append(str(CARPETA_PROYECTO))

# Importación ajustada de la función generadora
from notebook.simulaciones.simular_empresas import generar_empresas

# 1. Configuración (tabla de empresas)
NOMBRE_ENTIDAD = "empresas_sucio"
CARPETA_CRUDOS = CARPETA_PROYECTO / "data" / "crudo"


# 2. Funciones genéricas para exportación
def preparar_carpeta(carpeta: Path):
    os.makedirs(carpeta, exist_ok=True)
    return carpeta


def exportar_csv(datos_df: pd.DataFrame, carpeta: Path, nombre_archivo: str):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.csv"
    datos_df.to_csv(ruta, index=False, encoding="utf-8")
    print(f"Exportado CSV: {ruta} | Shape: {datos_df.shape}")
    return ruta


def exportar_json(datos_df: pd.DataFrame, carpeta: Path, nombre_archivo: str):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.json"
    datos_df.to_json(ruta, orient="records", force_ascii=False, indent=2)
    print(f"Exportado JSON: {ruta} | Shape: {datos_df.shape}")
    return ruta


def exportar_excel(datos_df: pd.DataFrame, carpeta: Path, nombre_archivo: str):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.xlsx"
    datos_df.to_excel(ruta, index=False, sheet_name="empresas", engine="openpyxl")
    print(f"Exportado Excel: {ruta} | Shape: {datos_df.shape}")
    return ruta


# 3. Función principal de exportación
def exportar_empresas_crudos():
    datos_sucios_df = generar_empresas()

    return [
        exportar_csv(datos_sucios_df, CARPETA_CRUDOS, NOMBRE_ENTIDAD),
        exportar_json(datos_sucios_df, CARPETA_CRUDOS, NOMBRE_ENTIDAD),
        exportar_excel(datos_sucios_df, CARPETA_CRUDOS, NOMBRE_ENTIDAD),
    ]


if __name__ == "__main__":
    exportar_empresas_crudos()