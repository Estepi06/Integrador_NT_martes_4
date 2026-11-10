"""
consultas_registros.py
Responde cinco preguntas sobre data/limpio/registros_limpio.csv y guarda cada resultado.
Ejecutar desde la raíz del proyecto: python notebook/consultas/consultas_registros.py
"""
import os

import pandas as pd

RUTA_LIMPIO = os.path.join("data", "limpio", "registros_limpio.csv")
CARPETA_LIMPIO = os.path.join("data", "limpio")


def guardar(resultado, numero):
    """Guarda el resultado de una consulta como data/limpio/registros_consulta_N.csv."""
    tabla = resultado.reset_index() if isinstance(resultado, pd.Series) else resultado
    ruta = os.path.join(CARPETA_LIMPIO, f"registros_consulta_{numero}.csv")
    tabla.to_csv(ruta, index=False, encoding="utf-8")
    print(f"Guardado: {ruta} ({len(tabla)} filas)")


def consulta_1(df):
    print("\n1. ¿Cuántas participaciones ya están finalizadas?")
    finalizados = df[df["estado"] == "FINALIZADO"]
    print(f"Total finalizadas: {len(finalizados)}")
    guardar(finalizados, 1)


def consulta_2(df):
    print("\n2. ¿Qué participaciones están repetidas (mismo usuario en el mismo reto)?")
    repetidos = df[df.duplicated(subset=["id_usuario", "id_reto"], keep=False)]
    grupos = repetidos.groupby(["id_usuario", "id_reto"]).ngroups
    print(f"Filas repetidas: {len(repetidos)} en {grupos} pares usuario-reto")
    guardar(repetidos, 2)


def consulta_3(df):
    print("\n3. ¿Cuántas participaciones hay por estado?")
    conteo = df["estado"].value_counts()
    print(conteo)
    guardar(conteo, 3)


def consulta_4(df):
    print("\n4. ¿Cuáles son los 10 retos con más participantes?")
    top_retos = df.groupby("id_reto")["id"].count().nlargest(10)
    print(top_retos)
    guardar(top_retos, 4)


def consulta_5(df):
    print("\n5. ¿Cuántas participaciones hubo cada mes?")
    por_mes = df.groupby("mes")["id"].count()
    print(por_mes)
    guardar(por_mes, 5)


def main():
    df = pd.read_csv(RUTA_LIMPIO, encoding="utf-8")
    os.makedirs(CARPETA_LIMPIO, exist_ok=True)

    consulta_1(df)
    consulta_2(df)
    consulta_3(df)
    consulta_4(df)
    consulta_5(df)


if __name__ == "__main__":
    main()
