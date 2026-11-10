"""Genera las tres gráficas de la HU G01 sobre la tabla retos y muestra las conclusiones.

Uso:
    python notebook/graficas/graficar_retos.py data/limpio/retos_limpio.csv
"""
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
ARCHIVO_DEFECTO = RAIZ_PROYECTO / "data" / "limpio" / "retos_limpio.csv"
CARPETA_SALIDA = RAIZ_PROYECTO / "data" / "graficas"
DPI = 120


def cargar_datos(ruta):
    """Lee el CSV de retos y convierte las columnas de fecha a tipo fecha."""
    df = pd.read_csv(ruta)
    df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"])
    df["fecha_fin"] = pd.to_datetime(df["fecha_fin"])
    return df


def grafica_estados(df, ruta):
    """Crea la gráfica 1: barras con la cantidad de retos por estado."""
    conteo = df["estado"].value_counts().sort_index()

    plt.figure(figsize=(8, 5))
    conteo.plot(kind="bar", color="steelblue")
    plt.title("Cantidad de retos por estado")
    plt.xlabel("Estado")
    plt.ylabel("Cantidad de retos")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(ruta, dpi=DPI)
    plt.close()
    return conteo


def grafica_meses(df, ruta):
    """Crea la gráfica 2: línea con la cantidad de retos que empiezan cada mes."""
    por_mes = df.groupby(df["fecha_inicio"].dt.to_period("M")).size()
    por_mes.index = por_mes.index.astype(str)

    plt.figure(figsize=(9, 5))
    por_mes.plot(kind="line", marker="o", color="seagreen")
    plt.title("Retos que empiezan cada mes")
    plt.xlabel("Mes de inicio")
    plt.ylabel("Cantidad de retos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(ruta, dpi=DPI)
    plt.close()
    return por_mes


def grafica_duracion(df_valido, ruta):
    """Crea la gráfica 3: histograma de la duración de los retos."""
    plt.figure(figsize=(8, 5))
    df_valido["duracion_dias"].plot(
        kind="hist", bins=20, color="darkorange", edgecolor="white"
    )
    plt.title("Distribución de la duración de los retos")
    plt.xlabel("Duración (días)")
    plt.ylabel("Cantidad de retos")
    plt.tight_layout()
    plt.savefig(ruta, dpi=DPI)
    plt.close()


def calcular_conclusiones(df, df_valido, por_mes):
    """Arma la lista de conclusiones en español a partir de los datos."""
    conclusiones = []

    mes_top = por_mes.idxmax()
    cantidad_top = por_mes.max()
    porcentaje = cantidad_top / len(df) * 100
    conclusiones.append(
        f"Los retos se concentran en {mes_top}, con {cantidad_top} inicios "
        f"({porcentaje:.0f}% del total)."
    )

    if "duracion_dias" in df_valido.columns and not df_valido.empty:
        promedio = df_valido.groupby("estado")["duracion_dias"].mean()
        mediana = df_valido.groupby("estado")["duracion_dias"].median()
        partes = [
            f"{estado} promedia {promedio[estado]:.0f} días "
            f"(mediana {mediana[estado]:.0f})"
            for estado in promedio.index
        ]
        conclusiones.append(
            "Duración promedio según el estado: " + "; ".join(partes) + "."
        )

    invalidos = int((df["fecha_fin"] < df["fecha_inicio"]).sum())
    conclusiones.append(
        f"{invalidos} retos tienen la fecha de fin antes que la de inicio."
    )

    return conclusiones


def main(ruta_entrada=None):
    """Ejecuta el reporte: lee el CSV, crea las tres gráficas e imprime las conclusiones."""
    if ruta_entrada:
        ruta_csv = Path(ruta_entrada)
    elif len(sys.argv) > 1:
        ruta_csv = Path(sys.argv[1])
    else:
        ruta_csv = ARCHIVO_DEFECTO

    if not ruta_csv.exists():
        print(f"⚠️ No se encontró el archivo de retos limpio: {ruta_csv}")
        return

    df = cargar_datos(ruta_csv)
    df_valido = df[df["fecha_fin"] >= df["fecha_inicio"]].copy()
    if "duracion_dias" not in df_valido.columns:
        df_valido["duracion_dias"] = (df_valido["fecha_fin"] - df_valido["fecha_inicio"]).dt.days

    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)
    ruta_1 = CARPETA_SALIDA / "retos_grafica_1.png"
    ruta_2 = CARPETA_SALIDA / "retos_grafica_2.png"
    ruta_3 = CARPETA_SALIDA / "retos_grafica_3.png"

    grafica_estados(df, ruta_1)
    por_mes = grafica_meses(df, ruta_2)
    grafica_duracion(df_valido, ruta_3)

    print("Gráficas de retos generadas:")
    for ruta in (ruta_1, ruta_2, ruta_3):
        print(f"  {ruta}")

    print("\nConclusiones Retos:")
    for i, texto in enumerate(calcular_conclusiones(df, df_valido, por_mes), 1):
        print(f"  {i}. {texto}")


if __name__ == "__main__":
    main()