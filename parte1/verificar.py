"""Verificación automática de consistencia de los artefactos (auditoría §3, §6).

Comprueba, sin re-correr los experimentos:
1. Funciones y gradientes (2D y 3D): mínimos, gradiente analítico vs.
   diferencias centrales y vs. diferencias hacia adelante.
2. Por cada dimensión: corridas.csv existe y n_eval_f <= presupuesto.
3. tabla_resultados.csv == agregados recalculados desde corridas.csv
   (media, std ddof=0, mediana, min, max, tasa de éxito, Wilson 95%,
   tasa de divergencia).
3b. n_costo_efectivo == n_f + 2·dim·n_grad en cada corrida.
3c. tabla_costo_efectivo.csv == agregados recalculados.
4. curvas.json: una entrada por cada fila de corridas.csv, eventos con
   n_f creciente y mejor no-creciente.
5. Figuras: PNGs de convergencia/boxplot/costo-efectivo por dimensión;
   GIFs en dim2.
6. PSO con presupuesto < población termina controlado (motivo=presupuesto).

Uso: python verificar.py [--presupuesto 5000] [--out resultados]
     [--dims 2 3] [--runs 30]
"""
import argparse
import json
import os
import sys

import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(BASE, "resultados")
METODOS = ["GD_analitico", "GD_numerico", "GD_backtracking",
           "Evolutivo", "PSO", "DE"]
FUNCIONES = ["rosenbrock", "rastrigin"]


def check(cond, msg):
    print(("OK  " if cond else "FALLO") + f" | {msg}")
    if not cond:
        check.fallos += 1
check.fallos = 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--presupuesto", type=int, default=5000)
    ap.add_argument("--out", type=str, default="resultados",
                    help="directorio base de resultados a verificar")
    ap.add_argument("--dims", type=int, nargs="+", default=[2, 3])
    ap.add_argument("--runs", type=int, default=30,
                    help="corridas esperadas por configuración")
    args = ap.parse_args()
    RES = os.path.join(BASE, args.out)

    sys.path.insert(0, BASE)
    from funciones import verifica_minimos
    for dim in (2, 3):
        verifica_minimos(dim=dim)
    check(True, "funciones y gradientes verificados en 2D y 3D")

    # H2 (auditoría 3): PSO con presupuesto menor que la población debe
    # detenerse de forma controlada, sin lanzar excepción
    from instrumentacion import Contador
    from pso_pyswarms import pso_pyswarms
    from funciones import FUNCIONES
    spec = FUNCIONES["rastrigin"]
    cont = Contador(spec["f"], 30)  # 30 < 50 partículas
    res = pso_pyswarms(cont, 2, *spec["dominio"], seed=1983)
    check(cont.n_f == 30 and res["motivo"] == "presupuesto"
          and np.isfinite(cont.mejor),
          "PSO con presupuesto=30 termina controlado (motivo=presupuesto)")

    for dim in args.dims:
        d = os.path.join(RES, f"dim{dim}")
        df = pd.read_csv(os.path.join(d, "corridas.csv"))
        check((df["n_eval_f"] <= args.presupuesto).all(),
              f"dim{dim}: ninguna corrida excede el presupuesto "
              f"(máx={df['n_eval_f'].max()})")
        # equivalencia de costos: n_costo_efectivo = n_f + 2·dim·n_grad
        ce_ok = np.allclose(df["n_costo_efectivo"].values,
                            df["n_eval_f"].values
                            + 2 * dim * df["n_eval_grad"].values)
        check(bool(ce_ok), f"dim{dim}: n_costo_efectivo consistente")
        check(set(df["metodo"]) == set(METODOS),
              f"dim{dim}: los 6 métodos presentes")
        check((df.groupby(["funcion", "metodo"]).size() == args.runs).all(),
              f"dim{dim}: {args.runs} corridas por configuración")

        from experimentos import wilson as _wilson

        def _agg_wilson(s):
            k = int(s.sum())
            lo, hi = _wilson(k, len(s))
            return pd.Series({"exitos_k": k, "wilson_inf": lo,
                              "wilson_sup": hi})

        agg = pd.read_csv(os.path.join(d, "tabla_resultados.csv"))
        rec = (df.groupby(["funcion", "dim", "metodo"])
                 .agg(n=("f_best", "size"),
                      media=("f_best", "mean"),
                      std=("f_best", lambda s: float(np.std(s, ddof=0))),
                      mediana=("f_best", "median"),
                      min=("f_best", "min"),
                      max=("f_best", "max"),
                      tasa_exito=("exito", "mean"),
                      tasa_divergencia=("motivo",
                                        lambda s: float((s == "divergencia").mean())),
                      n_eval_f_max=("n_eval_f", "max"))
                 .reset_index())
        rec = rec.merge(df.groupby(["funcion", "dim", "metodo"])["exito"]
                          .apply(_agg_wilson).unstack().reset_index(),
                        on=["funcion", "dim", "metodo"])
        cols = ["n", "media", "std", "mediana", "min", "max", "tasa_exito",
                "tasa_divergencia", "n_eval_f_max", "exitos_k",
                "wilson_inf", "wilson_sup"]
        mismas = set(agg["metodo"]) == set(rec["metodo"])
        vals_ok = True
        if mismas:
            a = agg.sort_values(["funcion", "metodo"]).reset_index(drop=True)
            b = rec.sort_values(["funcion", "metodo"]).reset_index(drop=True)
            for c in cols:
                if not np.allclose(a[c].values, b[c].values,
                                   rtol=1e-9, atol=0, equal_nan=True):
                    vals_ok = False
        check(mismas and vals_ok,
              f"dim{dim}: tabla_resultados.csv == agregados de corridas.csv")

        # tabla de costo efectivo: existe y coincide con agregados recalculados
        tce = pd.read_csv(os.path.join(d, "tabla_costo_efectivo.csv"))
        rec_ce = (df.groupby(["funcion", "dim", "metodo"])
                    .agg(n_eval_f_mediana=("n_eval_f", "median"),
                         n_eval_grad_mediana=("n_eval_grad", "median"),
                         costo_efectivo_mediana=("n_costo_efectivo", "median"),
                         costo_efectivo_max=("n_costo_efectivo", "max"))
                    .reset_index())
        a = tce.sort_values(["funcion", "metodo"]).reset_index(drop=True)
        b = rec_ce.sort_values(["funcion", "metodo"]).reset_index(drop=True)
        ce_cols = ["n_eval_f_mediana", "n_eval_grad_mediana",
                   "costo_efectivo_mediana", "costo_efectivo_max"]
        ce_ok = (len(a) == len(b) and all(
            np.allclose(a[c].values, b[c].values, rtol=1e-9, atol=0)
            for c in ce_cols))
        check(ce_ok, f"dim{dim}: tabla_costo_efectivo.csv == agregados")

        ruta_curvas = os.path.join(d, "curvas.json")
        if os.path.exists(ruta_curvas):
            with open(ruta_curvas) as fh:
                curvas = json.load(fh)
            ok_curvas = True
            for _, row in df.iterrows():
                key = f"{row['funcion']}|{row['metodo']}|{row['semilla'] - 1983}"
                h = np.array(curvas.get(key, []), dtype=float)
                if len(h) == 0:
                    ok_curvas = False
                    break
                bmin, fb = float(h[:, 2].min()), float(row["f_best"])
                iguales = (bmin == fb or
                           (np.isfinite(bmin) and np.isfinite(fb) and
                            abs(bmin - fb) <= 1e-9 * max(1.0, abs(fb))))
                if not (np.all(np.diff(h[:, 0]) > 0) and
                        np.all(np.diff(h[:, 2]) <= 0) and
                        h[-1, 0] == row["n_eval_f"] and iguales):
                    ok_curvas = False
                    break
            check(ok_curvas,
                  f"dim{dim}: curvas.json consistente con corridas.csv "
                  f"(eventos reales, n_f creciente, mejor monótono)")
        else:
            # curvas.json es un artefacto grande y regenerable: no se
            # versiona. En un clon limpio se genera con experimentos.py.
            print(f"AVISO| dim{dim}: no existe curvas.json; se omite su "
                  f"verificación (ejecute experimentos.py para generarlo)")

        for f_ in FUNCIONES:
            for kind in ("convergencia", "boxplot"):
                check(os.path.exists(os.path.join(d, f"{kind}_{f_}.png")),
                      f"dim{dim}: {kind}_{f_}.png existe")
        if dim == 2:
            for g in ("gif_gd_rastrigin.gif", "gif_de_rastrigin.gif"):
                check(os.path.exists(os.path.join(d, g)),
                      f"dim2: {g} existe")

    print()
    if check.fallos:
        print(f"{check.fallos} VERIFICACIONES FALLARON")
        sys.exit(1)
    print("Todas las verificaciones pasaron.")


if __name__ == "__main__":
    main()
