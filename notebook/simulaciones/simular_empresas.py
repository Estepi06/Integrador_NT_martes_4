'''
Organizacion que registra o propone retos. Crea el script `src/simular_empresas.py`. Con la libreria **Faker** 
genera 300 filas falsas de la tabla `empresas`, con las MISMAS columnas que usa Backend 
II. Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, 
mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, 
asi que tienen que quedar bien puestos.

Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` 
para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.

'''

import random
import uuid

import pandas as pd
from faker import Faker

#1 configurar el faker a la region que necesito 

fake=Faker("es_CO")

#2 Sembrar semillas para tener coherencia en los datos 
#simulados

Faker.seed(42)
random.seed(42)

#3 Identifico datos a simular 

#Se generan 300 filas con estas columnas: 

#id (texto (UUID)), 
#nombre (texto), 
#nit (texto), 
#sector (texto), 
#contacto (texto), 
#correo (texto), 
#telefono (texto), 
#activa (booleano).

#4 identifico los datos o dato que sea selector y escribo opciones

SECTORES=["ADMINISTRACION","CONTABLE","FINANZAS","SALUD","TECNOLOGIA","EDUCACION","CONSTRUCCION","TRANSPORTE"]

#5 Definir el dataset

FILAS=300

#6Construir una funcion para generar los N datos pedidos (LIMPIOS)

def generar_datos_limpios (numero_datos=FILAS):
    filas=[]
    for _ in range (numero_datos):
      filas.append({
        "id": str(uuid.uuid4()), 
        "nombre":fake.name(),
        "nit":fake.numerify("#########-#"),
        "sector":random.choice(SECTORES),
        "contacto":fake.name(),
        "correo":fake.company_email(),
        "telefono":fake.numerify("3#########"),
        "activa":random.choice([True,False])
      })
    return filas

#Ensuciar los datos

#1 crear una funcion para definir porcentaje de error 

def gernerar_muestra (datos, porcentaje_error):
    return datos.sample(frac=porcentaje_error, 
    random_state=random.randint(0,999)).index

#2 crear la funcion para escribir mal un texto 

def escribir_mal (texto):
    variantes=[texto.lower(),f"{texto.title()}", texto.capitalize()]
    return random.choice(variantes)

#3 crear una funcion para convertir booleanos en texto

def convertir_booleano(valor):
    if (valor):
        return random.choice(["SI","1"])
    return random.choice (["NO", "0"])

#4 funcion para ensuciar el telefono
def ensuciar_telefono(tel):
    opcion = random.choice([1, 2, 3])
    if opcion == 1:
        return tel
    elif opcion == 2:
        return f"{tel[:3]} {tel[3:6]} {tel[6:]}"
    else:
        return f"+57 {tel[:3]}-{tel[3:6]}-{tel[6:]}"


#5 Funcion para ensuciar datos 

def ensiciar(datos_df):
    datos_df=datos_df.copy()

    #Se ensucia `nombre`: 10% con espacios sobrantes al inicio y al final; 15% en MAYUSCULAS.
    
    filas_elegidas = gernerar_muestra(datos_df,0.1)
    datos_df.loc[filas_elegidas,"nombre"]=" "+datos_df.loc[filas_elegidas, "nombre"]+" "

    filas_elegidas = gernerar_muestra(datos_df,0.15)
    datos_df.loc[filas_elegidas,"nombre"]=datos_df.loc[filas_elegidas,"nombre"].str.upper()

    #Se ensucia `nit`: la mitad con puntos y guiones (900.123.456-7) y la otra mitad sin nada (9001234567)

    filas_elegidas = gernerar_muestra(datos_df,0.5)
    datos_df.loc[filas_elegidas,"nit"]=datos_df.loc[filas_elegidas, "nit"].str.replace( r'^(\d{3})(\d{3})(\d{3})-(\d{1})$', r'\1.\2.\3-\4', regex=True)

    filas_elegidas = gernerar_muestra(datos_df,0.5)
    datos_df.loc[filas_elegidas,"nit"]=datos_df.loc[filas_elegidas,"nit"].str.replace("-", "", regex=False)

    #Se ensucia `sector`: variantes del mismo sector: 'Logistica', 'LOGISTICA', ' logistica '

    filas_elegidas = gernerar_muestra(datos_df,0.15)
    datos_df.loc[filas_elegidas,"sector"]=datos_df.loc[filas_elegidas,"sector"].map(escribir_mal)

    #Se ensucia `contacto`: 8% en None (nulos).

    filas_elegidas = gernerar_muestra(datos_df,0.08)
    datos_df.loc[filas_elegidas,"contacto"]= None

   #Se ensucia `correo`: 6% sin la arroba (correo invalido).

    filas_elegidas = gernerar_muestra(datos_df,0.06)
    datos_df.loc[filas_elegidas,"correo"]=datos_df.loc[filas_elegidas,"correo"].str.replace("@","",regex=False)

    #Se ensucia `telefono`: tres formatos mezclados: '3001234567', '300 123 4567', '+57 300-123-4567'.

    filas_elegidas = gernerar_muestra(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "telefono"] = datos_df.loc[filas_elegidas, "telefono"].map(ensuciar_telefono)
    
    #Se ensucia `activa`: a veces como texto: 'SI', 'No', '1', '0'.

    datos_df["activa"] = datos_df["activa"].astype(object) 
    filas_elegidas = gernerar_muestra(datos_df,0.3)
    datos_df.loc[filas_elegidas,"activa"]= datos_df.loc[filas_elegidas, "activa"].map(convertir_booleano)

    #5% de las filas repetidas tal cual (duplicados exactos).

    filas_elegidas = gernerar_muestra(datos_df,0.05)
    filas_duplicadas = datos_df.loc[filas_elegidas]
    datos_df = pd.concat([datos_df, filas_duplicadas], ignore_index=True)

    # 3% de los nit repetidos entre empresas distintas

    filas_a = gernerar_muestra(datos_df, 0.03)
    filas_b = gernerar_muestra(datos_df, 0.03)

    datos_df.loc[filas_a, "nit"] = datos_df.loc[filas_b, "nit"].values

    return datos_df

# 6. Función principal para exportar

def generar_empresas(n=FILAS):
    df = pd.DataFrame(generar_datos_limpios(n))
    df = ensiciar(df)
    return df

# 7. Bloque de prueba en consola

if __name__ == "__main__":
    df = generar_empresas()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())



