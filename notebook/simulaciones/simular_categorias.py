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
#id(texto uuid)
# nombre(texto)
#correo (texto)
#contresena_hash (texto)
#rol (texto)
#activo (booleano)
#fecha_registro (fecha y hora)

#4Identifico los datos o el dato que sea selector y escrbiho los elementos.

ROLES = ["ADMIN", "EMPRESA", "PARTICIPANTE","INVITADO"]

#5Defino mi dataset
FILAS = 250

#6 Contruir una funcion para generar datos pedidos (limpios)
def generar_datos_limpios(numeros_datos=FILAS):
    filas = []
    for _ in range(numeros_datos):
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": fake.name(),
            "correo": fake.email(),
            "contresena_hash": fake.sha256(),
            "rol": random.choice(ROLES),
            "activo": random.choice([True, False]),
            "fecha_registro": fake.date_time_between(start_date='-2y', end_date='now').isoformat()
        })
    return filas

variable= pd.DataFrame(generar_datos_limpios())

 #Ensuciar Datos 

 #1 Crear una funcion para definiar porcentajes de error y ensuciar los datos

def generar_muestras (datos, porcentaje):
    return datos.sample(fraccion=porcentaje, random_state=random.randint(0,999)).index 

#2 Crear una funcion para escribir mal un texto

def escribir_mal(texto):
    variantes=[texto.lower(), f" {texto.title()} ", texto.capitalize() ]
    return random.choice(variantes)

#3 Crear una funcion para convertir booleanos a texto 

def convertir_booleano_texto (valor):
    if valor:
        return random.choice(["SI", "1"])
    return random.choice(["NO", "0"])

#4 Funcion para ensuciar los datos

def ensuciar_datos(datos_df):
    datos_df = datos_df.copy()

    #nombre: 10% con espacios sobrantes , 8% con mayusculas 
    filas_elegidas = generar_muestras(datos_df, 0.10) 

     #descripcion: 15% con espacios sobrantes , 10% con mayusculas 
    filas_elegidas = generar_muestras(datos_df, 0.15) 
    datos_df.loc[filas_elegidas,"descripcion"]="" + datos_df.loc[filas_elegidas, "descripcion"] + " "
    
    filas_elegidas = generar_muestras (datos_df, 0.10) 
    datos_df.loc[filas_elegidas,"descripcion"]=datos_df.loc [filas_elegidas, "descripcion"].str.upper()
    
        #correo: 12% mayusculas y el 5 % sin el @ y el 4% en none
    
    filas_elegidas= generar_muestras(datos_df, 0.12)
    datos_df.loc[filas_elegidas, "correo"]=datos_df.loc
    [filas_elegidas, "correo"].str.upper()
    
    filas_elegidas = generar_muestras(datos_df, 0.05)
    datos_df.loc[filas_elegidas, "correo"]=datos_df.loc
    [filas_elegidas, "correo"].str.replace("@","", regex=False)
    datos_df.loc[filas_elegidas, "correo"]=None
    
        # rol variante de escritura (admin, ADMIN, Admin)

    filas_elegidas = generar_muestras (datos_df, 0.07)
    datos_df.loc[filas_elegidas,"rol"]=datos_df.loc [filas_elegidas,"rol"].map(escribir_mal)

   # fecha dos formato mexzclados (2026-03-15 14:30:00) ISO y (15/03/2026 14:30) LATIN
    iso=datos_df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")
    latino=datos_df["fechas_registro"].dt.strftime("%d/%m/%Y %H:%M")
    datos_df["fecha_registro"]=iso
    filas_elegidas=generar_muestras(datos_df, 0.4)

    datos_df.loc[filas_elegidas], "fecha_registro"=latino.loc["filas_elegidas"]

    #Activo en ocasiones llega SI NO 1 o 0
    filas_elegidas=generar_muestras(datos_df, 0.3)
    datos_df.loc[filas_elegidas, "activo"]=datos_df.loc
    [filas_elegidas, "activo"].map (convertir_booleano_texto)
    




        
    