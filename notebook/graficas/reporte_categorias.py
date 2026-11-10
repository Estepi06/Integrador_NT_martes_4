"""Reporte grafico de la tabla categorias (HU G01).

Uso (desde la raiz del proyecto):
    python notebook/graficas/reporte_categorias.py data/limpio/categorias_limpio.csv

Lee el CSV limpio, crea tres graficas con matplotlib, las guarda en
data/graficas/ (dpi=120) e imprime la ruta de cada grafica y las conclusiones.
"""
import sys
import unicodedata
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # backend sin ventana: solo guarda archivos
import matplotlib.pyplot as plt
import pandas as pd

# reporte_categorias.py -> graficas -> notebook -> raiz
RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
ARCHIVO_ENTRADA = RAIZ_PROYECTO / "data" / "limpio" / "categorias_limpio.csv"
CARPETA_SALIDA = RAIZ_PROYECTO / "data" / "graficas"

COLUMNAS = ["id", "nombre", "descripcion", "area_responsable"]
SIN_AREA = "Sin área"
AREA_POR_DEFECTO = "Sin asignar"  # texto con el que limpiar_categorias.py rellena los nulos


def normalizar_nombre(valor):
    """Unifica variantes de escritura: quita espacios, tildes y mayusculas."""
    if pd.isna(valor):
        return valor
    texto = unicodedata.normalize("NFKD", str(valor).strip())
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.lower().capitalize()


def cargar_datos(ruta):
    """Lee el CSV y valida que existan las columnas que necesita el reporte."""
    ruta = Path(ruta)
    if not ruta.is_file():
        sys.exit(f"Error: no se encontró el archivo '{ruta}'.\n"
                 "Primero ejecuta: python notebook/limpieza/limpiar_categorias.py "
                 "data/crudo/categorias_sucio.csv")
    df = pd.read_csv(ruta)
    faltan = [c for c in COLUMNAS if c not in df.columns]
    if faltan:
        sys.exit(f"Error: faltan las columnas {faltan} en '{ruta}'.")
    return df


def preparar_datos(df):
    """Deja nombre homogeneo, quita duplicados exactos y unifica el area vacia."""
    df = df.copy()
    df["nombre"] = df["nombre"].map(normalizar_nombre)
    df = df.dropna(subset=["nombre"])
    # "Sin asignar" (relleno de la limpieza) y los nulos se agrupan como "Sin área"
    df["area_responsable"] = df["area_responsable"].replace(AREA_POR_DEFECTO, pd.NA)
    df["area_responsable"] = df["area_responsable"].fillna(SIN_AREA)
    df["area_responsable"] = df["area_responsable"].astype(str).str.strip().str.capitalize()
    df = df.drop_duplicates().reset_index(drop=True)
    return df


def guardar_grafica(fig, nombre_archivo):
    """Aplica tight_layout, guarda con dpi=120, cierra la figura y devuelve la ruta."""
    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)
    ruta = CARPETA_SALIDA / nombre_archivo
    fig.tight_layout()
    fig.savefig(ruta, dpi=120)
    plt.close(fig)
    return ruta


def grafica_1_filas_por_categoria(df):
    """Grafica 1: cuantas filas hay por categoria (barras horizontales)."""
    conteo = df["nombre"].value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(conteo.index, conteo.values, color="#4C72B0")
    for y, valor in enumerate(conteo.values):
        ax.text(valor + 0.3, y, str(valor), va="center")
    ax.set_title("Filas por categoría")
    ax.set_xlabel("Número de filas")
    ax.set_ylabel("Categoría")
    return guardar_grafica(fig, "grafica_1_filas_por_categoria.png")


def grafica_2_filas_por_area(df):
    """Grafica 2: cuantas filas hay por area responsable (barras verticales)."""
    conteo = df["area_responsable"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(conteo.index, conteo.values, color="#55A868")
    for x, valor in enumerate(conteo.values):
        ax.text(x, valor + 0.5, str(valor), ha="center")
    ax.set_title("Filas por área responsable")
    ax.set_xlabel("Área responsable")
    ax.set_ylabel("Número de filas")
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    return guardar_grafica(fig, "grafica_2_filas_por_area.png")


def grafica_3_categoria_por_area(df):
    """Grafica 3: barras apiladas con las filas de cada categoria divididas por area."""
    tabla = df.groupby(["nombre", "area_responsable"]).size().unstack(fill_value=0)
    tabla = tabla.loc[tabla.sum(axis=1).sort_values().index]
    fig, ax = plt.subplots(figsize=(10, 6))
    tabla.plot(kind="barh", stacked=True, ax=ax, colormap="tab20")
    ax.set_title("Filas por categoría y área responsable")
    ax.set_xlabel("Número de filas")
    ax.set_ylabel("Categoría")
    ax.legend(title="Área responsable", bbox_to_anchor=(1.02, 1), loc="upper left")
    return guardar_grafica(fig, "grafica_3_categoria_por_area.png")


def _nombres(serie):
    """Une en texto los indices de una serie (para empates)."""
    return " y ".join(serie.index)


def imprimir_conclusiones(df):
    """Imprime conclusiones calculadas con los datos del DataFrame."""
    por_categoria = df["nombre"].value_counts()
    por_area = df["area_responsable"].value_counts()
    con_area = por_area.drop(SIN_AREA, errors="ignore")
    sin_area = int(por_area.get(SIN_AREA, 0))

    mas_cat = por_categoria[por_categoria == por_categoria.max()]
    menos_cat = por_categoria[por_categoria == por_categoria.min()]
    mas_area = con_area[con_area == con_area.max()]
    menos_area = con_area[con_area == con_area.min()]

    print("\n=== Conclusiones ===")
    print(f"- La tabla tiene {len(df)} filas, {df['nombre'].nunique()} categorías "
          f"y {len(con_area)} áreas responsables.")
    print(f"- Categoría con más filas: {_nombres(mas_cat)} ({mas_cat.iloc[0]} filas).")
    print(f"- Categoría con menos filas: {_nombres(menos_cat)} ({menos_cat.iloc[0]} filas).")
    print(f"- Área con más filas: {_nombres(mas_area)} ({mas_area.iloc[0]} filas).")
    print(f"- Área con menos filas: {_nombres(menos_area)} ({menos_area.iloc[0]} filas).")
    print(f"- {sin_area} filas ({sin_area / len(df):.1%}) no tienen área responsable asignada.")


def main():
    """Punto de entrada: carga y prepara los datos, crea las graficas y las conclusiones."""
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else ARCHIVO_ENTRADA
    df = preparar_datos(cargar_datos(ruta))

    print("Gráficas guardadas en:")
    print(" -", grafica_1_filas_por_categoria(df))
    print(" -", grafica_2_filas_por_area(df))
    print(" -", grafica_3_categoria_por_area(df))
    imprimir_conclusiones(df)


if __name__ == "__main__":
    main()
