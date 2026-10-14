import random
import uuid
from faker import Faker
import pandas as pd

# Configuración del faker a la región que necesito
fake = Faker('es_CO')

# Sembrar semillas para mantener coherencia en los datos simulados
Faker.seed(42)
random.seed(42)

ESTADOS = ['PENDIENTE', 'EN PROCESO', 'FINALIZADO']
ESTADOS_SUCIOS = ['inscrito', 'EN PROCESO', ' Finalizado ']
IDS_USUARIO = [str(uuid.uuid4()) for _ in range(400)]
IDS_RETO = [str(uuid.uuid4()) for _ in range(200)]


def generar_datos_limpios(numero_datos=8000):
    filas = []
    for _ in range(numero_datos):
        filas.append({
            'id': str(uuid.uuid4()),
            'fecha_registro': fake.date_time_between(start_date='-2y', end_date='now'),
            'observaciones': fake.sentence(nb_words=10),
            'estado': random.choice(ESTADOS),
            'id_usuario': random.choice(IDS_USUARIO),
            'id_reto': random.choice(IDS_RETO),
        })
    return pd.DataFrame(filas)


def generar_muestras(datos, porcentaje):
    cantidad = max(1, int(len(datos) * porcentaje))
    return datos.sample(n=cantidad, random_state=random.randint(0, 999)).index


def ensuciar_datos(datos_df):
    datos_df = datos_df.copy()

    # 20% de observaciones como nulos
    filas_elegidas = generar_muestras(datos_df, 0.20)
    datos_df.loc[filas_elegidas, 'observaciones'] = None

    # Estado con variantes inconsistentes
    filas_elegidas = generar_muestras(datos_df, 0.10)
    datos_df.loc[filas_elegidas, 'estado'] = [
        random.choice(ESTADOS_SUCIOS) for _ in filas_elegidas
    ]

    # Fecha mezclando ISO y formato latino
    fechas_latinas = datos_df['fecha_registro'].dt.strftime('%d/%m/%Y %H:%M')
    datos_df['fecha_registro'] = datos_df['fecha_registro'].dt.strftime(
        '%Y-%m-%d %H:%M:%S'
    )
    filas_elegidas = generar_muestras(datos_df, 0.40)
    datos_df.loc[filas_elegidas, 'fecha_registro'] = fechas_latinas.loc[
        filas_elegidas
    ]

    # 10% repite combinacion usuario-reto existente
    filas_elegidas = generar_muestras(datos_df, 0.10)
    filas_disponibles = datos_df.drop(index=filas_elegidas)
    filas_referencia = filas_disponibles.sample(
        n=len(filas_elegidas),
        replace=True,
        random_state=random.randint(0, 999),
    )
    datos_df.loc[filas_elegidas, ['id_usuario', 'id_reto']] = filas_referencia[
        ['id_usuario', 'id_reto']
    ].to_numpy()

    # 5% de filas duplicadas
    df_duplicados = datos_df.sample(
        frac=0.05,
        random_state=random.randint(0, 999),
    )
    datos_df = pd.concat([datos_df, df_duplicados], ignore_index=True)

    return datos_df


def generar_registros(n=8000):
    """Genera un DataFrame de registros simulados con ruido controlado."""
    df_limpio = generar_datos_limpios(numero_datos=n)
    return ensuciar_datos(df_limpio)


if __name__ == '__main__':
    df = generar_registros()
    print(df.head())
    print(f'Filas generadas: {len(df)}')
    print('\nValores nulos por columna:')
    print(df.isna().sum())


