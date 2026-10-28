# Alternativas que no son la corrida oficial

## `M2-P_prefijos/`: M2-P con el esquema original del plan v5

M2-P entrenado con **un prefijo al azar por dibujo y época** (`esquema_m2p = "prefijos"`), con las semillas 0, 1 y 2. Fue el M2-P oficial hasta el 28 de octubre de 2026. En validación refutó H2: ganó AUC progresiva, pero perdió 1,8, 0,9 y 2,2 puntos de exactitud final frente a M2, y el criterio permite 1.

Por eso se aplicó el plan B del plan v5, el esquema mixto, con la regla fijada **antes** de entrenarlo ("Decisión sobre H2" en `docs/04_entrenamiento_y_busqueda.md`). El mixto cumplió el criterio en las tres semillas y pasó a ser el M2-P oficial (`trabajo/modelos/M2-P_s*`).

Esta carpeta se guarda porque el paper reporta los resultados de validación de **los dos** esquemas. No se evalúa en prueba.

| Carpeta | Contenido |
|---|---|
| `modelos/M2-P_s*/` | Pesos, historial e hiperparámetros |
| `resultados/predicciones_validacion/` | Predicción de cada prefijo de validación |
| `resultados/validacion/` | Métricas, hipótesis, figuras y tablas de validación con este M2-P (M1 y M2 son los mismos que los oficiales) |

Para volver a evaluarlo, por ejemplo con otra métrica, copien esta carpeta a `trabajo_pruebas/` junto con M1, M2 y la búsqueda, y usen `esquema_m2p="prefijos"` (`docs/00_como_ejecutar.md`, sección 7).
