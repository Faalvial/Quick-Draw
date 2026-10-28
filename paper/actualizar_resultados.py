"""Copia las figuras y tablas que genera el notebook a paper/figuras y paper/tablas.

Uso, desde la raíz del repositorio:
    python paper/actualizar_resultados.py              # resultados de validación
    python paper/actualizar_resultados.py prueba       # desde la semana 13

Así los números del paper nunca se copian a mano y cualquiera puede actualizarlos.
"""
import shutil
import sys
from pathlib import Path

PAPER = Path(__file__).resolve().parent
RESULTADOS = PAPER.parent / "trabajo" / "resultados"


def actualizar(particion: str = "validacion"):
    origen = RESULTADOS / particion
    if not origen.exists():
        sys.exit(f"No existe {origen}: ejecuten antes el notebook (sección 5, o 7 para prueba).")
    copiados = []
    for png in [RESULTADOS / "fig_prefijos.png", *sorted(origen.glob("fig_*.png"))]:
        shutil.copy2(png, PAPER / "figuras" / png.name)
        copiados.append(f"figuras/{png.name}")
    for tex in sorted((origen / "tablas").glob("*.tex")):
        shutil.copy2(tex, PAPER / "tablas" / tex.name)
        copiados.append(f"tablas/{tex.name}")
    print(f"Copiados de {particion}:", ", ".join(copiados))


if __name__ == "__main__":
    actualizar(sys.argv[1] if len(sys.argv) > 1 else "validacion")
