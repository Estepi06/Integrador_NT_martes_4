"""Genera las tres gráficas de la HU G01 sobre la tabla retos y muestra las conclusiones.

Uso:
    python scripts/reporte_retos.py retos_limpio.csv

Las gráficas se guardan en la carpeta reportes/ (se crea si no existe).
"""
import os
import sys

import matplotlib

# Modo sin ventana: el script solo guarda imágenes, nunca las muestra.
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

CARPETA_REPORTES = "reportes"
DPI = 120


def cargar_datos(ruta):
    """Lee el CSV de retos y convierte las columnas de fecha a tipo fecha.

    Recibe la ruta del archivo CSV y devuelve un DataFrame con las fechas
    listas para calcular meses y duraciones.
    """
    df = pd.read_csv(ruta)
    df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"])
    df["fecha_fin"] = pd.to_datetime(df["fecha_fin"])
    return df


def grafica_estados(df, ruta):
    """Crea la gráfica 1: barras con la cantidad de retos por estado.

    Recibe el DataFrame completo y la ruta donde se guarda la imagen.
    Devuelve la serie con el conteo por estado.
    """
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
    """Crea la gráfica 2: línea con la cantidad de retos que empiezan cada mes.

    Recibe el DataFrame completo y la ruta donde se guarda la imagen.
    Devuelve la serie con el conteo por mes (índice en formato AAAA-MM).
    """
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
    """Crea la gráfica 3: histograma de la duración de los retos.

    Recibe solo los retos con fechas válidas (sin duraciones negativas)
    y la ruta donde se guarda la imagen.
    """
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
    """Arma la lista de conclusiones en español a partir de los datos.

    Responde tres preguntas: en qué mes se concentran los retos, cuánto
    dura en promedio un reto según su estado y cuántos tienen la fecha
    de fin antes que la de inicio.
    Devuelve una lista de textos, uno por conclusión.
    """
    conclusiones = []

    # 1. Mes con más inicios de retos.
    mes_top = por_mes.idxmax()
    cantidad_top = por_mes.max()
    porcentaje = cantidad_top / len(df) * 100
    conclusiones.append(
        f"Los retos se concentran en {mes_top}, con {cantidad_top} inicios "
        f"({porcentaje:.0f}% del total). Los datos no explican la causa; una "
        "posibilidad es que se planeen más retos en ese periodo, pero conviene "
        "validarlo con el equipo."
    )

    # 2. Duración promedio según el estado (solo fechas válidas).
    promedio = df_valido.groupby("estado")["duracion_dias"].mean()
    mediana = df_valido.groupby("estado")["duracion_dias"].median()
    partes = [
        f"{estado} promedia {promedio[estado]:.0f} días "
        f"(mediana {mediana[estado]:.0f})"
        for estado in promedio.index
    ]
    conclusiones.append(
        "Duración promedio según el estado (sin los retos con fechas inválidas): "
        + "; ".join(partes)
        + ". En EN_CURSO la duración es la planeada, no la real."
    )

    # 3. Retos con fecha de fin anterior a la de inicio (dato para el back).
    invalidos = int((df["fecha_fin"] < df["fecha_inicio"]).sum())
    conclusiones.append(
        f"{invalidos} retos tienen la fecha de fin antes que la de inicio. "
        "El back debe corregirlos o marcarlos como inválidos; en este reporte "
        "se excluyeron de la duración."
    )

    return conclusiones


def main():
    """Ejecuta el reporte: lee el CSV, crea las tres gráficas e imprime las conclusiones."""
    if len(sys.argv) < 2:
        print("Uso: python scripts/reporte_retos.py retos_limpio.csv")
        sys.exit(1)

    df = cargar_datos(sys.argv[1])
    df_valido = df[df["fecha_fin"] >= df["fecha_inicio"]]

    os.makedirs(CARPETA_REPORTES, exist_ok=True)
    ruta_1 = os.path.join(CARPETA_REPORTES, "retos_grafica_1.png")
    ruta_2 = os.path.join(CARPETA_REPORTES, "retos_grafica_2.png")
    ruta_3 = os.path.join(CARPETA_REPORTES, "retos_grafica_3.png")

    grafica_estados(df, ruta_1)
    por_mes = grafica_meses(df, ruta_2)
    grafica_duracion(df_valido, ruta_3)

    print("Gráficas generadas:")
    for ruta in (ruta_1, ruta_2, ruta_3):
        print(f"  {ruta}")

    print("\nConclusiones:")
    for i, texto in enumerate(calcular_conclusiones(df, df_valido, por_mes), 1):
        print(f"  {i}. {texto}")


if __name__ == "__main__":
    main()