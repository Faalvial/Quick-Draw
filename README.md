# ¿Cuántos trazos bastan? Reconocimiento temprano de bocetos con CNN en Quick, Draw!

Proyecto final de CC421 Inteligencia Artificial, UNI, 2026-II.

**Pregunta.** ¿Con cuántos trazos reconoce una CNN un dibujo, y por qué algunas categorías necesitan más?

Se entrenan tres modelos sobre 30 categorías de Quick, Draw! (5 pares confundibles y 20 al azar; 10 000 dibujos reconocidos por categoría) y se evalúan con cada prefijo de cada dibujo:

- **M1**, perceptrón multicapa, como referencia;
- **M2**, CNN entrenada con dibujos completos;
- **M2-P**, la misma CNN entrenada con un prefijo al azar de cada dibujo.

## Empezar

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Faalvial/Quick-Draw/blob/main/notebooks/proyecto_quickdraw.ipynb)

Lean [`docs/00_como_ejecutar.md`](docs/00_como_ejecutar.md). En resumen: abran el notebook en Colab con el botón de arriba (la primera celda clona el repositorio; no hace falta Drive) o clonen el repositorio en su computadora, y ejecuten todo; primero con `MODO_RAPIDO = True` para comprobar que corre (un par de minutos). Drive solo hace falta para reentrenar (sección 1 de `docs/00`). Cada integrante trabaja en su propia rama y su propio módulo: ver "Cómo compartir cambios sin pisarse" en esa misma sección.

El repositorio trae la muestra de datos (`datos/muestra_30`) y la **corrida oficial ya hecha** en `trabajo/`: búsqueda de hiperparámetros, M1, M2 y M2-P con sus semillas, predicciones, métricas, hipótesis, figuras y tablas LaTeX, todo en **validación** (resumen en la sección 10 de `docs/00`). El conjunto de prueba sigue bloqueado hasta la semana 13. Con la corrida hecha, "Ejecutar todas" no entrena nada: solo carga y evalúa.

[![pruebas](https://github.com/Faalvial/Quick-Draw/actions/workflows/pruebas.yml/badge.svg)](https://github.com/Faalvial/Quick-Draw/actions/workflows/pruebas.yml) En cada push, GitHub corre las pruebas automáticas y el notebook en modo rápido.

## Estructura

| Ruta | Qué hay | Documento | Responsable |
|---|---|---|---|
| `notebooks/proyecto_quickdraw.ipynb` | Todo el proyecto, en orden, con "Ejecutar todas" | [00](docs/00_como_ejecutar.md) | Elias |
| `quickdraw/config.py` | Todos los parámetros en un solo lugar | [00](docs/00_como_ejecutar.md) | — |
| `quickdraw/datos.py`, `quickdraw/duracion.py`, `datos/download_sample.py` | Muestra, particiones por dibujo, tabla de hechos, duración | [01](docs/01_datos.md) | Elias |
| `quickdraw/raster.py` | Prefijos, normalización causal, rasterización y caché | [02](docs/02_prefijos_y_rasterizacion.md) | Jorly |
| `quickdraw/modelos.py` | M1, M2 y M2-P | [03](docs/03_modelos.md) | Cristian |
| `quickdraw/entrenar.py` | Entrenamiento, checkpoints y búsqueda de hiperparámetros | [04](docs/04_entrenamiento_y_busqueda.md) | Cristian |
| `quickdraw/metricas.py`, `quickdraw/figuras.py`, `quickdraw/tablas.py` | Exactitud por fracción, AUC progresiva, k*, confusión, figuras y tablas LaTeX | [05](docs/05_metricas.md) | Omar |
| `quickdraw/estadistica.py`, `quickdraw/hipotesis.py` | Bootstrap, McNemar, Spearman y criterios de H1, H2, H4 y H5 | [06](docs/06_estadistica_e_hipotesis.md) | Omar |
| `quickdraw/analisis.py` | Confundibilidad en el espacio de la CNN, t-SNE y pares | [07](docs/07_analisis_h4.md) | Farid |
| `demo/demo.py`, `notebooks/demo.ipynb` | Demo en Gradio | [08](docs/08_demo.md) | Jorly |
| `quickdraw/experimentos.py` | Las etapas que llama el notebook | [00](docs/00_como_ejecutar.md) | — |
| `tests/` | Pruebas automáticas (`pytest tests`) | — | — |
| `datos/muestra_30/` | La muestra: 10 000 reconocidos y 1 000 no reconocidos por categoría | [01](docs/01_datos.md) | Elias |
| `trabajo/` | La corrida oficial (modelos y resultados en validación) | [00](docs/00_como_ejecutar.md) | — |
| `paper/` | Plantilla del paper (IEEE), solo estructura | `paper/README.md` | Farid |

## Hipótesis

| Hip. | Mitad de la pregunta | Se confirma si (en las 3 semillas) |
|---|---|---|
| H1 | ¿Con cuántos trazos? | M2 pierde más de 10 puntos de exactitud a mitad del dibujo, con McNemar p < 0,05 |
| H2 | ¿Con cuántos trazos? | M2-P tiene más AUC progresiva que M2 (IC 95 % > 0) sin perder más de 1 punto al final |
| H5 | ¿Con cuántos trazos? | M2-P acierta de forma estable antes del último trazo en más del 50 % de los dibujos |
| H4 | ¿Por qué algunas necesitan más? | Las categorías más confundibles en el espacio de M2 necesitan más trazos en M2-P (Spearman ρ > 0, p < 0,05) |

## Reproducibilidad

- Semilla de la muestra y de las particiones: 2026. Los `key_id` de cada partición se guardan en `trabajo/resultados/particiones/`.
- Semillas de entrenamiento: 0, 1 y 2.
- El conjunto de prueba se usa una sola vez (semana 13), cambiando `USAR_PRUEBA` a `True`.

## Datos

La muestra de `datos/muestra_30/` sale de *The Quick, Draw! Dataset* de Google Creative Lab, que se distribuye bajo la licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Detalles en [`datos/muestra_30/README.md`](datos/muestra_30/README.md).

## Uso de IA

El código de este repositorio fue generado con asistencia de IA (Claude) a partir del plan del grupo, y revisado y modificado por el grupo. Debe declararse en la DUIA del entregable final.
