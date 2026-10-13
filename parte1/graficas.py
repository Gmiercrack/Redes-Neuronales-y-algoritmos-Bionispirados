"""Gráficas Parte 1: curvas de convergencia y boxplots por dimensión + GIFs (2D)."""
import json
import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from funciones import FUNCIONES
from descenso_gradiente import descenso_gradiente
from evolutivos import evolucion_diferencial, pob_inicial
from instrumentacion import Contador

BASE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(BASE, "resultados")
METODOS = ["GD_analitico", "GD_numerico", "GD_backtracking",
           "Evolutivo", "PSO", "DE"]
COLORES = {"GD_analitico": "tab:blue", "GD_numerico": "tab:cyan",
           "GD_backtracking": "tab:olive", "Evolutivo": "tab:orange",
           "PSO": "tab:green", "DE": "tab:red"}
NOMBRES = {"GD_analitico": "GD analítico", "GD_numerico": "GD numérico",
           "GD_backtracking": "GD backtracking", "Evolutivo": "Evolutivo",
           "PSO": "PSO", "DE": "Evol. diferencial"}


def cargar(dim, base=None):
    d = os.path.join(base or RES, f"dim{dim}")
    with open(os.path.join(d, "curvas.json")) as fh:
        curvas = json.load(fh)
    df = pd.read_csv(os.path.join(d, "corridas.csv"))
    return curvas, df, d


def curva_mediana(curvas, funcion, metodo, presupuesto):
    """Mediana del mejor valor vs evaluaciones, desde eventos reales."""
    xs = np.linspace(1, presupuesto, 200)
    series = []
    for key, h in curvas.items():
        f_, m_, _ = key.split("|")
        if f_ != funcion or m_ != metodo:
            continue
        h = np.array(h, dtype=float)
        h = h[np.isfinite(h[:, 2])]
        if len(h) == 0:
            continue
        xv, yv = h[:, 0], np.minimum.accumulate(h[:, 2])
        series.append(np.interp(xs, xv, yv, left=yv[0], right=yv[-1]))
    return xs, np.median(series, axis=0)


def curva_mediana_efectiva(curvas, funcion, metodo, dim, presupuesto):
    """Mediana del mejor valor vs COSTO EFECTIVO = n_f + 2·dim·n_grad
    (equivalencia propuesta: 1 gradiente analítico ≡ 2n evals de f,
    costo de reemplazo por diferencias centrales; ejemplo del enunciado)."""
    xs = np.linspace(1, presupuesto, 200)
    series = []
    for key, h in curvas.items():
        f_, m_, _ = key.split("|")
        if f_ != funcion or m_ != metodo:
            continue
        h = np.array(h, dtype=float)
        h = h[np.isfinite(h[:, 2])]
        if len(h) == 0:
            continue
        xe = h[:, 0] + 2 * dim * h[:, 1]  # estrictamente creciente
        yv = np.minimum.accumulate(h[:, 2])
        series.append(np.interp(xs, xe, yv, left=yv[0], right=yv[-1]))
    return xs, np.median(series, axis=0)


def convergencia_costo_efectivo(dim, base=None):
    curvas, df, d = cargar(dim, base)
    presupuesto = 5000
    for funcion in FUNCIONES:
        plt.figure(figsize=(8, 5))
        for metodo in METODOS:
            xs, med = curva_mediana_efectiva(curvas, funcion, metodo, dim,
                                             presupuesto)
            plt.plot(xs, med, label=NOMBRES[metodo], color=COLORES[metodo])
        plt.axhline(1e-6, color="k", ls="--", lw=1, label="umbral éxito")
        plt.yscale("log")
        plt.xlabel("Costo efectivo (1 gradiente analítico ≡ 2n evals de f)")
        plt.ylabel("Mediana del mejor valor de f (log)")
        plt.title(f"Convergencia vs costo efectivo — {funcion} ({dim}D)")
        plt.legend(fontsize=8)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(d, f"costo_efectivo_{funcion}.png"), dpi=120)
        plt.close()
    print(f"dim{dim}: curvas de costo efectivo OK")


def convergencia_y_boxplot(dim, base=None):
    curvas, df, d = cargar(dim, base)
    presupuesto = int(df["n_eval_f"].max())
    for funcion in FUNCIONES:
        plt.figure(figsize=(8, 5))
        for metodo in METODOS:
            xs, med = curva_mediana(curvas, funcion, metodo, presupuesto)
            plt.plot(xs, med, label=NOMBRES[metodo], color=COLORES[metodo])
        plt.axhline(1e-6, color="k", ls="--", lw=1, label="umbral éxito")
        plt.yscale("log")
        plt.xlabel("Evaluaciones de f (eventos reales)")
        plt.ylabel("Mediana del mejor valor de f (log)")
        plt.title(f"Convergencia — {funcion} ({dim}D, 30 corridas)")
        plt.legend(fontsize=8)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(d, f"convergencia_{funcion}.png"), dpi=120)
        plt.close()

        datos = [df[(df.funcion == funcion) & (df.metodo == m)]["f_best"].values
                 for m in METODOS]
        plt.figure(figsize=(9, 5))
        # tick_labels (mpl>=3.9) vs labels (deprecado en 3.9+, removido en 3.11)
        _etq = [NOMBRES[m] for m in METODOS]
        try:
            plt.boxplot(datos, tick_labels=_etq, showfliers=False)
        except TypeError:
            plt.boxplot(datos, labels=_etq, showfliers=False)
        plt.yscale("log")
        plt.ylabel("Mejor valor final de f (log)")
        plt.title(f"Distribución del mejor valor — {funcion} ({dim}D, 30 corridas)")
        plt.xticks(rotation=15)
        plt.grid(True, alpha=0.3, axis="y")
        plt.tight_layout()
        plt.savefig(os.path.join(d, f"boxplot_{funcion}.png"), dpi=120)
        plt.close()
    print(f"dim{dim}: curvas y boxplots OK")


def malla(funcion, lo, hi, n=200):
    spec = FUNCIONES[funcion]
    x = np.linspace(lo, hi, n)
    X, Y = np.meshgrid(x, x)
    Z = np.array([[spec["f"](np.array([a, b])) for a in x] for b in x])
    return X, Y, np.log10(np.maximum(Z, 1e-12))


def gif_gd_rastrigin(d):
    """GD atrapado en un mínimo local de Rastrigin (con la eta calibrada)."""
    spec = FUNCIONES["rastrigin"]
    f, grad, (lo, hi) = spec["f"], spec["grad"], spec["dominio"]
    with open(os.path.join(d, "etas.json")) as fh:
        eta_cal = json.load(fh)["rastrigin"]
    cont = Contador(f, 10 ** 9)
    x0 = pob_inicial(1, 2, lo, hi, 1983 + 7)[0]
    # reconstruir trayectoria desde el historial no es posible: se re-corre
    # guardando puntos (solo visualización, fuera del experimento)
    tray = [x0.copy()]
    x = x0.copy()
    for _ in range(400):
        g = grad(x)
        x = x - eta_cal * g
        tray.append(x.copy())
        if np.linalg.norm(g) < 1e-10:
            break
    tray = np.array(tray)
    X, Y, Z = malla("rastrigin", lo, hi)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.contour(X, Y, Z, levels=30, cmap="viridis")
    ax.plot(tray[:, 0], tray[:, 1], "w-", lw=1, alpha=0.6)
    punto, = ax.plot([], [], "ro", ms=8)
    txt = ax.text(0.02, 0.96, "", transform=ax.transAxes, color="white",
                  fontsize=10, bbox=dict(facecolor="black", alpha=0.6))
    ax.set_title(f"Descenso por gradiente en Rastrigin 2D (eta={eta_cal}, semilla 1990)\n"
                 "ilustrativo: corrida independiente, no parte de las 30 estadísticas",
                 fontsize=11)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)

    def upd(i):
        punto.set_data([tray[i, 0]], [tray[i, 1]])
        txt.set_text(f"iter {i}  f={f(tray[i]):.4f}")
        return punto, txt

    ani = FuncAnimation(fig, upd, frames=len(tray), interval=60, blit=True)
    ani.save(os.path.join(d, "gif_gd_rastrigin.gif"), writer=PillowWriter(fps=15))
    plt.close()
    print("gif GD OK")


def gif_de_rastrigin(d):
    """Población de DE convergiendo al óptimo global de Rastrigin."""
    spec = FUNCIONES["rastrigin"]
    f, (lo, hi) = spec["f"], spec["dominio"]
    from evolutivos import _limites, _aptitud
    import numpy as np
    rng = np.random.default_rng(1983)
    li, ls = _limites(2, lo, hi)
    cont = Contador(f, 10 ** 9)
    pob = pob_inicial(40, 2, li, ls, 1983)
    pobs = [pob.copy()]
    fit = _aptitud(pob, cont, li, ls)
    for _ in range(60):
        pn = np.empty_like(pob); fn = np.empty(40)
        for i in range(40):
            r1, r2, r3 = rng.choice([j for j in range(40) if j != i], 3, replace=False)
            v = pob[r1] + 0.8 * (pob[r2] - pob[r3])
            jr = rng.integers(2)
            mask = rng.random(2) < 0.9; mask[jr] = True
            u = np.clip(np.where(mask, v, pob[i]), li, ls)
            fu = cont.eval_f(u)
            pn[i], fn[i] = (u, fu) if fu <= fit[i] else (pob[i], fit[i])
        pob, fit = pn, fn
        pobs.append(pob.copy())
    X, Y, Z = malla("rastrigin", lo, hi)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.contour(X, Y, Z, levels=30, cmap="viridis")
    scat = ax.scatter([], [], c="red", s=18)
    txt = ax.text(0.02, 0.96, "", transform=ax.transAxes, color="white",
                  fontsize=10, bbox=dict(facecolor="black", alpha=0.6))
    ax.set_title("Evolución diferencial en Rastrigin 2D (N=40, F=0.8, CR=0.9, semilla 1983)\n"
                 "ilustrativo: corrida independiente, no parte de las 30 estadísticas",
                 fontsize=11)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)

    def upd(i):
        P = pobs[i]
        scat.set_offsets(P)
        txt.set_text(f"generación {i}  mejor f={min(f(p) for p in P):.2e}")
        return scat, txt

    ani = FuncAnimation(fig, upd, frames=len(pobs), interval=120, blit=True)
    ani.save(os.path.join(d, "gif_de_rastrigin.gif"), writer=PillowWriter(fps=8))
    plt.close()
    print("gif DE OK")


if __name__ == "__main__":
    import sys
    args = [a for a in sys.argv[1:] if not a.startswith("--base")]
    base = None
    for a in sys.argv[1:]:
        if a.startswith("--base="):
            base = a.split("=", 1)[1]
    dims = [int(a) for a in args if a.isdigit()] or [2, 3]
    for dim in dims:
        convergencia_y_boxplot(dim, base)
        convergencia_costo_efectivo(dim, base)
    if 2 in dims:
        d2 = os.path.join(base or RES, "dim2")
        gif_gd_rastrigin(d2)
        gif_de_rastrigin(d2)
