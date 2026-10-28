# Plantilla del paper (IEEE)

Solo estructura: el texto lo redacta el grupo. Cada sección está en su propio archivo de `secciones/`, y `main.tex` solo los junta con `\input`. Cada integrante edita **solo sus archivos**, así nadie pisa el trabajo de otro. El comentario al inicio de cada archivo dice quién la redacta y la revisa, la semana del borrador, la extensión, de dónde sale en el avance y qué debe cubrir, según la "Nueva distribución del trabajo y del paper".

| Archivo | Redacta |
|---|---|
| `00_resumen.tex`, `3e_confundibilidad.tex`, `4c_h4.tex`, `6_conclusiones.tex` | Farid |
| `1_introduccion.tex`, `3a_datos.tex` | Elias |
| `2_trabajo_relacionado.tex`, `3b_prefijos.tex` | Jorly |
| `3c_modelos.tex`, `4a_busqueda.tex` | Cristian |
| `3d_metricas.tex`, `4b_h1_h2_h5.tex` | Omar |
| `5_discusion.tex` | Todos (Elias junta las limitaciones) |

**En Overleaf:** *New Project → Upload Project* con esta carpeta comprimida. Compilador pdfLaTeX; la clase IEEEtran ya viene instalada.

**Tablas y figuras.** El notebook las genera; no se copian números a mano. `figuras/` y `tablas/` ya traen las de validación de la corrida oficial. Para actualizarlas, desde la raíz del repositorio:

```bash
python paper/actualizar_resultados.py           # validación
python paper/actualizar_resultados.py prueba    # desde la semana 13
```

Copia `trabajo/resultados/<partición>/fig_*.png`, `fig_prefijos.png` y `tablas/*.tex`. Si alguien ajusta una figura (por ejemplo `fig_h4.png`), vuelve a ejecutar la sección 5 del notebook y luego este script.

Mientras falte un archivo, el PDF muestra un recuadro con su nombre. Lo marcado en rojo con `\pendiente{}` es lo que falta escribir; no debe quedar nada rojo al entregar.

`referencias.bib` es la bibliografía del avance. Guo et al. y Bishop solo aparecen si se citan.

**Numeración.** LaTeX numera figuras y tablas en el orden en que se definen (el de los archivos de `secciones/`), así que los pies no llevan número y el texto cita con `\ref{fig:...}` y `\ref{tab:...}`. El orden actual da la numeración del plan (el comentario al inicio de `main.tex` la lista).

**Error "perhaps a missing \item" al compilar.** Aparece mientras el texto no tenga ningún `\cite{...}`: la bibliografía queda vacía. Desaparece con la primera cita.
