"""Reporte gráfico de la HU G01 sobre la tabla empresas (archivo LIMPIO).

Uso:
    python notebook/graficas/graficar_empresas.py data/limpio/empresas_limpio.csv
"""

import os
import sys
from pathlib import Path
import matplotlib

matplotlib.use("Agg")  # Modo sin ventana para ejecución continua
import matplotlib.pyplot as plt
import pandas as pd

# Definición dinámica de rutas
RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
CARPETA = RAIZ_PROYECTO / "data" / "graficas"
ARCHIVO_DEFECTO = RAIZ_PROYECTO / "data" / "limpio" / "empresas_limpio.csv"


def cargar_datos(ruta):
    """Lee el CSV limpio y asegura que 'activa' y 'correo_valido' sean booleanos."""
    df = pd.read_csv(ruta, dtype={"id": str, "nit": str, "telefono": str})
    for columna in ("activa", "correo_valido"):
        if columna in df.columns and df[columna].dtype != bool:
            df[columna] = df[columna].astype(str).str.strip().str.lower().eq("true")
    return df


def guardar(nombre):
    """Aplica tight_layout, asegura la existencia de data/graficas, guarda con dpi=120,
    cierra la figura y devuelve la ruta del archivo.
    """
    plt.tight_layout()
    os.makedirs(CARPETA, exist_ok=True)
    ruta = CARPETA / nombre
    plt.savefig(ruta, dpi=120)
    plt.close()
    return ruta


def grafica_1_por_sector(df):
    """Grafica 1 (barras): cantidad de empresas por sector."""
    por_sector = df.groupby("sector")["id"].count().sort_values(ascending=False)
    plt.figure(figsize=(9, 5))
    por_sector.plot(kind="bar", color="#3b7dd8")
    plt.title("Cantidad de empresas por sector")
    plt.xlabel("Sector")
    plt.ylabel("Número de empresas")
    plt.xticks(rotation=45, ha="right")
    return guardar("empresas_grafica_1.png"), por_sector


def grafica_2_activas(df):
    """Grafica 2 (torta): empresas activas vs inactivas."""
    conteo = df["activa"].map({True: "Activas", False: "Inactivas"}).value_counts()
    plt.figure(figsize=(6, 6))
    conteo.plot(kind="pie", autopct="%1.1f%%", colors=["#3b7dd8", "#e08a3c"])
    plt.title("Empresas activas vs inactivas")
    plt.xlabel("Estado de la empresa")
    plt.ylabel("Proporción de empresas")
    return guardar("empresas_grafica_2.png"), conteo


def grafica_3_apiladas(df):
    """Grafica 3 (barras apiladas): activas e inactivas por sector."""
    tabla = df.groupby(["sector", "activa"])["id"].count().unstack(fill_value=0)
    tabla = tabla.rename(columns={False: "Inactivas", True: "Activas"})
    for col in ["Activas", "Inactivas"]:
        if col not in tabla.columns:
            tabla[col] = 0
    tabla = tabla[["Activas", "Inactivas"]]
    plt.figure(figsize=(9, 5))
    tabla.plot(kind="bar", stacked=True, color=["#3b7dd8", "#e08a3c"], ax=plt.gca())
    plt.title("Empresas activas e inactivas por sector")
    plt.xlabel("Sector")
    plt.ylabel("Número de empresas")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Estado")
    return guardar("empresas_grafica_3.png"), tabla


def imprimir_conclusiones(df, por_sector, conteo_activa, tabla):
    """Calcula e imprime las conclusiones dinámicas a partir de los datos."""
    total = len(df)
    sector_top = por_sector.index[0]
    cantidad_top = por_sector.iloc[0]
    inactivas = int(conteo_activa.get("Inactivas", 0))
    pct_inactivas = (inactivas / total * 100) if total > 0 else 0

    invalidos = int((~df["correo_valido"]).sum()) if "correo_valido" in df.columns else 0
    pct_invalidos = (invalidos / total * 100) if total > 0 else 0

    suma_filas = tabla.sum(axis=1)
    tabla_pct = (tabla["Inactivas"] / suma_filas * 100).fillna(0)
    peor = tabla_pct.idxmax() if not tabla_pct.empty else "N/A"

    print("\n=== Conclusiones Empresas ===")
    print(
        f"1. El sector con más empresas registradas es {sector_top} "
        f"({cantidad_top} de {total}, {cantidad_top / total * 100:.1f}%)."
    )
    print(
        f"2. {inactivas} empresas están inactivas ({pct_inactivas:.1f}%). "
        f"El sector con mayor proporción de inactivas es {peor} "
        f"({tabla_pct.get(peor, 0):.1f}%)."
    )
    if "correo_valido" in df.columns:
        print(
            f"3. Aparecieron {invalidos} correos inválidos ({pct_invalidos:.1f}%)."
        )


def main(ruta_entrada=None):
    """Punto de entrada general para consola o pipeline main.py."""
    if ruta_entrada:
        ruta_csv = Path(ruta_entrada)
    elif len(sys.argv) > 1:
        ruta_csv = Path(sys.argv[1])
    else:
        ruta_csv = ARCHIVO_DEFECTO

    if not ruta_csv.exists():
        print(f"⚠️ No se encontró el archivo de empresas limpio: {ruta_csv}")
        return

    os.makedirs(CARPETA, exist_ok=True)
    df = cargar_datos(ruta_csv)

    ruta1, por_sector = grafica_1_por_sector(df)
    ruta2, conteo_activa = grafica_2_activas(df)
    ruta3, tabla = grafica_3_apiladas(df)

    print("Gráficas de empresas guardadas:")
    for ruta in (ruta1, ruta2, ruta3):
        print(f"  {ruta}")

    imprimir_conclusiones(df, por_sector, conteo_activa, tabla)


if __name__ == "__main__":
    main()