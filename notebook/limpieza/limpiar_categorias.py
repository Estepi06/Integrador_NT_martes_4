"""Limpia la tabla categorias del proyecto integrador (HU L01).

Uso (desde la raiz del proyecto):
    python notebook/limpieza/limpiar_categorias.py data/crudo/categorias_sucio.csv

Lee el CSV sucio, imprime el diagnostico, corrige los errores, imprime el
diagnostico otra vez y guarda data/limpio/categorias_limpio.csv.
"""
import sys
import unicodedata
from pathlib import Path

import pandas as pd

# limpiar_categorias.py -> limpieza -> notebook -> raiz
RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_ENTRADA = RAIZ_PROYECTO / "data" / "crudo" / "categorias_sucio.csv"
RUTA_SALIDA = RAIZ_PROYECTO / "data" / "limpio" / "categorias_limpio.csv"

# Columnas que debe tener la tabla (segun los criterios)
COLUMNAS = ["id", "nombre", "descripcion", "area_responsable"]

# Texto con el que se rellenan los nulos (no se borran filas por tener nulos)
DESCRIPCION_POR_DEFECTO = "Sin descripcion"
AREA_POR_DEFECTO = "Sin asignar"


def cargar_datos(ruta):
    """Lee el CSV sucio y valida que existan las columnas esperadas."""
    df = pd.read_csv(ruta, dtype=str)
    faltantes = [c for c in COLUMNAS if c not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas en el archivo: {faltantes}")
    return df[COLUMNAS]


def imprimir_diagnostico(df, titulo):
    """Imprime shape, info, nulos y duplicados de un DataFrame."""
    print(f"\n===== {titulo} =====")
    print("shape:", df.shape)
    print("\ninfo:")
    df.info()
    print("\nnulos por columna:")
    print(df.isna().sum())
    print("\nduplicados exactos:", df.duplicated().sum())
    print("nombres distintos en 'nombre':", df["nombre"].nunique())


def quitar_tildes(texto):
    """Quita las tildes de un texto (logística -> logistica)."""
    base = unicodedata.normalize("NFD", texto)
    return "".join(c for c in base if unicodedata.category(c) != "Mn")


def normalizar_nombre(valor):
    """Unifica las variantes de un nombre: sin espacios, sin tildes, formato título."""
    if pd.isna(valor):
        return valor
    limpio = quitar_tildes(str(valor)).strip()
    limpio = " ".join(limpio.split())  # colapsa espacios internos repetidos
    return limpio.title() if limpio else pd.NA


def limpiar_texto(valor):
    """Quita espacios sobrantes; un texto vacio pasa a nulo."""
    if pd.isna(valor):
        return valor
    limpio = " ".join(str(valor).split())
    return limpio if limpio else pd.NA


def limpiar_categorias(df):
    """Aplica todas las correcciones y devuelve un DataFrame nuevo."""
    df = df.copy()

    # 1. Espacios sobrantes y textos vacios en todas las columnas
    for col in COLUMNAS:
        df[col] = df[col].map(limpiar_texto)

    # 2. Variantes del mismo nombre ('LOGISTICA', ' logistica ', 'logística')
    df["nombre"] = df["nombre"].map(normalizar_nombre)

    # 3. Duplicados exactos (filas repetidas tal cual)
    df = df.drop_duplicates().reset_index(drop=True)

    # 4. Nulos: se rellenan para no perder filas
    df["descripcion"] = df["descripcion"].fillna(DESCRIPCION_POR_DEFECTO)
    df["area_responsable"] = df["area_responsable"].fillna(AREA_POR_DEFECTO)
    return df


def main():
    """Punto de entrada: diagnostico antes, limpieza, diagnostico despues y guardado."""
    if len(sys.argv) > 2:
        print("Uso: python notebook/limpieza/limpiar_categorias.py data/crudo/categorias_sucio.csv")
        sys.exit(1)

    ruta = Path(sys.argv[1]) if len(sys.argv) == 2 else RUTA_ENTRADA
    if not ruta.exists():
        print(f"No se encontro el archivo: {ruta}")
        sys.exit(1)

    df_sucio = cargar_datos(ruta)
    imprimir_diagnostico(df_sucio, "DIAGNOSTICO ANTES")

    df_limpio = limpiar_categorias(df_sucio)
    imprimir_diagnostico(df_limpio, "DIAGNOSTICO DESPUES")

    RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    df_limpio.to_csv(RUTA_SALIDA, index=False)

    eliminadas = len(df_sucio) - len(df_limpio)
    print(f"\nFilas eliminadas: {eliminadas}")
    print(f"Archivo limpio guardado en: {RUTA_SALIDA}")


if __name__ == "__main__":
    main()