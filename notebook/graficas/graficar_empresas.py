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

# Definición dinámica de la ruta de salida en data/graficas/
RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
CARPETA = RAIZ_PROYECTO / "data" / "graficas"


def cargar_datos(ruta):
    """Lee el CSV limpio y asegura que 'activa' y 'correo_valido' sean booleanos."""
    df = pd.read_csv(ruta, dtype={"id": str, "nit": str, "telefono": str})
    for columna in ("activa", "correo_valido"):
        if df[columna].dtype != bool:
            df[columna] = df[columna].astype(str).str.strip().str.lower().eq("true")
    return df


def guardar(nombre):
    """Aplica tight_layout, asegura la existencia de data/graficas, guarda con dpi=120,
    cierra la figura y devuelve la ruta del archivo.
    """
    plt.tight_layout()
    os.makedirs(CARPETA, exist_ok=True)  # Crea data/graficas si no existe
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
    pct_inactivas = inactivas / total * 100
    invalidos = int((~df["correo_valido"]).sum())
    pct_invalidos = invalidos / total * 100
    tabla_pct = tabla["Inactivas"] / tabla.sum(axis=1) * 100
    peor = tabla_pct.idxmax()

    print("\n=== Conclusiones ===")
    print(
        f"1. El sector con más empresas registradas es {sector_top} "
        f"({cantidad_top} de {total}, {cantidad_top / total * 100:.1f}%)."
    )
    print(
        f"2. {inactivas} empresas están inactivas ({pct_inactivas:.1f}%). "
        "Para la plataforma significa que esa proporción del registro no "
        "genera actividad: infla las cifras, hay que decidir si se depura "
        "o se reactiva, y conviene vigilarla. "
        f"El sector con mayor proporción de inactivas es {peor} "
        f"({tabla_pct[peor]:.1f}%)."
    )
    print(
        f"3. Aparecieron {invalidos} correos inválidos ({pct_invalidos:.1f}%). "
        "Hay que validarlos en el back porque la validación del front se "
        "puede saltar (otro cliente, la API directa, datos importados), y un "
        "correo malo rompe notificaciones y recuperación de cuentas."
    )


def main():
    """Lee el CSV, crea las tres gráficas, imprime sus rutas y las conclusiones."""
    if len(sys.argv) < 2:
        print(
            "Uso: python notebook/graficas/graficar_empresas.py"
            " data/limpio/empresas_limpio.csv"
        )
        sys.exit(1)

    ruta_csv = Path(sys.argv[1])
    if not ruta_csv.exists():
        print(f"No se encontró el archivo: {ruta_csv}")
        sys.exit(1)

    os.makedirs(CARPETA, exist_ok=True)
    df = cargar_datos(ruta_csv)

    ruta1, por_sector = grafica_1_por_sector(df)
    ruta2, conteo_activa = grafica_2_activas(df)
    ruta3, tabla = grafica_3_apiladas(df)

    print("Gráficas guardadas:")
    for ruta in (ruta1, ruta2, ruta3):
        print(f"  {ruta}")

    imprimir_conclusiones(df, por_sector, conteo_activa, tabla)


if __name__ == "__main__":
    main()