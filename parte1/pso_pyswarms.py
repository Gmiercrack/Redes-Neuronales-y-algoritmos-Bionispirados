"""PSO con PySwarms (librería usada en clase, notebook IRNA202602_PSO).

Notación de clase: b_i^(t) mejor personal, g^(t) mejor global.
Toda evaluación de f pasa por el Contador (presupuesto duro, registro real).
Con n_particles=50 e iters=100 el consumo es exactamente 5000 evaluaciones.
"""
import sys
import importlib
from types import ModuleType

if 'imp' not in sys.modules:  # parche para Python 3.12+ (igual que el notebook)
    _m = ModuleType('imp')
    _m.reload = importlib.reload
    sys.modules['imp'] = _m

import numpy as np
import pyswarms as ps

from instrumentacion import PresupuestoAgotado


class _PararPSO(Exception):
    """Señal interna: detener el enjambre de forma controlada (H2)."""


def pso_pyswarms(cont, dim, lim_inf, lim_sup, n_particles=50, iters=100,
                 c1=0.5, c2=0.3, w=0.9, seed=1983):
    """Retorna {"motivo", "f_final"}; lo mejor queda en cont.

    Si el presupuesto se agota a mitad de un enjambre (p. ej. presupuesto
    configurable menor que n_particles*iters, como en una demo en vivo),
    se detiene de forma controlada y se devuelve lo mejor encontrado.
    """
    np.random.seed(seed)
    bounds = (np.full(dim, lim_inf), np.full(dim, lim_sup))
    options = {'c1': c1, 'c2': c2, 'w': w}
    optimizer = ps.single.GlobalBestPSO(
        n_particles=n_particles, dimensions=dim, options=options,
        bounds=bounds, ftol=1e-12, ftol_iter=10 ** 9)  # sin parada prematura

    def f_contada(X):
        vals = []
        for x in X:
            try:
                vals.append(cont.eval_f(x))
            except PresupuestoAgotado:
                raise _PararPSO()
        return np.array(vals)

    try:
        cost, _ = optimizer.optimize(f_contada, iters=iters, verbose=False)
        f_final = float(cost)
    except _PararPSO:
        f_final = float(cont.mejor)  # mejor encontrado antes de agotar
    motivo = "presupuesto" if cont.n_f >= cont.max_evals else "max_iter"
    return {"motivo": motivo, "f_final": f_final}
