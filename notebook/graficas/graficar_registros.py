"""
graficar_registros.py
Genera tres gráficas PNG en reportes/ y las conclusiones a partir de data/limpio/registros_limpio.csv.
Ejecutar desde la raíz del proyecto: python notebook/graficas/graficar_registros.py
"""
import os

import matplotlib

matplotlib.use("Agg")  # sin ventanas: el script no se queda esperando
import matplotlib.pyplot as plt
import pandas as pd

RUTA_LIMPIO = os.path.join("data", "limpio", "registros_limpio.csv")
CARPETA_REPORTES = "reportes"


def guardar_grafica(numero):
    """Guarda la figura activa como reportes/registros_grafica_N.png y la cierra."""
    ruta = os.path.join(CARPETA_REPORTES, f"registros_grafica_{numero}.png")
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica guardada: {ruta}")


def main():
    df = pd.read_csv(RUTA_LIMPIO, encoding="utf-8")
    os.makedirs(CARPETA_REPORTES, exist_ok=True)

    conteo = df["estado"].value_counts()
    por_mes = df.groupby("mes")["id"].count()
    top_retos = df.groupby("id_reto")["id"].count().nlargest(10)

    # Gráfica 1: barras por estado
    conteo.plot(kind="bar")
    plt.title("Participaciones por estado")
    plt.xlabel("Estado")
    plt.ylabel("Participaciones")
    guardar_grafica(1)

    # Gráfica 2: línea por mes
    por_mes.plot(kind="line", marker="o")
    plt.title("Participaciones por mes")
    plt.xlabel("Mes")
    plt.ylabel("Participaciones")
    guardar_grafica(2)

    # Gráfica 3: barras horizontales de los 10 retos con más participantes
    top_retos.plot(kind="barh")
    plt.title("Los 10 retos con más participantes")
    plt.xlabel("Participaciones")
    plt.ylabel("Reto (id)")
    guardar_grafica(3)

    # Conclusiones
    reto_top = top_retos.index[0]
    print("\n--- Conclusiones ---")
    print(f"El reto más popular es {reto_top} con {top_retos.iloc[0]} participaciones.")
    print(f"El mes con más inscripciones fue {por_mes.idxmax()} con {por_mes.max()} participaciones.")

    repetidos = df[df.duplicated(subset=["id_usuario", "id_reto"], keep=False)]
    grupos = repetidos.groupby(["id_usuario", "id_reto"]).ngroups
    print(f"Se encontraron {len(repetidos)} inscripciones duplicadas en {grupos} pares usuario-reto.")
    print("El back debe bloquearlas con 409 Conflict porque un mismo usuario no puede inscribirse "
          "dos veces en el mismo reto.")


if __name__ == "__main__":
    main()
