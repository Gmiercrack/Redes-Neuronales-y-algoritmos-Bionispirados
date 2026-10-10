# Trabajo 1 — Parte 1: Optimización numérica y metaheurísticas

Curso: Redes neuronales y algoritmos bioinspirados (UNAL, Facultad de Minas, 2026-02).

Compara descenso por gradiente (analítico, numérico, backtracking), algoritmo
evolutivo (esquema de clase), PSO (PySwarms, como en clase) y evolución
diferencial (DE/rand/1/bin generacional, Storn & Price 1997) sobre Rosenbrock y
Rastrigin (definición estándar), con **presupuesto igual de 5.000 evaluaciones
de f** y 30 corridas por configuración (semillas 1983+r, reproducibles).

## Instalación

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Probado en Python 3.12. `pso_pyswarms.py` incluye el parche del módulo `imp`
que PySwarms 1.3.0 necesita en Python 3.12+ (igual que el notebook de clase).

## Uso

```bash
# verifica funciones y gradientes (2D y 3D)
python funciones.py && python funciones.py 3

# experimentos: 30 corridas por (función, método), presupuesto 5000
python experimentos.py --dim 2 --runs 30
python experimentos.py --dim 3 --runs 30

# gráficas + GIFs (los GIFs solo se generan para dim 2)
python graficas.py 2 3

# verificación automática de consistencia (funciones, presupuesto,
# corridas↔tabla↔curvas, artefactos)
python verificar.py
```

Resultados en `resultados/dim{2,3}/`: `corridas.csv` (una fila por corrida:
semilla, evaluaciones reales de f y de gradiente, motivo de parada, f_best,
f_final, éxito), `tabla_resultados.csv` (agregados), `curvas.json`
(eventos reales de convergencia), `etas.json`, `convergencia_*.png`,
`boxplot_*.png`, `gif_*.gif`.

## Modelo de costos: evaluaciones de f vs. gradiente (auditoría 4)

Unidad de costo: **1 evaluación de f**. Cada corrida registra por separado
`n_eval_f` y `n_eval_grad` (ver `corridas.csv`).

- **GD numérico**: el gradiente por diferencias hacia adelante cuesta d+1
  evaluaciones de f (d nuevas + f(x) reutilizada, como en el notebook de
  clase) → ya incluido en `n_eval_f`. Comparación en igualdad de condiciones.
- **GD analítico / backtracking**: el gradiente analítico no consume f; se
  cuenta aparte en `n_eval_grad` (hasta ~5000). Además se evalúa f una vez
  por iteración para monitorear el progreso (incluido en `n_eval_f`).
- **Evolutivo, PSO, DE**: `n_grad = 0`.

**Equivalencia propuesta y justificada.** 1 gradiente analítico ≡ **2n**
evaluaciones de f. Justificación: es el costo de obtener la misma
información sin fórmula analítica, por diferencias centrales (el ejemplo
del enunciado). Es conservadora: nuestra implementación analítica cuesta
en realidad ~1–2× una evaluación de f (si se reutilizaran intermedios).
Se guarda por corrida `n_costo_efectivo = n_f + 2·dim·n_grad` y las
gráficas incluyen curvas de convergencia contra costo efectivo
(`costo_efectivo_{funcion}.png`), además de las curvas contra `n_f`.
Los agregados por configuración están en
`resultados/dim{2,3}/tabla_costo_efectivo.csv`.

**Robustez.** La comparación a igual `n_f` (declarando el gradiente como
información adicional) es la contabilidad más favorable al GD; bajo
cualquier equivalencia con c>0 los métodos sin gradiente no cambian y el
GD solo puede empeorar su posición relativa. Como el GD pierde en
Rastrigin incluso con la contabilidad más favorable, la conclusión no
depende del c elegido.

## Parámetros: cuáles se fijaron y cuál se calibró (auditoría 4)

| Método | Parámetros | Origen |
|---|---|---|
| GD (3 variantes) | η | **Calibrado**: rejilla [1e-5..5e-3] refinada entre 1e-4 y 5e-4, 10 semillas separadas (7000+r), criterio (fracción divergida, mediana). Ver `etas.json` (v7: rosenbrock 2e-4, rastrigin 1e-5). |
| Evolutivo | N=50, frac_e=0.15, frac_m=0.1, frac_c=0.75, 100 gen | Fijados: esquema y fracciones del notebook de clase |
| PSO | N=50, c1=0.5, c2=0.3, w=0.9, 100 it | Fijados: hiperparámetros del ejemplo de clase (PySwarms) |
| DE | N=50, F=0.8, CR=0.9 | Fijados: valores estándar de Storn & Price (1997) |

Solo se calibró η porque el GD sin calibración no es una línea base
significativa (η es extremadamente sensible); los demás usan elecciones
estándar robustas de la clase/literatura. Se declara explícitamente que
el ranking puede depender de estos parámetros (verificado: PSO con
c1=c2=1.5, w=0.7 llega a 100% en Rastrigin 2D) — material para la
modificación en vivo.

**Dominio.** El GD no está acotado a la caja de búsqueda (como en el
notebook de clase); los métodos poblacionales sí se confinan a ella
(también como en clase). Las funciones están definidas en todo R^n; la
caja es dominio de inicialización/búsqueda. La divergencia se declara
cuando ||x||∞ > 1e6 (ver `DIVERG_NORMA`).

## Limitaciones declaradas (auditoría 5)

- **Calibración de η (Rastrigin):** con η estable, el GD siempre cae en el
  mínimo local más cercano al punto de partida; el destino lo determina
  la cuenca, no el η exacto. La selección entre etas estables es entonces
  casi insensible al criterio (η=1e-5 quedó por desempate, en el borde
  inferior de la rejilla) — cualquiera de ellas cuenta la misma historia.
- **Calibración de η (Rosenbrock):** v7 refinó la rejilla entre 1e-4 y
  5e-4 → η=2e-4 (mediana 0.109, 0% divergencia). El criterio lexicográfico
  sigue siendo conservador (prefiere 0 divergencias antes que mejor
  mediana); el GD de η fija queda penalizado frente al backtracking
  (0.034).
- **Evolutivo reevalúa la élite** (~8/50 ≈ 16% del presupuesto) en cada
  generación sobre fitness ya conocido; DE no lo hace. Se mantiene así
  deliberadamente porque es el esquema literal del notebook de clase
  (`eval_pob` en cada generación); el costo está dentro del presupuesto
  declarado.

## Cómo correr

```bash
pip install -r requirements.txt
python run.py                 # pipeline completo: experimentos 2D+3D, gráficas, verificación
python run.py --dims 2       # solo 2D
```

Para la demo en vivo, los hiperparámetros se varían por CLI
(ver `python experimentos.py --help`): `--eta`, `--pop`, `--de-f`,
`--de-cr`, `--pso-c1`, `--pso-c2`, `--pso-w`, `--frac-e/m/c`.

## Decisiones de diseño (trazabilidad para la auditoría)

- **Presupuesto duro**: toda evaluación de f pasa por `Contador`
  (`instrumentacion.py`); al agotarse se detiene el optimizador. Ninguna
  corrida excede 5000 (verificado automáticamente al final de cada ejecución).
- **Curvas desde eventos reales**: cada evaluación registra
  (n_f, n_grad, mejor); no hay reconstrucciones aproximadas.
- **Métricas**: `f_best` = mejor valor observado (comparación entre métodos);
  `f_final` = valor en el punto final (transparencia). Éxito = f_best < 1e-6.
  `std` con ddof=0 (poblacional).
- **Rastrigin**: se usa la definición estándar. El notebook de clase omite el
  "−A·" antes del coseno (con esa fórmula el mínimo no está en el origen;
  verificado numéricamente).
- **DE**: no se vio en clase; se implementó de Storn & Price (1997), variante
  generacional, sobre el esquema poblacional del curso. Semilla 1983 (canónica
  del curso); la calibración de `eta` usa semillas separadas (7000+r).
- **PSO**: PySwarms `GlobalBestPSO` con hiperparámetros de clase
  {c1: 0.5, c2: 0.3, w: 0.9}. Al GD analítico se le cuenta 1 evaluación de f
  por iteración (monitoreo del progreso); el gradiente analítico es
  información adicional y se declara como tal.
- Los intervalos [-5,5] y [-5.12,5.12] son **dominios de búsqueda** del
  experimento, no el dominio matemático de las funciones.
