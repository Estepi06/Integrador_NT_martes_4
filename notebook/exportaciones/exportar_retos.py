#rutina para convertir la tabla retos simulada en tres archivos crudos (csv, xlsx y json)
#Ejecutar desde la raíz del proyecto:  python src/exportar_retos.py

import os
from importlib import import_module

#1. Importar la función de simulación (no se vuelve a copiar la generación)
simular_retos = import_module("simular_retos")

#2. Configuración
CARPETA_CRUDO = "data/crudo"
NOMBRE_ARCHIVO = "retos_sucio"


#3. Funciones para crear los archivos
def exportar_csv(df, ruta):
    df.to_csv(ruta, index=False, encoding="utf-8")
    return ruta

def exportar_xlsx(df, ruta):
    df.to_excel(ruta, index=False, sheet_name="retos")
    return ruta

def exportar_json(df, ruta):
    df.to_json(ruta, orient="records", force_ascii=False, indent=2)
    return ruta


#4. Generar la tabla y guardar los tres archivos
def main():
    os.makedirs(CARPETA_CRUDO, exist_ok=True)
    df = simular_retos.generar_retos()

    rutas = [
        exportar_csv(df, os.path.join(CARPETA_CRUDO, f"{NOMBRE_ARCHIVO}.csv")),
        exportar_xlsx(df, os.path.join(CARPETA_CRUDO, f"{NOMBRE_ARCHIVO}.xlsx")),
        exportar_json(df, os.path.join(CARPETA_CRUDO, f"{NOMBRE_ARCHIVO}.json")),
    ]

    for ruta in rutas:
        print(f"{ruta} -> {os.path.getsize(ruta)} bytes, filas x columnas: {df.shape}")


if __name__ == "__main__":
    main()