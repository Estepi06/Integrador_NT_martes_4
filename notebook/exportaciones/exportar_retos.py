#rutina para convertir una lista de diccionarios en múltiples fuentes de información

import json
from pathlib import Path
from textwrap import indent

#1. configuracion (cambiar segun la tabla)
NOMBRE_ENTIDAD="retos"

CARPETA_PROYECTO=Path(__file__).resolve().parents[2]
CARPETA_CRUDOS= CARPETA_PROYECTO/"datos"/"crudos"
CARPETA_LIMPIOS= CARPETA_PROYECTO/"datos"/"limpios"
CARPETA_REPORTES= CARPETA_PROYECTO/"datos"/"reportes"

#2 Funciones genericas para crear los archivos 

#2.1 Crear carpeta si no existe
def preparar_carpeta(carpeta):
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta

#2.2 exportar a CSV
def exportar_csv(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta)/ f"{nombre_archivo}.csv"
    datos_df.to_csv(ruta, index=False, sep=";", encoding="utf-8-sig")
    return ruta

#2.3 exportar a jason

def exportar_json(datos_df,carpeta,nombre_archivo):
    ruta = preparar_carpeta(carpeta)/ f"{nombre_archivo}.json"
    datos_df.to_json(ruta, orient="records", date_format="iso", indent=2)
    return ruta

#2.4 esportar a excel 

def exportar_excel(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta)/f"{nombre_archivo}.xlsx"
    datos_df.to_excel(ruta, index=False, engine="openpyxl")
    return ruta

#3 genero los archivos en el proyecto
def exportar_retos_crudos(datos_sucios_df):
    return[
        #llamar la funcion crudo
        exportar_csv(datos_sucios_df, CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo"),
        #llamar la funcion json
        exportar_json(datos_sucios_df, CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo"),
        #llamar la funcion excel
        exportar_excel(datos_sucios_df, CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo")
    ]
