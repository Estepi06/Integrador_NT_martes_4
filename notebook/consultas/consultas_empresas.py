"""Consultas de la HU Q01 sobre la tabla empresas (archivo LIMPIO).

Uso:
    python notebook/consultas/consultas_empresas.py data/limpio/empresas_limpio.csv [sector]
"""

import sys
from pathlib import Path
import pandas as pd

SECTOR_POR_DEFECTO = "Logistica"

def cargar_datos(ruta):
    """Lee el CSV limpio. NIT y teléfono se leen como texto para no perder
    los ceros iniciales; 'activa' se asegura como booleano."""
    df = pd.read_csv(ruta, dtype={"id": str, "nit": str, "telefono": str})
    if df["activa"].dtype != bool:
        df["activa"] = df["activa"].astype(str).str.strip().str.lower().eq("true")
    return df

def guardar(resultado, carpeta, numero):
    """Guarda el resultado de una consulta como empresas_consulta_N.csv
    (con el índice cuando el resultado es un conteo o una tabla agrupada)."""
    ruta = carpeta / f"empresas_consulta_{numero}.csv"
    con_indice = not isinstance(resultado.index, pd.RangeIndex)
    resultado.to_csv(ruta, index=con_indice)
    return ruta

def consulta_1_activas(df):
    """Consulta 1: devuelve las empresas activas (activa == True)."""
    print("\n=== Consulta 1: ¿Cuáles son las empresas activas? ===")
    activas = df[df["activa"] == True]  # noqa: E712
    print(activas)
    print(f"Total activas: {len(activas)}")
    return activas

def consulta_2_sector(df, sector):
    """Consulta 2: devuelve las empresas de un sector, ordenadas por nombre."""
    print(f"\n=== Consulta 2: ¿Cuáles son las empresas del sector {sector}, ordenadas por nombre? ===")
    logistica = df[df["sector"] == sector].sort_values("nombre")
    if logistica.empty:
        print(f"No hay empresas en el sector '{sector}'.")
        print("Sectores disponibles: " + ", ".join(sorted(df["sector"].unique())))
    else:
        print(logistica)
    return logistica

def consulta_3_conteo(df):
    """Consulta 3: conteo rápido de empresas por sector con value_counts."""
    print("\n=== Consulta 3: ¿Cuántas empresas hay por sector (conteo rápido)? ===")
    conteo = df["sector"].value_counts()
    print(conteo)
    return conteo

def consulta_4_groupby(df):
    """Consulta 4 (groupby): empresas por sector, de mayor a menor."""
    print("\n=== Consulta 4: ¿Cuántas empresas hay por sector, de mayor a menor? (groupby) ===")
    por_sector = df.groupby("sector")["id"].count().sort_values(ascending=False)
    print(por_sector)
    return por_sector

def consulta_5_groupby_doble(df):
    """Consulta 5 (groupby doble): activas e inactivas por sector."""
    print("\n=== Consulta 5: ¿Cuántas empresas activas e inactivas hay por sector? (groupby doble) ===")
    tabla = df.groupby(["sector", "activa"])["id"].count().unstack(fill_value=0)
    print(tabla)
    return tabla

def main():
    """Lee el CSV, ejecuta las cinco consultas en orden y guarda los resultados."""
    if len(sys.argv) < 2:
        print("Uso: python notebook/consultas/consultas_empresas.py data/limpio/empresas_limpio.csv [sector]")
        sys.exit(1)

    ruta = Path(sys.argv[1])
    sector = sys.argv[2] if len(sys.argv) > 2 else SECTOR_POR_DEFECTO

    if not ruta.exists():
        print(f"No se encontró el archivo: {ruta}")
        sys.exit(1)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_colwidth", 32)
    pd.set_option("display.max_rows", 15)

    df = cargar_datos(ruta)
    carpeta = ruta.parent

    resultados = [
        consulta_1_activas(df),
        consulta_2_sector(df, sector),
        consulta_3_conteo(df),
        consulta_4_groupby(df),
        consulta_5_groupby_doble(df),
    ]

    print("\nArchivos guardados:")
    for numero, resultado in enumerate(resultados, start=1):
        print(f"  {guardar(resultado, carpeta, numero)}")

if __name__ == "__main__":
    main()