"""
limpieza_retos.py
Limpia la tabla de retos del proyecto integrador (criterios de la HU L01 de Kaizen).

Uso:
    python notebook/limpieza/limpieza_retos.py data/crudo/retos_sucio.csv

Genera retos_limpio.csv en la carpeta data/limpio/.
"""

import os
import sys
from pathlib import Path
import pandas as pd

# Rutas fijas calculadas desde la raíz del proyecto
RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
ENTRADA_DEFECTO = RAIZ_PROYECTO / "data" / "crudo" / "retos_sucio.csv"
CARPETA_LIMPIO = RAIZ_PROYECTO / "data" / "limpio"
SALIDA_DEFECTO = CARPETA_LIMPIO / "retos_limpio.csv"

# Columnas obligatorias
COLUMNAS_OBLIGATORIAS = ["id", "nombre", "estado", "fecha_inicio", "fecha_fin"]


def imprimir_diagnostico(df, titulo):
    """Imprime el shape, info y nulos del DataFrame."""
    print(f"\n===== {titulo} =====")
    print("Shape:", df.shape)
    print("Nulos por columna:")
    print(df.isna().sum())
    print("Duplicados exactos:", df.duplicated().sum())


def leer_csv(ruta):
    """Lee el CSV autodeteccionando el separador (coma o punto y coma)."""
    ruta_path = Path(ruta)
    if not ruta_path.exists():
        print(f"⚠️ Error: no se encontró el archivo '{ruta}'.")
        return None
    try:
        df = pd.read_csv(ruta_path, sep=None, engine="python", encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(ruta_path, encoding="utf-8-sig")

    df.columns = df.columns.str.strip()
    return df


def quitar_duplicados(df):
    """Elimina las filas que son copias exactas."""
    return df.drop_duplicates()


def parsear_fecha(serie):
    """Convierte texto a fecha aceptando ISO y formato día/mes/año."""
    iso = pd.to_datetime(serie, format="%Y-%m-%d", errors="coerce")
    dmy = pd.to_datetime(serie, format="%d/%m/%Y", errors="coerce")
    return iso.fillna(dmy)


def convertir_fechas(df):
    """Convierte fecha_inicio y fecha_fin a tipo datetime."""
    if "fecha_inicio" in df.columns:
        df["fecha_inicio"] = parsear_fecha(df["fecha_inicio"])
    if "fecha_fin" in df.columns:
        df["fecha_fin"] = parsear_fecha(df["fecha_fin"])
    return df


def unificar_estado(df):
    """Normaliza texto de la columna estado."""
    if "estado" in df.columns:
        df["estado"] = df["estado"].astype(str).str.strip().str.upper().str.replace(" ", "_")
    return df


def rellenar_descripciones(df):
    """Rellena descripciones nulas."""
    if "descripcion" in df.columns:
        df["descripcion"] = df["descripcion"].fillna("Sin descripcion")
    return df


def calcular_duracion_y_validez(df):
    """Calcula duracion_dias y validez de fechas."""
    if "fecha_inicio" in df.columns and "fecha_fin" in df.columns:
        df["duracion_dias"] = (df["fecha_fin"] - df["fecha_inicio"]).dt.days
        df["fecha_valida"] = df["duracion_dias"] >= 0
    return df


def reportar_fechas_incoherentes(df):
    """Reporta incoherencias de fechas."""
    if "duracion_dias" in df.columns:
        incoherentes = (df["duracion_dias"] < 0).sum()
        print(f"\nFechas incoherentes (fin antes que inicio): {incoherentes}")


def eliminar_nulos_obligatorios(df):
    """Elimina filas sin campos esenciales presentes."""
    cols_presentes = [c for c in COLUMNAS_OBLIGATORIAS if c in df.columns]
    return df.dropna(subset=cols_presentes)


def main(ruta_entrada_param=None):
    """Procesa el CSV y guarda la salida en data/limpio/retos_limpio.csv."""
    if ruta_entrada_param:
        ruta_entrada = Path(ruta_entrada_param)
    elif len(sys.argv) > 1:
        ruta_entrada = Path(sys.argv[1])
    else:
        ruta_entrada = ENTRADA_DEFECTO

    df = leer_csv(ruta_entrada)
    if df is None or df.empty:
        print(f"⚠️ No se pudo procesar {ruta_entrada}")
        return

    imprimir_diagnostico(df, "DIAGNÓSTICO ANTES DE LIMPIAR")
    filas_antes = len(df)

    df = quitar_duplicados(df)
    df = convertir_fechas(df)
    df = unificar_estado(df)
    df = rellenar_descripciones(df)
    df = calcular_duracion_y_validez(df)
    reportar_fechas_incoherentes(df)
    df = eliminar_nulos_obligatorios(df)
    df = quitar_duplicados(df)

    imprimir_diagnostico(df, "DIAGNÓSTICO DESPUÉS DE LIMPIAR")

    filas_eliminadas = filas_antes - len(df)
    print(f"\nFilas antes: {filas_antes} | después: {len(df)} | eliminadas: {filas_eliminadas}")

    # Guardado en data/limpio/
    CARPETA_LIMPIO.mkdir(parents=True, exist_ok=True)
    df.to_csv(SALIDA_DEFECTO, index=False, encoding="utf-8")
    print(f"✓ Archivo guardado en: {SALIDA_DEFECTO}")


if __name__ == "__main__":
    main()