"""Responde las cinco consultas de la HU Q01 sobre la tabla retos.

Uso:
    python scripts/consultas_retos.py retos_limpio.csv

Lee el CSV limpio, imprime el título y el resultado de cada consulta en orden
y guarda cada resultado como retos_consulta_N.csv en la misma carpeta del CSV.
"""
import os
import sys

import pandas as pd


def consulta_1_en_curso(df, carpeta_salida):
    """Consulta 1: ¿Qué retos están en curso? Filtra las filas con estado EN_CURSO
    y guarda el resultado en retos_consulta_1.csv."""
    print("Consulta 1: ¿Qué retos están en curso?")
    en_curso = df[df["estado"] == "EN_CURSO"]
    print(en_curso.to_string(index=False))
    en_curso.to_csv(os.path.join(carpeta_salida, "retos_consulta_1.csv"), index=False)
    print()


def consulta_2_mas_largos(df, carpeta_salida):
    """Consulta 2: ¿Cuáles son los 10 retos más largos? Usa nlargest sobre
    duracion_dias y guarda el resultado en retos_consulta_2.csv."""
    print("Consulta 2: ¿Cuáles son los 10 retos más largos?")
    largos = df.nlargest(10, "duracion_dias")[["nombre", "duracion_dias", "estado"]]
    print(largos.to_string(index=False))
    largos.to_csv(os.path.join(carpeta_salida, "retos_consulta_2.csv"), index=False)
    print()


def consulta_3_conteo_estado(df, carpeta_salida):
    """Consulta 3: ¿Cuántos retos hay por estado? Cuenta las filas de cada estado
    con value_counts y guarda el resultado en retos_consulta_3.csv."""
    print("Consulta 3: ¿Cuántos retos hay por estado?")
    conteo = (
        df["estado"]
        .value_counts()
        .rename_axis("estado")
        .reset_index(name="cantidad")
    )
    print(conteo.to_string(index=False))
    conteo.to_csv(os.path.join(carpeta_salida, "retos_consulta_3.csv"), index=False)
    print()


def consulta_4_resumen_por_estado(df, carpeta_salida):
    """Consulta 4 (groupby): ¿Cuál es la duración promedio, mínima y máxima de los
    retos por estado? Agrupa por estado y guarda el resultado en retos_consulta_4.csv."""
    print("Consulta 4: ¿Cuál es la duración promedio, mínima y máxima por estado?")
    resumen = df.groupby("estado")["duracion_dias"].agg(["count", "mean", "min", "max"])
    resumen = resumen.rename(
        columns={"count": "cantidad", "mean": "promedio", "min": "minima", "max": "maxima"}
    )
    resumen["promedio"] = resumen["promedio"].round(2)
    resumen = resumen.reset_index()
    print(resumen.to_string(index=False))
    resumen.to_csv(os.path.join(carpeta_salida, "retos_consulta_4.csv"), index=False)
    print()


def consulta_5_por_mes(df, carpeta_salida):
    """Consulta 5 (groupby): ¿Cuántos retos empiezan cada mes? Agrupa por mes de
    fecha_inicio y guarda el resultado en retos_consulta_5.csv."""
    print("Consulta 5: ¿Cuántos retos empiezan cada mes?")
    por_mes = df.groupby(df["fecha_inicio"].dt.to_period("M"))["id"].count()
    por_mes = por_mes.rename_axis("mes").reset_index(name="cantidad")
    por_mes["mes"] = por_mes["mes"].astype(str)
    print(por_mes.to_string(index=False))
    por_mes.to_csv(os.path.join(carpeta_salida, "retos_consulta_5.csv"), index=False)
    print()


def main():
    """Lee retos_limpio.csv desde el argumento de la línea de comandos y ejecuta
    las cinco consultas en orden."""
    if len(sys.argv) != 2:
        print("Uso: python scripts/consultas_retos.py retos_limpio.csv")
        sys.exit(1)

    ruta = sys.argv[1]
    carpeta = os.path.dirname(os.path.abspath(ruta))
    df = pd.read_csv(ruta, parse_dates=["fecha_inicio"])

    consulta_1_en_curso(df, carpeta)
    consulta_2_mas_largos(df, carpeta)
    consulta_3_conteo_estado(df, carpeta)
    consulta_4_resumen_por_estado(df, carpeta)
    consulta_5_por_mes(df, carpeta)


if __name__ == "__main__":
    main()