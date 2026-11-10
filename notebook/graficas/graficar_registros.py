"""
graficar_registros.py
Genera tres gráficas PNG en data/graficas/ y las conclusiones a partir de data/limpio/registros_limpio.csv.
Ejecutar desde la raíz del proyecto: python notebook/graficas/graficar_registros.py
"""
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # sin ventanas: el script no se queda esperando
import matplotlib.pyplot as plt
import pandas as pd

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_DEFECTO = RAIZ_PROYECTO / "data" / "limpio" / "registros_limpio.csv"
CARPETA_SALIDA = RAIZ_PROYECTO / "data" / "graficas"


def guardar_grafica(numero):
    """Guarda la figura activa en data/graficas/ y la cierra."""
    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)
    ruta = CARPETA_SALIDA / f"registros_grafica_{numero}.png"
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica guardada: {ruta}")


def main(ruta_entrada=None):
    if ruta_entrada:
        ruta_csv = Path(ruta_entrada)
    elif len(sys.argv) > 1:
        ruta_csv = Path(sys.argv[1])
    else:
        ruta_csv = RUTA_DEFECTO

    if not ruta_csv.exists():
        print(f"⚠️ No se encontró el archivo de registros limpio: {ruta_csv}")
        return

    df = pd.read_csv(ruta_csv, encoding="utf-8")
    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)

    conteo = df["estado"].value_counts()
    por_mes = df.groupby("mes")["id"].count()
    top_retos = df.groupby("id_reto")["id"].count().nlargest(10)

    # Gráfica 1: barras por estado
    plt.figure()
    conteo.plot(kind="bar")
    plt.title("Participaciones por estado")
    plt.xlabel("Estado")
    plt.ylabel("Participaciones")
    guardar_grafica(1)

    # Gráfica 2: línea por mes
    plt.figure()
    por_mes.plot(kind="line", marker="o")
    plt.title("Participaciones por mes")
    plt.xlabel("Mes")
    plt.ylabel("Participaciones")
    guardar_grafica(2)

    # Gráfica 3: barras horizontales de los 10 retos con más participantes
    plt.figure()
    top_retos.plot(kind="barh")
    plt.title("Los 10 retos con más participantes")
    plt.xlabel("Participaciones")
    plt.ylabel("Reto (id)")
    guardar_grafica(3)

    # Conclusiones
    reto_top = top_retos.index[0] if not top_retos.empty else "N/A"
    print("\n--- Conclusiones Registros ---")
    print(f"El reto más popular es {reto_top} con {top_retos.iloc[0]} participaciones.")
    print(f"El mes con más inscripciones fue {por_mes.idxmax()} con {por_mes.max()} participaciones.")

    repetidos = df[df.duplicated(subset=["id_usuario", "id_reto"], keep=False)]
    grupos = repetidos.groupby(["id_usuario", "id_reto"]).ngroups
    print(f"Se encontraron {len(repetidos)} inscripciones duplicadas en {grupos} pares usuario-reto.")


if __name__ == "__main__":
    main()