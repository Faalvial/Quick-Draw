# 00 · Cómo ejecutar el proyecto

Este documento explica cómo correr todo, qué se guarda, cómo retomar cuando Colab corta la sesión y **qué borrar cuando modifican algo**.

## 1. Dónde trabajar: Colab, Colab con Drive o su computadora

El repositorio ya trae todo lo necesario: el código, la muestra (`datos/muestra_30`, 62 MB) y los modelos y resultados de la corrida oficial (`trabajo/`, ver la sección 10). Cada integrante trabaja con su propia copia; nadie necesita la carpeta de otro.

**a) Colab, sin Drive (lo normal).** Abran el notebook directo desde GitHub: [notebook principal](https://colab.research.google.com/github/Faalvial/Quick-Draw/blob/main/notebooks/proyecto_quickdraw.ipynb) o [demo](https://colab.research.google.com/github/Faalvial/Quick-Draw/blob/main/notebooks/demo.ipynb). La primera celda clona el repositorio en `/content/Quick-Draw` (`COLAB_ORIGEN = "clonar"`). Colab borra `/content` al cerrar la sesión, así que cada sesión vuelve a clonar y a crear la caché de prefijos (unos 10 a 20 min). Alcanza para estudiar, evaluar y todos los experimentos que no reentrenan.

**b) Colab con Drive (solo para reentrenar).** En la primera celda pongan `COLAB_ORIGEN = "drive"`: el repositorio se clona en `MyDrive/quickdraw-early` la primera vez y después se reutiliza, con su caché y sus checkpoints. Así un entrenamiento de horas sobrevive a los cortes de Colab (sección 4). Para traer cambios del repositorio: `!git -C /content/drive/MyDrive/quickdraw-early pull`.

**c) Su computadora.** `git clone https://github.com/Faalvial/Quick-Draw.git` y la sección 9. No hace falta Colab ni Drive; en CPU todo menos reentrenar tarda minutos.

Si borran `datos/muestra_30`, el notebook la vuelve a descargar con `datos/download_sample.py` (unos minutos; sale idéntica por la semilla 2026).

### Cómo compartir cambios sin pisarse

- Cada integrante trabaja en **su propia rama** (`git checkout -b elias`, por ejemplo) y sube sus cambios con un *pull request* a `main`. GitHub corre las pruebas y el modo rápido en cada uno: si algo se rompe, se ve antes de mezclarlo.
- Cada uno toca solo los archivos de su módulo (la tabla "Estructura" del README) y su sección del paper (`paper/secciones/`). Así dos personas nunca editan el mismo archivo.
- `trabajo/` (la corrida oficial) no se modifica en las ramas personales: los experimentos van en `trabajo_pruebas/` (sección 7), que git ignora.
- Para subir cambios hace falta acceso de escritura al repositorio, que da su dueño.

## 2. Primera prueba: modo rápido

1. Abran `notebooks/proyecto_quickdraw.ipynb` con Colab.
2. *Entorno de ejecución → Cambiar tipo de entorno → T4 GPU.*
3. En la primera celda pongan `MODO_RAPIDO = True`.
4. *Entorno de ejecución → Ejecutar todas.*

El modo rápido (`config_rapida` en `quickdraw/config.py`) usa 120 dibujos por categoría y 2 épocas. Tarda alrededor de un minuto y sirve **solo** para comprobar que todo corre de punta a punta. Sus números no significan nada. Guarda todo en `trabajo_rapido/`, separado de la corrida real.

## 3. La corrida real

**La corrida oficial ya está hecha y viene en el repositorio** (`trabajo/`, ver la sección 10). Con `MODO_RAPIDO = False`, "Ejecutar todas" no entrena nada: carga la búsqueda, los modelos y las predicciones, y rehace métricas, hipótesis, figuras y tablas en validación. La primera vez en cada Drive también crea la caché de prefijos, que no se sube al repositorio. En Colab sin Drive la caché se crea en cada sesión. Si después de clonar el notebook recalcula alguna predicción, es normal (git no conserva qué archivo es más nuevo) y tarda unos minutos.

Tiempos medidos en la corrida oficial (CPU de 4 núcleos, sin GPU, 27 de octubre de 2026):

| Etapa | Qué hace | Tiempo medido en CPU | En Colab |
|---|---|---|---|
| Datos | Lee 300 000 dibujos y rasteriza sus 1,87 millones de prefijos (entrenamiento + validación) | 6 min con 4 procesos | 10 a 20 min la primera vez (2 procesos); luego se lee la caché |
| Búsqueda | 12 combinaciones de M2 y 3 de M1, con 5 épocas y el 30 % de los datos | 64 min | ya hecha: solo se lee |
| Entrenamiento | M1 (1 semilla), M2 y M2-P (3 semillas cada uno), hasta 20 épocas | 3 h 33 min (~135 s por época de M2 o M2-P; ~10 s de M1) | ya hecho: solo se carga |
| Evaluación | Métricas, hipótesis y figuras en validación | 14 min la primera vez; ~3 min con las predicciones guardadas | unos minutos |

En total, 4 h 57 min. La caché ocupa unos 1,5 GB en disco y la corrida usó unos 4,6 GB de RAM: cabe en Colab. Si reentrenan algo en una T4, será más rápido que en CPU (AMP se activa solo con GPU).

**Repartir el trabajo entre cuentas.** Cada modelo y cada semilla se guardan en su propia carpeta, así que dos personas pueden entrenar a la vez sobre la misma carpeta compartida sin pisarse. Por ejemplo, en una cuenta:

```python
modelos = E.entrenar_modelos(cfg, D, hp, nombres=("M2",))
```

y en la otra `nombres=("M2-P",)`. Solo hace falta si reentrenan (por ejemplo, el esquema mixto de `04_entrenamiento_y_busqueda.md`). Al final, una sola persona ejecuta todo el notebook: los modelos ya entrenados solo se cargan.

## 4. Retomar cuando Colab corta la sesión

No hay que hacer nada especial: vuelvan a ejecutar todas las celdas. Cada etapa revisa qué ya existe en `trabajo/`:

- la caché de prefijos se lee del disco;
- la búsqueda salta las combinaciones ya probadas;
- un modelo terminado (`modelo.pt`) solo se carga;
- un modelo a medio entrenar sigue desde su `checkpoint.pt`, en la época donde quedó;
- las predicciones guardadas se reutilizan, salvo que el modelo se haya reentrenado después.

## 5. Qué se guarda y dónde

```
trabajo/
  cache/                    prefijos rasterizados (entrenamiento_n10000_r28_..., validacion_..., prueba_...)
  modelos/M2-P_s0/          checkpoint.pt, modelo.pt, historial.json, hiperparametros.json
  resultados/
    tabla_hechos.csv        dibujos, mediana de trazos y país más frecuente por categoría
    particiones/            key_id de cada dibujo en entrenamiento, validación y prueba
    busqueda_M1.json, busqueda_M2.json, tabla_busqueda.csv, hiperparametros_elegidos.json
    fig_prefijos.png
    predicciones_validacion/   predicción de cada modelo para cada prefijo
    validacion/             metricas.csv, metricas_media_desviacion.csv, hipotesis.json,
                            separacion_pares.csv y las figuras fig_*.png
    prueba/                 lo mismo, solo después de la semana 13
```

## 6. Si modifican algo: qué se recalcula solo y qué hay que borrar

El código protege contra la mezcla de resultados viejos y nuevos:

| Si cambian… | Qué pasa |
|---|---|
| Rasterización (`resolucion`, `grosor`, `margen`, `lienzo`), `dibujos_por_categoria` o `semilla_particion` | Se crea una caché nueva (el nombre del archivo lleva esos valores). Los modelos guardados ya no coinciden y el notebook **se detiene con un mensaje** al empezar la búsqueda (antes de gastar tiempo): borren `trabajo/modelos/` y `trabajo/resultados/predicciones_*`. |
| La rejilla de búsqueda | Solo se prueban las combinaciones nuevas; las que salieron de la rejilla se ignoran. |
| Hiperparámetros, `lote`, `epocas_max`, `paciencia` | El notebook se detiene con un mensaje que muestra la configuración guardada y la actual. Borren la carpeta del modelo que quieren reentrenar. |
| La arquitectura (`quickdraw/modelos.py`) o la forma de entrenar (`quickdraw/entrenar.py`) | **Esto no se detecta solo.** Borren `trabajo/modelos/` y `trabajo/resultados/predicciones_*`. |
| Métricas, hipótesis o figuras | Basta con volver a ejecutar la sección 5 del notebook: no hace falta reentrenar. |

Si dudan, borrar `trabajo/` entero siempre es seguro: solo cuesta volver a calcular. Ojo: `trabajo/` trae la corrida oficial del repositorio; si lo borran, recupérenlo con `git checkout -- trabajo`.

## 7. Experimentos de la guía de dominio sin tocar la corrida oficial

Nunca hagan un experimento sobre `trabajo/`: es la corrida oficial. Hay dos casos.

**Experimentos que no reentrenan** (otro número de vecinos, otra perplejidad de t-SNE, bootstrap con 200 remuestreos, matrices de confusión de M2…). Después de ejecutar el notebook completo (todo se carga, nada se entrena), agreguen una celda al final:

```python
cfg_p = replace(cfg, ruta_trabajo=RAIZ / "trabajo_pruebas", vecinos_knn=5)   # el cambio que quieran
R_p = E.evaluar(cfg_p, D, modelos, preds_val, "validacion")
display(R_p["veredictos"])
```

`evaluar` escribe en `trabajo_pruebas/resultados/validacion/` y deja intacto `trabajo/`. Con funciones sueltas (`metricas`, `analisis`, `estadistica`) no se escribe nada en disco.

**Experimentos que reentrenan** (otro grosor, otros dibujos por categoría, el esquema mixto…). En la primera celda pongan `CARPETA_TRABAJO = "trabajo_pruebas"` o `MODO_RAPIDO = True`, y hagan el cambio en la línea `cfg = replace(cfg, ...)` de la segunda celda, que va **después** de `config_rapida` (si no, el modo rápido lo pisa). En `trabajo_pruebas` el notebook reentrena todo con datos completos (horas); en modo rápido tarda minutos pero los números no significan nada: sirve para ver el efecto, no para el paper.

Si un cambio va a quedarse, se decide en grupo con resultados de validación y se anota para el paper.

## 8. El conjunto de prueba (semana 13)

Mientras `USAR_PRUEBA = False`, ninguna función toca los dibujos de prueba: ni se rasterizan, y `predecir_todo(..., "prueba")` lanza un error. En la semana 13, con los modelos congelados:

1. pongan `USAR_PRUEBA = True` en la primera celda;
2. ejecuten todo **una sola vez**;
3. no cambien nada después de ver los resultados de prueba. Si algo sale mal, se reporta tal cual en el paper.

## 9. Fuera de Colab

```bash
pip install -r requirements.txt
cd notebooks && jupyter notebook proyecto_quickdraw.ipynb
```

Fuera de Colab, el notebook usa como raíz la carpeta de arriba de `notebooks/` (o la variable de entorno `QD_RAIZ`). Las pruebas automáticas se ejecutan desde la raíz del repositorio con `pytest tests`.

## 10. La corrida oficial (`trabajo/`)

Hecha el 27 de octubre de 2026 en CPU, con la configuración por defecto de `config.py` (grosor 16, margen 2) y **solo validación**: el conjunto de prueba no se tocó (`USAR_PRUEBA = False`). Está en el repositorio: `trabajo/modelos/` (pesos, historial e hiperparámetros de cada modelo) y `trabajo/resultados/` (búsqueda, particiones, predicciones, métricas, hipótesis, figuras y tablas LaTeX).

- **Búsqueda.** M2: Adam, η = 0,003, sin dropout (79,0 % en validación; la mejor con SGD, 57,6 %). M1: Adam, η = 0,003. M2-P hereda la de M2. La tasa elegida es la más alta de la rejilla.
- **Modelos** (validación, todas las categorías, media ± desviación de 3 semillas): exactitud final M1 72,4 %, M2 82,7 ± 1,2 %, M2-P 81,0 ± 0,6 %; AUC progresiva 0,520, 0,611 ± 0,018 y 0,695 ± 0,004.
- **Hipótesis en validación:** H1, H4 y H5 confirmadas en las tres semillas; **H2 refutada**: M2-P gana AUC en las tres (límite inferior del IC entre 0,072 y 0,097) pero pierde 1,8, 0,9 y 2,2 puntos de exactitud final, y el criterio permite 1. Ver "Si H2 falla" en `04_entrenamiento_y_busqueda.md`.
- **Parada temprana.** M2 con la semilla 1 se detuvo en la época 6 (mejor época, la 3) y quedó en 81,3 %, frente a 83,3 % y 83,5 % de las otras dos. Es la única semilla en la que H2 se cumple.

Los resultados de **prueba** se generan una sola vez, en la semana 13 (sección 8).
