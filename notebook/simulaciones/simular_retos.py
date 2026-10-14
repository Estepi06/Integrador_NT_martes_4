'''El elemento central: la necesidad que publica la empresa. 
Crea el script `src/simular_retos.py`. Con la libreria **Faker** genera 500 filas falsas de la tabla `retos`, 
con las MISMAS columnas que usa Backend II.
Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. 
Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.
Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.
'''
from datetime import timedelta
import random
import uuid
import pandas as pd
from faker import Faker


#1. Configurar el faker a la region que necesitas
fake = Faker("es_CO")

 #2. Sembrar semillas para tener coherencia en los datos simulados y tener los mismos datos

Faker.seed(42)
random.seed(42)

#3. Identifico los datos que debo simular
#id (texto (UUID)), 
#nombre (texto), 
#descripcion (texto), 
#fecha_inicio (fecha),
#fecha_fin (fecha), 
#estado (texto),
#id_empresa (texto (UUID)), 
#id_categoria (texto (UUID)),
#id_prioridad (texto (UUID)).

ESTADOS=("PENDIENTE", "COMPLETADO", "EN_PROGRESO")
IDS_EMPRESA = [
    str(uuid.uuid5(uuid.NAMESPACE_URL, f"beta_nt_2026_4/empresa/{i}"))
    for i in range(1, 6)
]
IDS_CATEGORIA = [
    str(uuid.uuid5(uuid.NAMESPACE_URL, f"beta_nt_2026_4/categoria/{i}"))
    for i in range(1, 9)
]
IDS_PRIORIDAD = [
    str(uuid.uuid5(uuid.NAMESPACE_URL, f"beta_nt_2026_4/prioridad/{i}"))
    for i in range(1, 4)
]

FILAS=500

def generar_datos_limpios(numero_datos=FILAS):
    filas=[]
    for indice in range(numero_datos):
        fecha_inicio = fake.date_between(start_date="-1y", end_date="+3m")
        filas.append({
                    "id":str(uuid.uuid5(
                        uuid.NAMESPACE_URL,
                        f"beta_nt_2026_4/reto/{indice}",
                    )),
                    "nombre": fake.name(),
                    "descripcion": fake.sentence(nb_words=12),
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_inicio + timedelta(days=random.randint(15, 180)),
                    "estado": random.choice(ESTADOS),
                    "id_empresa": random.choice(IDS_EMPRESA),
                    "id_categoria": random.choice(IDS_CATEGORIA),
                    "id_prioridad": random.choice(IDS_PRIORIDAD)
                })
    return filas

#1. crear una funcion para definir porcentaje de error
def generar_muestra(datos, porcentaje):
    return datos.sample(
        frac=porcentaje,
        random_state=random.randint(0, 999)
    ).index

#2 crear una funcion para escribir mal un texto
def escribir_mal(texto):
    variantes=[texto.lower(), f" {texto.title()}", texto.capitalize()]
    return random.choice(variantes)
#4. Funcion para restar dias

def restar_dias(f):
    fecha_anterior = f - timedelta(days=random.randint(1, 30))
    return fecha_anterior.strftime("%Y-%m-%d")

def ensuciar(datos_df):
    datos_df=datos_df.copy()
    fecha_inicio_original = pd.to_datetime(datos_df["fecha_inicio"])

    #Se ensucia `nombre`: 10% con espacios sobrantes.
    filas_elegidas= generar_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "nombre"]=" " + datos_df.loc[filas_elegidas,"nombre"] + " "

    #Se ensucia `descripcion`: 12% en None (nulos).
    filas_elegidas= generar_muestra(datos_df, 0.12)
    datos_df.loc[filas_elegidas, "descripcion"]= None

    #Se ensucia `fecha_inicio`: dos formatos mezclados: "2026-03-02" y "02/03/2026".
    iso=fecha_inicio_original.dt.strftime("%Y-%m-%d")
    latino=fecha_inicio_original.dt.strftime("%d/%m/%Y")
    datos_df["fecha_inicio"]=iso
        
    filas_elegidas=generar_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "fecha_inicio"]=latino.loc[filas_elegidas]

    # 8 % de fecha_fin en None
    filas_nulas = generar_muestra(datos_df, 0.08)
    datos_df.loc[filas_nulas, "fecha_fin"] = None
    
    # 5 % con fecha_fin anterior a fecha_inicio, sin reutilizar filas nulas
    filas_disponibles = datos_df.index.difference(filas_nulas)
    filas_anteriores = datos_df.loc[filas_disponibles].sample(
        n=round(len(datos_df) * 0.05),
        random_state=random.randint(0, 999)
    ).index                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    
    datos_df.loc[filas_anteriores, "fecha_fin"] = fecha_inicio_original.loc[
        filas_anteriores
    ].map(restar_dias)

    #Se ensucia `estado`: variantes: 'en_curso', 'EN CURSO', ' Cerrado '.
    filas_elegidas=generar_muestra(datos_df, 0.09 )
    datos_df.loc[filas_elegidas, "estado"]= datos_df.loc[filas_elegidas, "estado"].map(escribir_mal)

    # 5% de las filas repetidas tal cual (duplicados exactos).
    filas_duplicadas = generar_muestra(datos_df, 0.05)
    datos_df = pd.concat([datos_df, datos_df.loc[filas_duplicadas]], ignore_index=True)
    return datos_df

#Todo se arma en una funcion `generar_retos(n=500)` que **devuelve el DataFrame** (`return df`), para poder importarla desde el script de exportacion.
def generar_retos(n=FILAS):
    
    df = pd.DataFrame(generar_datos_limpios(n))
    df= ensuciar(df)
    return df

#El bloque `if __name__ == "__main__":` solo imprime `df.shape`, `df.head()` y `df.isna().sum()` para revisar que los datos quedaron sucios.
if __name__ == "__main__":
    df = generar_retos()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())
