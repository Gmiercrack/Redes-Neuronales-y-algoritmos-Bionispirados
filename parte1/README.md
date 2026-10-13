# Parte 1 — Optimización numérica: descenso por gradiente vs. metaheurísticas

Curso: Redes neuronales y algoritmos bioinspirados (UNAL, Facultad de Minas, 2026-02).

Se comparan tres variantes de descenso por gradiente (analítico, numérico y con
*backtracking*), un algoritmo evolutivo (esquema visto en clase), PSO (PySwarms)
y evolución diferencial (DE/rand/1/bin, Storn & Price, 1997) sobre las funciones
de **Rosenbrock** y **Rastrigin** (definición estándar), en 2 y 3 dimensiones.
Todos los métodos reciben el mismo presupuesto de **5000 evaluaciones de f** y se
repiten **30 veces** por configuración (semillas `1983 + r`, reproducibles).

## Instalación

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Probado en Python 3.12 con las versiones fijadas en `requirements.txt`.
`pso_pyswarms.py` incluye el parche del módulo `imp` que PySwarms 1.3.0 necesita
en Python 3.12+ (el mismo que usa el notebook de clase).

## Ejecución

Un solo comando reproduce todo (experimentos 2D y 3D, figuras, GIFs y verificación):

```bash
python run.py
```

Demostración rápida (solo experimentos, sin figuras ni GIFs):

```bash
python run.py --dims 2 --sin-graficas
```

Cualquier ejecución que no sea la oficial (otro número de corridas, otras
dimensiones o hiperparámetros distintos) escribe en `resultados/demo/` y **no
modifica** los resultados oficiales. Con `--out RUTA` se elige otra carpeta (una
ruta relativa se interpreta respecto al directorio actual). `verificar.py` revisa
siempre la carpeta realmente usada.

Los hiperparámetros se cambian por línea de comandos, sin editar el código:

```bash
python run.py --dims 2 --runs 5 --resto --eta 0.001 --pso-c1 1.5 --pso-c2 1.5 --pso-w 0.7
python experimentos.py --help      # lista completa: --eta, --pop, --de-f, --de-cr,
                                   # --pso-c1/c2/w, --frac-e/m/c, --presupuesto
```

Comandos individuales (equivalentes a lo que hace `run.py`):

```bash
python funciones.py && python funciones.py 3   # verifica funciones y gradientes
python experimentos.py --dim 2 --runs 30
python experimentos.py --dim 3 --runs 30
python graficas.py 2 3                         # figuras; los GIFs solo en 2D
python verificar.py                            # consistencia de los artefactos
```

`curvas.json` es un archivo grande y regenerable que no se versiona. En un clon
limpio, `verificar.py` avisa que lo omite hasta que se ejecute `experimentos.py`.

## Resultados

En `resultados/dim{2,3}/`:

| Archivo | Contenido |
|---|---|
| `corridas.csv` | una fila por corrida: semilla, evaluaciones de f y de gradiente, motivo de parada, `f_best`, `f_final`, éxito |
| `tabla_resultados.csv` | media, desviación, mediana, mínimo, máximo, tasa de éxito (con intervalo de Wilson) por función y método |
| `tabla_costo_efectivo.csv` | evaluaciones de f, de gradiente y costo efectivo por método |
| `etas.json` | tasa de aprendizaje calibrada del GD |
| `convergencia_*.png`, `boxplot_*.png`, `costo_efectivo_*.png` | figuras |
| `gif_gd_rastrigin.gif`, `gif_de_rastrigin.gif` | animaciones (solo 2D) |
| `curvas.json` | eventos reales de convergencia (se regenera; no se versiona) |

## Modelo de costos: evaluaciones de f y de gradiente

Unidad de costo: **1 evaluación de f**. Cada corrida registra por separado
`n_eval_f` y `n_eval_grad`.

- **GD numérico:** el gradiente por diferencias hacia adelante cuesta d+1
  evaluaciones de f (d nuevas más f(x) reutilizada, como en el notebook de
  clase); ya está incluido en `n_eval_f`.
- **GD analítico y *backtracking*:** el gradiente analítico no consume f y se
  cuenta aparte en `n_eval_grad`. Además se evalúa f una vez por iteración para
  monitorear el progreso (incluido en `n_eval_f`).
- **Evolutivo, PSO y DE:** `n_eval_grad = 0`.

**Equivalencia propuesta.** 1 gradiente analítico ≡ **2n** evaluaciones de f,
que es el costo de obtener la misma información por diferencias centrales (el
ejemplo del enunciado). Es una elección conservadora: un gradiente analítico
cuesta en la práctica entre 1 y 2 evaluaciones de f. Por corrida se guarda
`n_costo_efectivo = n_f + 2·dim·n_grad` y se grafican curvas de convergencia
contra ese costo (`costo_efectivo_*.png`), además de las curvas contra `n_f`.

Las tablas de resultados comparan a igual `n_f = 5000`, que es la contabilidad
más favorable al GD analítico. A costo efectivo ese método gasta entre 3 y 7
veces más que los demás, de modo que su posición relativa solo puede empeorar
bajo cualquier equivalencia con costo positivo.

## Parámetros

| Método | Parámetros | Origen |
|---|---|---|
| GD (3 variantes) | η | **Calibrado:** rejilla de 9 valores entre 1e-5 y 5e-3 (rango estable), 10 semillas separadas (7000+r), criterio (fracción divergida, mediana). Ver `etas.json`: Rosenbrock 2e-4, Rastrigin 1e-5 |
| Evolutivo | N=50, frac_e=0.15, frac_m=0.1, frac_c=0.75, 100 generaciones | Fijados: esquema y fracciones del notebook de clase |
| PSO | N=50, c1=0.5, c2=0.3, w=0.9, 100 iteraciones | Fijados: hiperparámetros del ejemplo de clase (PySwarms) |
| DE | N=50, F=0.8, CR=0.9 | Fijados: valores habituales de Storn & Price (1997) |

Solo se calibra η porque un GD sin calibrar no es una línea base significativa
(es muy sensible a η). Los demás métodos usan valores estándar de la clase o de
la literatura, así que el ranking puede depender de ellos: por ejemplo, PSO con
c1 = c2 = 1.5 y w = 0.7 alcanza 100 % de éxito en Rastrigin 2D, frente a 3.3 %
con los parámetros de clase. Esto se puede comprobar con la línea de comandos.

## Dominio

El GD no está acotado a la caja de búsqueda (como en el notebook de clase); los
métodos poblacionales sí se confinan a ella. Las funciones están definidas en
todo R^n; los intervalos [-5, 5] (Rosenbrock) y [-5.12, 5.12] (Rastrigin) son el
dominio de inicialización y búsqueda del experimento, no el dominio matemático.
Se declara divergencia cuando ‖x‖∞ > 1e6 (`DIVERG_NORMA`).

## Limitaciones

- **Calibración de η en Rastrigin:** con un η estable el GD cae siempre en el
  mínimo local más cercano al punto de partida; el destino lo determina la cuenca
  y no el valor exacto de η. Por eso la elección entre etas estables es casi
  indiferente (η = 1e-5 queda por desempate, en el borde inferior de la rejilla).
- **Calibración de η en Rosenbrock:** el criterio (fracción divergida, mediana)
  es conservador: prefiere 0 divergencias antes que una mejor mediana. Un η fijo
  queda penalizado frente al *backtracking* (mediana 0.034 en 2D).
- **Evolutivo:** reevalúa la élite en cada generación (unas 8 de 50 evaluaciones,
  ≈16 % del presupuesto) sobre fitness ya conocido; DE no lo hace. Se mantiene
  porque es el esquema literal del notebook de clase, y ese costo está dentro del
  presupuesto declarado.

## Decisiones de diseño

- **Presupuesto duro:** toda evaluación de f pasa por `Contador`
  (`instrumentacion.py`); al agotarse se detiene el optimizador. Ninguna corrida
  excede 5000 evaluaciones (se verifica al final de cada ejecución).
- **Curvas reales:** cada evaluación registra `(n_f, n_grad, mejor)`; no hay
  reconstrucciones aproximadas.
- **Métricas:** `f_best` es el mejor valor observado (para comparar métodos);
  `f_final` es el valor en el punto final. Éxito = `f_best < 1e-6`. La desviación
  usa `ddof=0` (poblacional).
- **Rastrigin:** se usa la definición estándar. El notebook de clase omite el
  factor `A·` delante del coseno; con esa fórmula el mínimo no está en el origen
  (verificado numéricamente).
- **DE:** no se vio en clase; se implementó según Storn & Price (1997), en su
  variante generacional, sobre el esquema poblacional del curso.
- **PSO:** PySwarms `GlobalBestPSO` con `{c1: 0.5, c2: 0.3, w: 0.9}`.
- **Semillas:** las corridas usan `1983 + r` (r = 0…29). Cada método recibe un
  flujo aleatorio independiente (`SeedSequence.spawn`). La calibración de η usa
  semillas separadas (7000 + r).
