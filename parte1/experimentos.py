"""Experimentos Parte 1 (v5: correcciones de la 4ª auditoría).

Uso oficial (configuración del reporte):
    python experimentos.py --dim 2 --runs 30
    python experimentos.py --dim 3 --runs 30

Para la demo en vivo / exploración, los hiperparámetros se pueden variar:
    python experimentos.py --dim 2 --runs 3 --eta 0.001 --pso-c1 1.5 --pso-w 0.7

Diseño:
- 30 corridas por (función, método); semilla de evaluación: 1983 + r.
  Cada método recibe un flujo aleatorio INDEPENDIENTE derivado con
  SeedSequence.spawn (antes, el x0 del GD era el primer individuo de las
  poblaciones de EA/DE).
- Presupuesto DURO e igual para todos, vía Contador (≤5000 f-evals).
- eta del GD: calibración con rejilla en el rango estable (auditoría 4),
  10 semillas SEPARADAS (7000+r), criterio lexicográfico
  (fracción divergida, mediana). Puede fijarse con --eta.
- Equivalencia de costos (auditoría 4, ejemplo del enunciado):
  1 gradiente analítico ≡ 2n evaluaciones de f (costo de reemplazo por
  diferencias centrales). Se guarda n_costo_efectivo = n_f + 2·dim·n_grad.
- Métricas: f_best (comparación), f_final, motivo, éxito = f_best < 1e-6,
  con conteos k/30 e intervalo de Wilson al 95% (n=30: 3.3% es 1 corrida).
- std con ddof=0 (poblacional), declarado.
"""
import argparse
import json
import os
import time

import numpy as np
import pandas as pd
from numpy.random import SeedSequence

from funciones import FUNCIONES
from descenso_gradiente import descenso_gradiente, descenso_gradiente_backtracking
from evolutivos import evolutivo, evolucion_diferencial, pob_inicial
from pso_pyswarms import pso_pyswarms
from instrumentacion import Contador

BASE = os.path.dirname(os.path.abspath(__file__))
METODOS = ["GD_analitico", "GD_numerico", "GD_backtracking",
           "Evolutivo", "PSO", "DE"]
UMBRAL_EXITO = 1e-6
SEED_BASE = 1983
SEED_CALIB = 7000

# Rejilla de calibración en el rango de estabilidad teórica (eta < 2/L):
# Rastrigin L≈2+40π²≈397 -> eta<5e-3; Rosenbrock exige etas aún menores.
# (La rejilla anterior llegaba a 5e-2: el GD "rebotaba" en vez de descender.
#  v7: refinada entre 1e-4 y 5e-4, donde está el óptimo de Rosenbrock.)
ETAS_GRID = [1e-5, 5e-5, 1e-4, 2e-4, 3e-4, 5e-4, 1e-3, 2e-3, 5e-3]
N_SEEDS_CALIB = 10


def wilson(k, n, z=1.96):
    """Intervalo de Wilson al 95% para una proporción (k éxitos en n)."""
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    den = 1 + z * z / n
    c = p + z * z / (2 * n)
    d = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - d) / den), min(1.0, (c + d) / den))


def calibrar_eta(nombre, dim, presupuesto):
    """Elige eta minimizando (fracción divergida, mediana de f_best).

    Solo se consideran etas estables; la divergencia se penaliza primero
    porque una eta que diverge el 30% de las veces no es un GD utilizable,
    aunque su mediana "rebote" a buenos valores.
    """
    spec = FUNCIONES[nombre]
    f, grad, (lo, hi) = spec["f"], spec["grad"], spec["dominio"]
    mejor = (np.inf, np.inf, ETAS_GRID[0])
    for eta in ETAS_GRID:
        divs, vals = 0, []
        for r in range(N_SEEDS_CALIB):
            seed = SEED_CALIB + r
            cont = Contador(f, presupuesto)
            s = SeedSequence(seed).spawn(1)[0]
            x0 = pob_inicial(1, dim, lo, hi, s)[0]
            res = descenso_gradiente(x0, cont, grad=grad, eta=eta, tol=0)
            if res["motivo"] == "divergencia":
                divs += 1
            elif np.isfinite(cont.mejor):
                vals.append(cont.mejor)
        frac_div = divs / N_SEEDS_CALIB
        med = float(np.median(vals)) if vals else np.inf
        if (frac_div, med) < (mejor[0], mejor[1]):
            mejor = (frac_div, med, eta)
    print(f"    {nombre}: eta={mejor[2]} (div={mejor[0]:.0%}, med={mejor[1]:.2e})")
    return mejor[2]


def correr(nombre, metodo, dim, seed, P):
    """P: namespace con presupuesto e hiperparámetros. Retorna dict de corrida."""
    spec = FUNCIONES[nombre]
    f, grad, (lo, hi) = spec["f"], spec["grad"], spec["dominio"]
    cont = Contador(f, P.presupuesto)
    s_x0, s_ea, s_de, s_pso = SeedSequence(seed).spawn(4)
    x0 = pob_inicial(1, dim, lo, hi, s_x0)[0]
    eta = P.eta if P.eta is not None else P.etas[nombre]

    if metodo == "GD_analitico":
        res = descenso_gradiente(x0, cont, grad=grad, eta=eta)
    elif metodo == "GD_numerico":
        res = descenso_gradiente(x0, cont, grad=None, eta=eta)
    elif metodo == "GD_backtracking":
        res = descenso_gradiente_backtracking(x0, cont, grad)
    elif metodo == "Evolutivo":
        res = evolutivo(cont, dim, lo, hi, N=P.pop, frac_e=P.frac_e,
                        frac_m=P.frac_m, frac_c=P.frac_c,
                        n_gen=P.presupuesto // P.pop, seed=s_ea)
    elif metodo == "PSO":
        res = pso_pyswarms(cont, dim, lo, hi, n_particles=P.pop,
                           iters=P.presupuesto // P.pop,
                           c1=P.pso_c1, c2=P.pso_c2, w=P.pso_w,
                           seed=int(s_pso.generate_state(1)[0]))
    elif metodo == "DE":
        res = evolucion_diferencial(cont, dim, lo, hi, N=P.pop,
                                    F=P.de_f, CR=P.de_cr, seed=s_de)
    else:
        raise ValueError(metodo)

    assert cont.n_f <= P.presupuesto, f"{metodo} excedió el presupuesto"
    cont.cerrar()
    r = cont.resumen()
    f_best = r["f_best"]
    n_ef = r["n_eval_f"] + 2 * dim * r["n_eval_grad"]  # equivalencia 2n
    return {
        "n_eval_f": r["n_eval_f"],
        "n_eval_grad": r["n_eval_grad"],
        "n_costo_efectivo": n_ef,
        "motivo": res["motivo"],
        "f_best": f_best,
        "f_final": res["f_final"],
        "exito": bool(np.isfinite(f_best) and f_best < UMBRAL_EXITO),
        "historial": cont.historial,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dim", type=int, default=2)
    ap.add_argument("--runs", type=int, default=30)
    ap.add_argument("--presupuesto", type=int, default=5000)
    # Hiperparámetros (demo en vivo / exploración). Sin flags = config oficial.
    ap.add_argument("--eta", type=float, default=None,
                    help="fija eta del GD (omite calibración)")
    ap.add_argument("--pop", type=int, default=50)
    ap.add_argument("--de-f", type=float, default=0.8, dest="de_f")
    ap.add_argument("--de-cr", type=float, default=0.9, dest="de_cr")
    ap.add_argument("--pso-c1", type=float, default=0.5, dest="pso_c1")
    ap.add_argument("--pso-c2", type=float, default=0.3, dest="pso_c2")
    ap.add_argument("--pso-w", type=float, default=0.9, dest="pso_w")
    ap.add_argument("--frac-e", type=float, default=0.15, dest="frac_e")
    ap.add_argument("--frac-m", type=float, default=0.1, dest="frac_m")
    ap.add_argument("--frac-c", type=float, default=0.75, dest="frac_c")
    ap.add_argument("--out", type=str, default=None,
                    help="directorio de salida (por defecto resultados/dim{dim}); "
                         "úselo para demos sin pisar los resultados oficiales")
    P = ap.parse_args()
    dim, n_runs, presupuesto = P.dim, P.runs, P.presupuesto

    out = P.out or os.path.join(BASE, "resultados", f"dim{dim}")
    os.makedirs(out, exist_ok=True)

    if P.eta is None:
        print(f"Calibrando eta (dim={dim}, {N_SEEDS_CALIB} semillas 7000+)...")
        P.etas = {nombre: calibrar_eta(nombre, dim, presupuesto)
                  for nombre in FUNCIONES}
    else:
        P.etas = {nombre: P.eta for nombre in FUNCIONES}
        print(f"eta fijada por CLI: {P.eta}")
    with open(os.path.join(out, "etas.json"), "w") as fh:
        json.dump({k: float(v) for k, v in P.etas.items()}, fh, indent=2)

    filas, curvas = [], {}
    t0 = time.time()
    for nombre in FUNCIONES:
        for metodo in METODOS:
            for r in range(n_runs):
                seed = SEED_BASE + r
                t_run = time.perf_counter()
                res = correr(nombre, metodo, dim, seed, P)
                t_run = time.perf_counter() - t_run
                filas.append({"funcion": nombre, "dim": dim, "metodo": metodo,
                              "semilla": seed, "n_eval_f": res["n_eval_f"],
                              "n_eval_grad": res["n_eval_grad"],
                              "n_costo_efectivo": res["n_costo_efectivo"],
                              "motivo": res["motivo"], "f_best": res["f_best"],
                              "f_final": res["f_final"], "exito": res["exito"],
                              "tiempo_s": round(t_run, 3)})
                curvas[f"{nombre}|{metodo}|{r}"] = res["historial"]
            sub = np.array([f["f_best"] for f in filas
                            if f["funcion"] == nombre and f["metodo"] == metodo])
            divs = sum(1 for f in filas if f["funcion"] == nombre
                       and f["metodo"] == metodo and f["motivo"] == "divergencia")
            print(f"{nombre:10s} {metodo:14s} mediana={np.median(sub):.3e} "
                  f"éxito={np.mean(sub < UMBRAL_EXITO):.0%} div={divs}")

    df = pd.DataFrame(filas)
    df.to_csv(os.path.join(out, "corridas.csv"), index=False)

    def agg_wilson(s):
        k = int(s.sum())
        lo, hi = wilson(k, len(s))
        return pd.Series({"exitos_k": k, "wilson_inf": lo, "wilson_sup": hi})

    base = (df.groupby(["funcion", "dim", "metodo"])
              .agg(n=("f_best", "size"),
                   media=("f_best", "mean"),
                   std=("f_best", lambda s: float(np.std(s, ddof=0))),
                   mediana=("f_best", "median"),
                   min=("f_best", "min"),
                   max=("f_best", "max"),
                   tasa_exito=("exito", "mean"),
                   tasa_divergencia=("motivo", lambda s: float((s == "divergencia").mean())),
                   n_eval_f_max=("n_eval_f", "max"))
              .reset_index())
    w = (df.groupby(["funcion", "dim", "metodo"])["exito"]
           .apply(agg_wilson).unstack().reset_index())
    agg = base.merge(w, on=["funcion", "dim", "metodo"])
    agg.to_csv(os.path.join(out, "tabla_resultados.csv"), index=False)

    # Tabla de costo efectivo (equivalencia 1 gradiente = 2n evals de f):
    # mediana y máximo de n_f, n_grad y n_costo_efectivo por configuración.
    (df.groupby(["funcion", "dim", "metodo"])
       .agg(n_eval_f_mediana=("n_eval_f", "median"),
            n_eval_grad_mediana=("n_eval_grad", "median"),
            costo_efectivo_mediana=("n_costo_efectivo", "median"),
            costo_efectivo_max=("n_costo_efectivo", "max"))
       .reset_index()
       .to_csv(os.path.join(out, "tabla_costo_efectivo.csv"), index=False))

    with open(os.path.join(out, "curvas.json"), "w") as fh:
        json.dump(curvas, fh)

    assert (df["n_eval_f"] <= presupuesto).all(), "presupuesto excedido"
    print(f"OK: {len(df)} corridas, ninguna excedió {presupuesto} "
          f"({time.time() - t0:.1f}s) -> {out}")


if __name__ == "__main__":
    main()
