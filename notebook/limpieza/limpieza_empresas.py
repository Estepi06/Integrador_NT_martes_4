"""Limpieza de la tabla empresas del proyecto integrador (HU L01, Kaizen).

Uso:
    python src/limpiar_empresas.py data/crudo/empresas_sucio.csv
"""

import sys
from pathlib import Path
import pandas as pd

# Ruta de salida según los criterios de la HU L01
RUTA_SALIDA = Path("data/limpio/empresas_limpio.csv")

# Columnas que no pueden quedar con nulos después de limpiar
OBLIGATORIAS = ["nombre", "sector", "nit", "telefono", "activa"]

def leer_csv(ruta):
    """Lee el CSV con pandas. Todo entra como texto para que .str funcione
    en nit y telefono aunque vengan solo con dígitos."""
    return pd.read_csv(ruta, dtype=str)

def imprimir_diagnostico(df, titulo):
    """Imprime shape, info, nulos por columna y cantidad de duplicados."""
    print(f"\n===== {titulo} =====")
    print("shape:", df.shape)
    print("\ninfo:")
    df.info()
    print("\nnulos por columna:")
    print(df.isna().sum())
    print("\nduplicados exactos:", df.duplicated().sum())

def quitar_duplicados(df):
    """Elimina las filas que son duplicados exactos."""
    return df.drop_duplicates()

def limpiar_nombre(df):
    """Quita los espacios sobrantes al inicio y al final del nombre."""
    df["nombre"] = df["nombre"].str.strip()
    return df

def unificar_sector(df):
    """Unifica el sector: sin espacios sobrantes y con formato Título."""
    df["sector"] = df["sector"].str.strip().str.title()
    return df

def limpiar_nit(df):
    """Deja el NIT en un solo formato, sin puntos ni guiones."""
    df["nit"] = df["nit"].str.replace(r"[.\-]", "", regex=True)
    return df

def limpiar_telefono(df):
    """Deja el teléfono solo con dígitos."""
    df["telefono"] = df["telefono"].str.replace(r"\D", "", regex=True)
    return df

def convertir_activa(df):
    """Convierte activa (llega como texto) a booleano real. Lo que no se
    reconoce queda como nulo y luego se elimina por ser columna obligatoria."""
    df["activa"] = (
        df["activa"].astype(str).str.strip().str.upper()
        .map({"TRUE": True, "SI": True, "1": True,
              "FALSE": False, "NO": False, "0": False})
    )
    return df

def rellenar_contacto(df):
    """Rellena los contactos vacíos con 'Sin contacto'."""
    df["contacto"] = df["contacto"].fillna("Sin contacto")
    return df

def marcar_correos(df):
    """Crea la columna correo_valido: True si el correo contiene '@'."""
    df["correo_valido"] = df["correo"].str.contains("@", na=False)
    return df

def quitar_nulos_obligatorios(df):
    """Elimina las filas con nulos o texto vacío en las columnas obligatorias."""
    cols = [c for c in OBLIGATORIAS if c in df.columns]
    df[cols] = df[cols].replace(r"^\s*$", pd.NA, regex=True)
    return df.dropna(subset=cols)

def limpiar(df):
    """Aplica todas las correcciones en orden. Los duplicados se quitan dos
    veces: antes (exactos del crudo) y después de normalizar, porque al
    limpiar espacios y formatos aparecen duplicados nuevos."""
    df = quitar_duplicados(df)
    df = limpiar_nombre(df)
    df = unificar_sector(df)
    df = limpiar_nit(df)
    df = limpiar_telefono(df)
    df = convertir_activa(df)
    df = rellenar_contacto(df)
    df = marcar_correos(df)
    df = quitar_nulos_obligatorios(df)
    df["activa"] = df["activa"].astype(bool)  # ya sin nulos: dtype bool real
    df = quitar_duplicados(df)
    return df

def guardar(df, ruta):
    """Guarda el DataFrame limpio en CSV UTF-8 sin índice, creando la carpeta."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta, index=False, encoding="utf-8")

def main():
    """Punto de entrada: lee, diagnostica, limpia, diagnostica y guarda."""
    if len(sys.argv) != 2:
        sys.exit("Uso: python src/limpiar_empresas.py data/crudo/empresas_sucio.csv")
    df = leer_csv(sys.argv[1])
    filas_antes = len(df)
    imprimir_diagnostico(df, "DIAGNÓSTICO ANTES")
    df = limpiar(df)
    imprimir_diagnostico(df, "DIAGNÓSTICO DESPUÉS")
    print(f"\nFilas eliminadas: {filas_antes - len(df)} "
          f"({filas_antes} -> {len(df)})")
    guardar(df, RUTA_SALIDA)
    print(f"Archivo guardado en: {RUTA_SALIDA}")

if __name__ == "__main__":
    main()