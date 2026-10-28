# 04 · Entrenamiento y búsqueda de hiperparámetros

**Archivos:** `quickdraw/entrenar.py`, `quickdraw/experimentos.py` (etapas 2 y 3)
**Responsable en el plan:** Cristian
**Teoría:** sección 3.3.2 (entropía cruzada), 3.4.6 (entrenamiento con dibujos parciales) y 3.6.1 (validación) del avance; sección 3 del plan v5

## Qué hace

### Qué imagen ve cada modelo (`indices_de_epoca`)

- **M1 y M2 (`'completos'`):** en cada época, el dibujo completo de cada dibujo de entrenamiento.
- **M2-P (`'prefijos'`):** en cada época, **un prefijo al azar** de cada dibujo, con k uniforme entre 1 y K. En la época siguiente se sortea otro k.

Cada dibujo aporta una imagen por época en los dos esquemas, así que M2 y M2-P hacen el mismo número de pasos y los dibujos con muchos trazos no pesan más.

### Bucle de entrenamiento (`entrenar`)

- Entropía cruzada, lotes de 256, calendario de tasa de aprendizaje coseno (baja suavemente hasta 0 en `epocas_max`).
- Adam, o SGD con momentum 0,9 (Nesterov).
- Precisión mixta (AMP) cuando hay GPU: casi el doble de rápido en una T4 sin cambiar los resultados de forma apreciable.
- **Parada temprana:** si el objetivo de validación no mejora en 3 épocas (`paciencia`), se detiene y se queda con los pesos de la mejor época.
  - M1 y M2: exactitud con el dibujo completo en validación.
  - M2-P: AUC progresiva en una submuestra fija de 3 000 dibujos de validación.
- Un `checkpoint.pt` por época, para retomar si Colab corta.

### Búsqueda (`busqueda`, `rejilla_m2`, `rejilla_m1`)

- M2: {Adam, SGD} × tasa {0,003, 0,001, 0,0003} × dropout {0, 0,3} = 12 combinaciones, con 5 épocas y el 30 % del entrenamiento.
- M1: las 3 tasas con Adam y dropout 0,3.
- Se elige la combinación con mejor exactitud de validación. **M2-P hereda la de M2.**
- Resultado: `tabla_busqueda.csv` (una tabla del paper) y `hiperparametros_elegidos.json`.

### Semillas

M2 y M2-P se entrenan con las semillas 0, 1 y 2; M1 solo con la 0 (`semillas_m1`). La semilla fija la inicialización, el orden de los lotes y los prefijos sorteados. Las hipótesis se confirman solo si se cumplen en las tres.

## Decisiones y por qué

- **M2-P hereda los hiperparámetros de M2.** Si cada uno tuviera su propia búsqueda, H2 compararía dos cosas a la vez (datos y configuración). Así cambia una sola.
- **La búsqueda es corta (5 épocas, 30 %).** Sirve para ordenar las combinaciones, no para el resultado final. Es la respuesta a "¿por qué esos valores?" en la exposición.
- **Parada temprana de M2-P con la AUC.** *Esto difiere un poco del plan v5,* que dice "exactitud de validación" para todos. M2-P se entrena para acertar temprano; si se detuviera mirando solo el dibujo completo, podría quedarse con una época que acierta al final pero no antes. Si el grupo prefiere seguir el plan al pie de la letra, en `entrenar_o_cargar` cambien `(cfg.esquema_m2p, "auc")` por `(cfg.esquema_m2p, "final")`. Es un cambio de código: no se detecta solo, así que borren antes `trabajo/modelos/M2-P_s*` y `trabajo/resultados/predicciones_*`.
- **Calendario coseno y AMP.** No estaban en el plan; son prácticas estándar que estabilizan el final del entrenamiento y ahorran GPU. Para quitarlos, borren `sched.step()` o pongan `usar_amp = False`.
- **"Quien entrena no evalúa".** Este módulo solo entrena y predice; todas las métricas salen de `metricas.py`.

## Dónde modificar

| Quieren… | Cambien… |
|---|---|
| Otra rejilla | `busqueda_optimizadores`, `busqueda_lr`, `busqueda_dropout` en `Config` |
| Más épocas o más paciencia | `epocas_max`, `paciencia` |
| M1 con 3 semillas (si sobra tiempo) | `semillas_m1=(0, 1, 2)` |
| Entrenar solo un modelo | `E.entrenar_modelos(cfg, D, hp, nombres=("M2-P",))` |
| Elegir hiperparámetros a mano | Editen el diccionario `hp` en el notebook antes de `entrenar_modelos`; si cambian `hp["M2"]`, cambien también `hp["M2-P"]` (debe heredar la misma) |

### Si H2 falla porque M2-P pierde exactitud final

En la corrida oficial (validación, `00_como_ejecutar.md`, sección 10) pasó justo esto: M2-P ganó entre 0,074 y 0,100 de AUC progresiva, pero perdió 1,8, 0,9 y 2,2 puntos de exactitud final con las semillas 0, 1 y 2; el criterio de H2 permite 1, así que H2 queda refutada. Si el grupo decide modificar el método, una opción razonable es **mezclar dibujos completos** en el entrenamiento de M2-P: por ejemplo, con probabilidad 0,5 usar el dibujo completo y si no un prefijo al azar. Ya está implementado: en el notebook, al crear `cfg`, agreguen `esquema_m2p="mixto"` (y si quieren otra proporción, `m2p_prob_completo=0.3`). Para reentrenar M2-P, borren antes `trabajo/modelos/M2-P_s*` y `trabajo/resultados/predicciones_*` o el notebook se detiene avisando que la configuración cambió. Conviene probarlo primero en `trabajo_pruebas` (`00_como_ejecutar.md`, sección 7). En CPU, las tres semillas de M2-P tardaron unas 2 h; en una T4, menos.

Es un cambio de método: debe decidirse con los resultados de **validación** (nunca de prueba) y declararse en el paper.

### Decisión sobre H2 (fijada el 28 de octubre de 2026, antes de entrenar el esquema mixto)

Con el esquema original, M2-P perdió más de 1 punto de exactitud final en validación. Se aplica el plan B que el plan v5 ya preveía para ese caso, con esta regla, escrita **antes** de ver ningún resultado del esquema mixto:

1. **Qué se prueba.** Solo el esquema mixto con `m2p_prob_completo = 0.5`, el valor que ya estaba en `config.py` antes de la corrida oficial. No se prueba ninguna otra proporción ni otro cambio.
2. **Cómo.** M2-P mixto con las semillas 0, 1 y 2, los mismos hiperparámetros (heredados de M2), las mismas particiones y la misma parada temprana con la AUC. Se evalúa solo en **validación**.
3. **Regla para adoptarlo.** El esquema mixto pasa a ser el M2-P oficial si cumple el criterio de H2 **en las tres semillas** (límite inferior del IC 95 % de la diferencia de AUC > 0 y caída de exactitud final ≤ 1 punto). Si no lo cumple, se mantiene el esquema original y H2 se reporta refutada.
4. **Qué se reporta.** En los dos casos, el paper reporta los resultados de validación de **ambos** esquemas y dice que el cambio se decidió con esta regla, antes de la prueba. Si se adopta el mixto, H4 y H5 se reevalúan con él, porque también usan M2-P.
5. **La prueba.** En la semana 13 se evalúa solo el M2-P oficial. El otro esquema queda guardado en `trabajo/alternativas/` para el paper y no se evalúa en prueba.
