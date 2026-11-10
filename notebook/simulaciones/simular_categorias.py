' Crea el script `src/simular_categorias.py`. Con la libreria **Faker** genera 250 filas falsas de la tabla `categorias`, con las MISMAS columnas que usa Backend II. '
'Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes,mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.'
'Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.'

import random
import uuid
import pandas as pd          
from faker import Faker

#1Configar el Faker a la region que necesitas
fake = Faker('es_CO')

#2Sembrar semillas para tener la coherencia en los datos simulados y tener los mismo datos 

Faker.seed(42)
random.seed(42)

#3Identifico los datos que debo simular
#id(texto (UUID)) 
# nombre(texto)
# descripcion(texto)
# area_responsable (texto).
#Categorias: id, nombre, descripcion, area_responsable

#4Identifico los datos o el dato que sea selector y escrbiho los elementos.

CATEGORIAS = ["Logistica", "Tecnologia", "Educacion", "Economia", "Ecologia",
              "Nutricion", "Psicologia", "Musica", "Fotografia", "Geografia"]

AREAS= ["OPERACIONES", "INNOVACION", "BIENESTAR", "FORMACION", "COMUNICACIONES"]

ACENTOS = {
    "Logistica": "Logística", "Tecnologia": "Tecnología", "Educacion": "Educación",
    "Economia": "Economía", "Ecologia": "Ecología", "Nutricion": "Nutrición",
    "Psicologia": "Psicología", "Musica": "Música", "Fotografia": "Fotografía",
    "Geografia": "Geografía",
}

#5Defino mi dataset
FILAS = 250

#6 Contruir una funcion para generar datos pedidos (limpios)
def generar_datos_limpios(numeros_datos=FILAS):
    categorias = []
    for _ in range(numeros_datos):
        categorias.append({
            # UUID v4 que respeta random.seed(42) (uuid.uuid4() no lo respeta)
            "id": str(uuid.UUID(int=random.getrandbits(128), version=4)),
            "nombre": random.choice(CATEGORIAS),
            "descripcion": fake.sentence(nb_words=8),
            "area_responsable": random.choice(AREAS)
        })
    return categorias

 #1 Crear una funcion para definiar porcentajes de error y ensuciar los datos

def generar_muestras (datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0,999)).index 


#2 Crear una funcion para escribir mal un texto

def escribir_mal(nombre):
    variantes = [
        nombre,                       
        nombre.upper(),               
        f" {nombre.lower()} ",        
        ACENTOS[nombre].lower(),      
    ]
    return random.choice(variantes)

#3 Funcion para ensuciar los datos
def ensuciar_datos(datos_df):
    datos_df = datos_df.copy()

        # nombre: variantes del mismo nombre
    datos_df["nombre"] = datos_df["nombre"].map(escribir_mal)

    # descripcion: 15% en None (nulos)
    filas_elegidas = generar_muestras(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "descripcion"] = None 

        # area_responsable: 10% en None
    filas_elegidas = generar_muestras(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "area_responsable"] = None

    return datos_df   
    
#  funcion principal que arma todo y devuelve el DataFrame
def generar_categorias(n=250):
    n_repetidas = round(n * 0.08)        # 8% de filas repetidas (20 filas)
    n_propias = n - n_repetidas          # 230 + 20 repetidas = 250

    df = pd.DataFrame(generar_datos_limpios(n_propias))
    df = ensuciar_datos(df)

    # 8% de filas repetidas tal cual (duplicados exactos)
    repetidas = df.sample(n=n_repetidas, random_state=random.randint(0, 999))
    df = pd.concat([df, repetidas], ignore_index=True)

    return df


#   bloque principal, solo revisa que los datos quedaron sucios
if __name__ == "__main__":
    df = generar_categorias()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())