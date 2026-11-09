"""
limpiar_retos.py
Limpia la tabla de retos del proyecto integrador (criterios de la HU L01 de Kaizen).

Uso:
    python scripts/limpiar_retos.py retos_sucio.csv

Genera retos_limpio.csv en la misma carpeta que el archivo de entrada.
"""

import os
import sys

import pandas as pd

# Columnas que no pueden quedar vacías después de limpiar.
COLUMNAS_OBLIGATORIAS = ["id", "nombre", "estado", "fecha_inicio", "fecha_fin"]


def imprimir_diagnostico(df, titulo):
    """Imprime el shape, la info, los nulos por columna y los duplicados exactos del DataFrame."""
    print(f"\n===== {titulo} =====")
    print("Shape:", df.shape)
    print("\nInfo:")
    df.info()
    print("\nNulos por columna:")
    print(df.isna().sum())
    print("\nDuplicados exactos:", df.duplicated().sum())


def leer_csv(ruta):
    """Lee el CSV con pandas y lo devuelve. Termina el programa si el archivo no existe."""
    if not os.path.exists(ruta):
        print(f"Error: no se encontró el archivo '{ruta}'.")
        sys.exit(1)
    # El archivo viene con separador ";" y BOM de UTF-8 (utf-8-sig), por eso se indica aquí.
    return pd.read_csv(ruta, sep=";", encoding="utf-8-sig")


def quitar_duplicados(df):
    """Elimina las filas que son copias exactas de otra fila."""
    return df.drop_duplicates()


def parsear_fecha(serie):
    """Convierte una columna de texto a fechas aceptando aaaa-mm-dd y dd/mm/aaaa. Lo que no se pueda leer queda como nulo."""
    # Cada formato se prueba por separado: con format="mixed" y dayfirst=True,
    # pandas lee las fechas ISO (aaaa-mm-dd) como día-mes, lo que da fechas falsas.
    iso = pd.to_datetime(serie, format="%Y-%m-%d", errors="coerce")
    dmy = pd.to_datetime(serie, format="%d/%m/%Y", errors="coerce")
    return iso.fillna(dmy)


def convertir_fechas(df):
    """Convierte fecha_inicio y fecha_fin a fechas usando parsear_fecha."""
    df["fecha_inicio"] = parsear_fecha(df["fecha_inicio"])
    df["fecha_fin"] = parsear_fecha(df["fecha_fin"])
    return df


def unificar_estado(df):
    """Quita espacios sobrantes, pasa a mayúsculas y reemplaza espacios por guion bajo en la columna estado."""
    df["estado"] = df["estado"].str.strip().str.upper().str.replace(" ", "_")
    return df


def rellenar_descripciones(df):
    """Reemplaza las descripciones vacías por un texto por defecto."""
    df["descripcion"] = df["descripcion"].fillna("Sin descripcion")
    return df


def calcular_duracion_y_validez(df):
    """Crea duracion_dias (días entre inicio y fin) y fecha_valida (False si el fin es anterior al inicio)."""
    df["duracion_dias"] = (df["fecha_fin"] - df["fecha_inicio"]).dt.days
    df["fecha_valida"] = df["duracion_dias"] >= 0
    return df


def reportar_fechas_incoherentes(df):
    """Cuenta e imprime cuántos retos tienen la fecha de fin anterior a la de inicio."""
    incoherentes = (df["duracion_dias"] < 0).sum()
    print(f"\nFechas incoherentes (fin antes que inicio): {incoherentes}")


def eliminar_nulos_obligatorios(df):
    """Elimina las filas que tienen nulos en alguna columna obligatoria."""
    return df.dropna(subset=COLUMNAS_OBLIGATORIAS)


def main():
    """Función principal: lee el CSV, diagnostica, limpia, vuelve a diagnosticar y guarda el resultado."""
    if len(sys.argv) < 2:
        print("Uso: python scripts/limpiar_retos.py retos_sucio.csv")
        sys.exit(1)

    ruta_entrada = sys.argv[1]
    carpeta = os.path.dirname(os.path.abspath(ruta_entrada))
    ruta_salida = os.path.join(carpeta, "retos_limpio.csv")

    df = leer_csv(ruta_entrada)
    imprimir_diagnostico(df, "DIAGNÓSTICO ANTES DE LIMPIAR")
    filas_antes = len(df)

    df = quitar_duplicados(df)
    df = convertir_fechas(df)
    df = unificar_estado(df)
    df = rellenar_descripciones(df)
    df = calcular_duracion_y_validez(df)
    reportar_fechas_incoherentes(df)
    df = eliminar_nulos_obligatorios(df)
    # Se repite la eliminación de duplicados: tras normalizar, dos filas pueden quedar iguales.
    df = quitar_duplicados(df)

    imprimir_diagnostico(df, "DIAGNÓSTICO DESPUÉS DE LIMPIAR")

    filas_eliminadas = filas_antes - len(df)
    print(f"\nFilas antes: {filas_antes} | después: {len(df)} | eliminadas: {filas_eliminadas}")

    df.to_csv(ruta_salida, index=False, encoding="utf-8")
    print(f"Archivo guardado en: {ruta_salida}")


if __name__ == "__main__":
    main()