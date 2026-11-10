"""Consultas de la HU Q01 sobre la tabla categorias (proyecto integrador).

Uso (desde la raiz del proyecto):
    python notebook/consultas/consultas_categorias.py data/limpio/categorias_limpio.csv

Lee el CSV limpio, resuelve cinco consultas con pandas (cada una en su
funcion), imprime el titulo y el resultado de cada una y guarda
categorias_consulta_N.csv junto al archivo de entrada.
"""
import sys
import unicodedata
from pathlib import Path

import pandas as pd

# consultas_categorias.py -> consultas -> notebook -> raiz
RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
ARCHIVO_ENTRADA = RAIZ_PROYECTO / "data" / "limpio" / "categorias_limpio.csv"

SIN_AREA = "Sin area"

# Textos con los que limpiar_categorias.py rellena los nulos. Aqui se vuelven
# a tratar como datos faltantes para que las consultas 1 y 4 puedan contarlos.
DESCRIPCION_POR_DEFECTO = "Sin descripcion"
AREA_POR_DEFECTO = "Sin asignar"


def normalizar_texto(valor):
    """Quita espacios y tildes y deja formato 'Titulo'; respeta los nulos."""
    if pd.isna(valor):
        return valor
    sin_tildes = unicodedata.normalize("NFKD", str(valor))
    sin_tildes = "".join(c for c in sin_tildes if not unicodedata.combining(c))
    return " ".join(sin_tildes.split()).title()


def cargar_datos(ruta):
    """Lee el CSV, unifica la escritura de nombre y area, y quita duplicados
    exactos. Devuelve el DataFrame listo y la cantidad de filas leidas."""
    df = pd.read_csv(ruta, encoding="utf-8-sig")
    leidas = len(df)

    # Los textos de relleno de la limpieza vuelven a ser nulos
    df["descripcion"] = df["descripcion"].replace(DESCRIPCION_POR_DEFECTO, pd.NA)
    df["area_responsable"] = df["area_responsable"].replace(AREA_POR_DEFECTO, pd.NA)

    df["nombre"] = df["nombre"].apply(normalizar_texto)
    df["area_responsable"] = df["area_responsable"].apply(normalizar_texto)
    df = df.drop_duplicates().reset_index(drop=True)
    return df, leidas


def consulta_1_resumen(df, leidas):
    """Consulta 1: resumen general (filas, duplicados, categorias y areas distintas,
    y datos faltantes)."""
    resumen = {
        "filas_leidas": leidas,
        "duplicados_exactos_eliminados": leidas - len(df),
        "filas_finales": len(df),
        "categorias_distintas": df["nombre"].nunique(),
        "areas_distintas": df["area_responsable"].nunique(),
        "filas_sin_descripcion": int(df["descripcion"].isna().sum()),
        "filas_sin_area": int(df["area_responsable"].isna().sum()),
    }
    return pd.DataFrame({"metrica": list(resumen), "valor": list(resumen.values())})


def consulta_2_filas_por_categoria(df):
    """Consulta 2 (groupby): cuantas filas hay por cada categoria, de mayor a menor."""
    return (df.groupby("nombre").size()
              .reset_index(name="total")
              .sort_values(["total", "nombre"], ascending=[False, True])
              .reset_index(drop=True))


def consulta_3_filas_por_area(df):
    """Consulta 3 (groupby): cuantas filas y cuantas categorias distintas tiene cada
    area responsable; los nulos se agrupan como 'Sin area'."""
    con_area = df.assign(area_responsable=df["area_responsable"].fillna(SIN_AREA))
    return (con_area.groupby("area_responsable")
                    .agg(total=("id", "count"), categorias=("nombre", "nunique"))
                    .reset_index()
                    .sort_values(["total", "area_responsable"], ascending=[False, True])
                    .reset_index(drop=True))


def consulta_4_filas_incompletas(df):
    """Consulta 4: filas a las que les falta descripcion o area responsable."""
    faltan = df["descripcion"].isna() | df["area_responsable"].isna()
    return df[faltan].sort_values("nombre").reset_index(drop=True)


def consulta_5_categoria_por_area(df):
    """Consulta 5 (groupby): tabla cruzada categoria x area con el numero de filas."""
    con_area = df.assign(area_responsable=df["area_responsable"].fillna(SIN_AREA))
    tabla = (con_area.groupby(["nombre", "area_responsable"]).size()
                     .unstack(fill_value=0))
    tabla.columns.name = None
    return tabla.reset_index()


def mostrar_y_guardar(numero, titulo, resultado, carpeta):
    """Imprime el titulo y el resultado de una consulta y la guarda en
    categorias_consulta_N.csv dentro de la carpeta indicada."""
    print(f"\n=== Consulta {numero}: {titulo} ===")
    print(resultado.to_string(index=False) if len(resultado) else "(sin resultados)")
    ruta = carpeta / f"categorias_consulta_{numero}.csv"
    resultado.to_csv(ruta, index=False, encoding="utf-8")


def main():
    """Punto de entrada: carga el CSV limpio y ejecuta las cinco consultas."""
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else ARCHIVO_ENTRADA
    if not ruta.exists():
        print(f"No se encontro el archivo: {ruta}")
        print("Primero ejecuta: python notebook/limpieza/limpiar_categorias.py data/crudo/categorias_sucio.csv")
        sys.exit(1)

    df, leidas = cargar_datos(ruta)
    carpeta = ruta.resolve().parent
    mostrar_y_guardar(1, "Resumen general de la tabla", consulta_1_resumen(df, leidas), carpeta)
    mostrar_y_guardar(2, "Filas por categoria", consulta_2_filas_por_categoria(df), carpeta)
    mostrar_y_guardar(3, "Filas por area responsable", consulta_3_filas_por_area(df), carpeta)
    mostrar_y_guardar(4, "Filas sin descripcion o sin area", consulta_4_filas_incompletas(df), carpeta)
    mostrar_y_guardar(5, "Categoria por area responsable", consulta_5_categoria_por_area(df), carpeta)


if __name__ == "__main__":
    main()
