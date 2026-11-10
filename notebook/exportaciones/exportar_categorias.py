"""Exporta la tabla `categorias` sucia (HU X01) a CSV, Excel y JSON.

Uso (desde la raiz del proyecto):
    python notebook/exportaciones/exportar_categorias.py

Usa generar_categorias() de simular_categorias.py y guarda los tres archivos
en data/crudo/ con el mismo contenido.
"""

import sys
from pathlib import Path

# Raiz del proyecto: exportar_categorias.py -> exportaciones -> notebook -> raiz
RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.append(str(RAIZ_PROYECTO))

from notebook.simulaciones.simular_categorias import generar_categorias

CARPETA_SALIDA = RAIZ_PROYECTO / "data" / "crudo"


def exportar_categorias(df=None):
    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)
    if df is None:
        df = generar_categorias()

    # utf-8-sig para que Excel abra bien las tildes del CSV
    df.to_csv(CARPETA_SALIDA / "categorias_sucio.csv", index=False, encoding="utf-8-sig")
    df.to_excel(CARPETA_SALIDA / "categorias_sucio.xlsx", index=False)
    # force_ascii=False conserva las tildes; los None salen como null
    df.to_json(CARPETA_SALIDA / "categorias_sucio.json", orient="records",
               force_ascii=False, indent=2)
    return df


if __name__ == "__main__":
    df = exportar_categorias()
    print(f"Exportadas {len(df)} filas a {CARPETA_SALIDA}")
