# Muestra de 30 categorías de Quick, Draw!

**Fuente.** *The Quick, Draw! Dataset*, Google Creative Lab, <https://github.com/googlecreativelab/quickdraw-dataset>, formato *simplified* (`https://storage.googleapis.com/quickdraw_dataset/full/simplified/<categoria>.ndjson`).

**Licencia.** Los datos de Google se distribuyen bajo [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Esta carpeta es un subconjunto de esos datos, redistribuido con la misma licencia y con esta atribución. Los únicos cambios son la selección de dibujos y la compresión con gzip: cada línea es el registro original de Google, con los mismos campos y valores.

**Cómo se generó.** Con `datos/download_sample.py`: para cada categoría se recorre el archivo completo y se toma una muestra uniforme con muestreo por reservorio (algoritmo R) y la semilla 2026. Volver a ejecutarlo da exactamente los mismos dibujos.

| Archivo | Contenido |
|---|---|
| `<categoria>.ndjson.gz` | 10 000 dibujos reconocidos (`recognized = true`): los que usa el proyecto |
| `<categoria>_no_reconocidos.ndjson.gz` | 1 000 dibujos no reconocidos (no se usan; ver la pregunta de defensa 7) |
| `<categoria>_hechos.json`, `hechos_avance.csv` | Dibujos en el archivo completo, proporción de reconocidos, mediana de trazos y país más frecuente (Cuadro 2 del avance) |

Cada dibujo tiene `key_id`, `word`, `countrycode`, `timestamp`, `recognized` y `drawing` (lista de trazos `[xs, ys]`). No hay datos personales: el único dato de origen es el país.
