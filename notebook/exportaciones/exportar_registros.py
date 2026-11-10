"""
exportar_registros.py
Genera los archivos crudos de registros (CSV, XLSX y JSON) en data/crudo/.
Ejecutar desde la raíz del proyecto: python notebook/exportaciones/exportar_registros.py
"""
import os
import sys
from importlib import import_module

# La función generar_registros vive en simular_registros
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "simulaciones"))
simular = import_module("simular_registros")

CARPETA_CRUDO = os.path.join("data", "crudo")


def main():
    os.makedirs(CARPETA_CRUDO, exist_ok=True)

    df = simular.generar_registros(800)

    ruta_csv = os.path.join(CARPETA_CRUDO, "registros_sucio.csv")
    ruta_xlsx = os.path.join(CARPETA_CRUDO, "registros_sucio.xlsx")
    ruta_json = os.path.join(CARPETA_CRUDO, "registros_sucio.json")

    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    df.to_excel(ruta_xlsx, index=False, sheet_name="registros")
    df.to_json(ruta_json, orient="records", force_ascii=False, indent=2)

    for ruta in [ruta_csv, ruta_xlsx, ruta_json]:
        print(f"{ruta} | tamaño: {os.path.getsize(ruta):,} bytes | filas x columnas: {df.shape}")


if __name__ == "__main__":
    main()
