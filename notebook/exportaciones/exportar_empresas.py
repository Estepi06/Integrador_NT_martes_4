# rutina para convertir una lista de diccionarios en múltiples fuentes de información

import os
from pathlib import Path
import pandas as pd

# Importación ajustada al módulo completo de la carpeta simulaciones
from notebook.simulaciones.simular_empresas import generar_empresas

# 1. configuracion (cambiar segun la tabla)
NOMBRE_ENTIDAD = "empresas_sucio"

# Ajuste de ruta a la carpeta data/crudo desde la raíz del proyecto
CARPETA_EXPORTACIONES = Path(__file__).resolve().parent
CARPETA_PROYECTO = CARPETA_EXPORTACIONES.parents[1]
CARPETA_CRUDOS = CARPETA_PROYECTO / "data" / "crudo"

# 2 Funciones genericas para crear los archivos 

# 2.1 Crear carpeta si no existe
def preparar_carpeta(carpeta: Path):
    os.makedirs(carpeta, exist_ok=True)
    return carpeta

# 2.2 exportar a CSV
def exportar_csv(datos_df: pd.DataFrame, carpeta: Path, nombre_archivo: str):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.csv"
    datos_df.to_csv(ruta, index=False, encoding="utf-8")
    print(f"Exportado CSV: {ruta} | Shape: {datos_df.shape}")
    return ruta

# 2.3 exportar a json
def exportar_json(datos_df: pd.DataFrame, carpeta: Path, nombre_archivo: str):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.json"
    datos_df.to_json(ruta, orient="records", force_ascii=False, indent=2)
    print(f"Exportado JSON: {ruta} | Shape: {datos_df.shape}")
    return ruta

# 2.4 exportar a excel 
def exportar_excel(datos_df: pd.DataFrame, carpeta: Path, nombre_archivo: str):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.xlsx"
    datos_df.to_excel(ruta, index=False, sheet_name="empresas", engine="openpyxl")
    print(f"Exportado Excel: {ruta} | Shape: {datos_df.shape}")
    return ruta

# 3 genero los archivos en el proyecto
def exportar_empresas_crudos():
    datos_sucios_df = generar_empresas()
    
    return [
        exportar_csv(datos_sucios_df, CARPETA_CRUDOS, NOMBRE_ENTIDAD),
        exportar_json(datos_sucios_df, CARPETA_CRUDOS, NOMBRE_ENTIDAD),
        exportar_excel(datos_sucios_df, CARPETA_CRUDOS, NOMBRE_ENTIDAD)
    ]

if __name__ == "__main__":
    exportar_empresas_crudos()