"""
limpieza_registros.py
Limpia data/crudo/registros_sucio.csv y guarda data/limpio/registros_limpio.csv.
Ejecutar desde la raíz del proyecto: python notebook/limpieza/limpieza_registros.py
"""
import os

import pandas as pd

RUTA_ENTRADA = os.path.join("data", "crudo", "registros_sucio.csv")
RUTA_SALIDA = os.path.join("data", "limpio", "registros_limpio.csv")
COLUMNAS_OBLIGATORIAS = ["id", "fecha_registro", "estado", "id_usuario", "id_reto"]


def diagnostico(df, titulo):
    """Imprime forma, tipos, nulos y duplicados exactos del DataFrame."""
    print(f"\n--- {titulo} ---")
    print("shape:", df.shape)
    df.info()
    print("Nulos por columna:")
    print(df.isna().sum())
    print("Duplicados exactos:", df.duplicated().sum())


def main():
    df = pd.read_csv(RUTA_ENTRADA, encoding="utf-8")
    filas_inicio = len(df)
    diagnostico(df, "Diagnóstico inicial")

    # 1. Quitar duplicados exactos
    df = df.drop_duplicates()

    # 2. estado: quitar espacios y pasar a mayúsculas ('inscrito' y ' Finalizado ' quedan iguales)
    df["estado"] = df["estado"].str.strip().str.upper()

    # 3. observacion: los nulos pasan a un texto fijo
    df["observacion"] = df["observacion"].fillna("Sin observación")

    # 4. fecha_registro: dos formatos a un solo tipo de fecha
    fecha = pd.to_datetime(df["fecha_registro"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
    faltan = fecha.isna()
    fecha[faltan] = pd.to_datetime(df.loc[faltan, "fecha_registro"], format="%d/%m/%Y %H:%M", errors="coerce")
    df["fecha_registro"] = fecha.dt.strftime("%Y-%m-%d %H:%M:%S")
    df["mes"] = fecha.dt.strftime("%Y-%m")

    # 5. Sin fecha válida o sin columnas obligatorias, la fila no sirve
    df = df.dropna(subset=COLUMNAS_OBLIGATORIAS)

    # 6. Por si la normalización dejó copias exactas
    df = df.drop_duplicates()

    eliminadas = filas_inicio - len(df)

    print("\n--- Resultado ---")
    print("shape:", df.shape)
    print("Nulos por columna:")
    print(df.isna().sum())
    print(f"Filas eliminadas: {eliminadas} (de {filas_inicio})")

    os.makedirs(os.path.dirname(RUTA_SALIDA), exist_ok=True)
    df.to_csv(RUTA_SALIDA, index=False, encoding="utf-8")
    print("Guardado:", RUTA_SALIDA, df.shape)


if __name__ == "__main__":
    main()
