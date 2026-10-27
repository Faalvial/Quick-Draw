# Plantilla del paper (IEEE)

Solo estructura: el texto lo redacta el grupo. Cada sección de `main.tex` tiene, como comentario, quién la redacta y la revisa, la semana del borrador, la extensión, de dónde sale en el avance y qué debe cubrir. Todo sigue la "Nueva distribución del trabajo y del paper".

**En Overleaf:** *New Project → Upload Project* con esta carpeta comprimida. Compilador pdfLaTeX; la clase IEEEtran ya viene instalada.

**Tablas y figuras.** El notebook las genera; no se copian números a mano.

| Copiar de `trabajo/resultados/` | a |
|---|---|
| `validacion/tablas/*.tex` (desde la semana 13, `prueba/tablas/*.tex`) | `tablas/` |
| `validacion/fig_*.png` (desde la semana 13, `prueba/fig_*.png`) | `figuras/` |
| `fig_prefijos.png` | `figuras/` |

Mientras falte un archivo, el PDF muestra un recuadro con su nombre. Lo marcado en rojo con `\pendiente{}` es lo que falta escribir; no debe quedar nada rojo al entregar.

`referencias.bib` es la bibliografía del avance. Guo et al. y Bishop solo aparecen si se citan.

**Numeración.** LaTeX numera figuras y tablas en el orden en que se definen en `main.tex`, así que los pies no llevan número y el texto cita con `\ref{fig:...}` y `\ref{tab:...}`. El orden actual da la numeración del plan (el comentario al inicio de `main.tex` la lista).

**Error "perhaps a missing \item" al compilar.** Aparece mientras el texto no tenga ningún `\cite{...}`: la bibliografía queda vacía. Desaparece con la primera cita.
