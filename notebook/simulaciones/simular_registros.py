"""
simular_registros.py
Genera la tabla registros con datos sucios a propósito.
Ejecutar desde la raíz del proyecto: python notebook/simulaciones/simular_registros.py
"""
import random
import uuid
from datetime import datetime

import pandas as pd
from faker import Faker

ESTADOS = ["INSCRITO", "EN PROCESO", "FINALIZADO"]
IDS_USUARIO = [str(uuid.uuid5(uuid.NAMESPACE_DNS, f"usuario-{i}")) for i in range(1000)]
IDS_RETO = [str(uuid.uuid5(uuid.NAMESPACE_DNS, f"reto-{i}")) for i in range(100)]

N_FILAS = 800

# Rango fijo de fechas para que cada ejecución genere lo mismo (en vez de "now")
FECHA_INICIO = datetime(2025, 11, 3)
FECHA_FIN = datetime(2026, 11, 3)


def generar_registros(n=N_FILAS):
    """Crea el DataFrame de registros y le mete la suciedad que pide la HU."""
    Faker.seed(42)
    random.seed(42)
    fake = Faker("es_ES")

    filas = []
    for _ in range(n):
        filas.append({
            # UUID v4 generado con la semilla fija, para que sea reproducible
            "id": str(uuid.UUID(int=random.getrandbits(128), version=4)),
            "fecha_registro": fake.date_time_between(start_date=FECHA_INICIO, end_date=FECHA_FIN),
            "observacion": fake.sentence(nb_words=10),
            "estado": random.choice(ESTADOS),
            "id_usuario": random.choice(IDS_USUARIO),
            "id_reto": random.choice(IDS_RETO),
        })
    df = pd.DataFrame(filas)

    # 1. fecha_registro: dos formatos mezclados (50 % y 50 %)
    df["fecha_registro"] = [
        f.strftime("%Y-%m-%d %H:%M:%S") if random.random() < 0.5 else f.strftime("%d/%m/%Y %H:%M")
        for f in df["fecha_registro"]
    ]

    # 2. estado: variantes de escritura en ~30 % de las filas
    for i in random.sample(range(n), int(n * 0.30)):
        if df.at[i, "estado"] == "INSCRITO":
            df.at[i, "estado"] = "inscrito"
        elif df.at[i, "estado"] == "FINALIZADO":
            df.at[i, "estado"] = " Finalizado "

    # 3. observacion: 20 % nulos
    for i in random.sample(range(n), int(n * 0.20)):
        df.at[i, "observacion"] = None

    # 4. Par id_usuario + id_reto repetido: 40 filas copian el par de otras 40 (≈10 % de las filas)
    filas_par = random.sample(range(n), 40)
    filas_origen_par = random.sample([i for i in range(n) if i not in filas_par], 40)
    for destino, origen in zip(filas_par, filas_origen_par):
        df.at[destino, "id_usuario"] = df.at[origen, "id_usuario"]
        df.at[destino, "id_reto"] = df.at[origen, "id_reto"]

    # 5. Duplicados exactos: 40 filas (5 %) se reemplazan por copias de otras filas intactas
    usadas = set(filas_par) | set(filas_origen_par)
    filas_copia = random.sample([i for i in range(n) if i not in usadas], 40)
    origenes_copia = random.sample([i for i in range(n) if i not in usadas and i not in filas_copia], 40)
    for destino, origen in zip(filas_copia, origenes_copia):
        df.iloc[destino] = df.iloc[origen].values

    return df


def main():
    """Genera la tabla y muestra forma, primeras filas y nulos para revisar que quedó sucia."""
    df = generar_registros()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())


if __name__ == "__main__":
    main()
