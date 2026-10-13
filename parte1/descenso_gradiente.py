"""Descenso por gradiente, variante enseñada en clase, con instrumentación exacta.

Regla de clase: x^(t+1) = x^(t) - eta * grad f(x^(t)), eta fija, parada por
||x^(t+1) - x^(t)|| < tolerancia.

Toda evaluación de f pasa por el Contador (presupuesto duro). El gradiente
numérico usa diferencias hacia adelante como en el notebook de clase
(costo: d evaluaciones de f por gradiente, reutilizando f(x) ya conocido).
El gradiente analítico se cuenta aparte (n_grad).

Cada función retorna {"motivo", "f_final"}; el mejor valor/solución quedan en
cont (f_best, x_best). Motivos: convergencia | presupuesto | divergencia |
line_search_failed | max_iter.
"""
import numpy as np

from instrumentacion import PresupuestoAgotado

# Umbral de divergencia: si ||x||_inf supera este valor, la trayectoria
# abandonó cualquier región de interés (los óptimos están en ||x||<=~2).
# Detecta la divergencia "finita pero astronómica" (p. ej. x~1e33) que el
# chequeo de isfinite no ve, y evita el artefacto numérico del gradiente:
# con x~1e33, h=1e-3 queda bajo el ulp de float64 (~1e17) y f(x+h)==f(x),
# de modo que un gradiente numérico da exactamente 0 y parecería
# "convergencia". La guarda se evalúa ANTES de cualquier chequeo de
# convergencia.
DIVERG_NORMA = 1e6


def _divergio(x):
    return not np.all(np.isfinite(x)) or np.max(np.abs(x)) > DIVERG_NORMA


def _grad_adelante(x, fx, cont, h=1e-3):
    """Diferencias hacia adelante reutilizando fx = f(x): d evaluaciones."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    g = np.empty(n)
    for i in range(n):
        dx = np.zeros(n)
        dx[i] = h
        g[i] = (cont.eval_f(x + dx) - fx) / h
    return g


def descenso_gradiente(x0, cont, grad=None, eta=1e-3, max_iter=100000,
                       tol=1e-8, h=1e-3):
    x = np.asarray(x0, dtype=float).copy()
    motivo = "max_iter"
    try:
        fx = cont.eval_f(x)  # f(x0)
        for _ in range(max_iter):
            if _divergio(x):
                motivo = "divergencia"
                break
            if grad is None:
                g = _grad_adelante(x, fx, cont, h)
            else:
                g = cont.eval_grad(grad(x))
            if not np.all(np.isfinite(g)):
                motivo = "divergencia"
                break
            if np.linalg.norm(g) < 1e-12:
                motivo = "convergencia"
                break
            x_new = x - eta * g
            if _divergio(x_new):
                motivo = "divergencia"
                break
            fx_new = cont.eval_f(x_new)  # monitoreo (1 eval, registra mejor)
            if np.linalg.norm(x_new - x) < tol:
                x, fx = x_new, fx_new
                motivo = "convergencia"
                break
            x, fx = x_new, fx_new
    except PresupuestoAgotado:
        motivo = "presupuesto"
    return {"motivo": motivo, "f_final": float(fx) if np.isfinite(fx) else np.inf}


def descenso_gradiente_backtracking(x0, cont, grad, eta0=1.0, beta=0.5, c=1e-4,
                                    max_iter=100000, tol=1e-8):
    """Line search con backtracking (notas teóricas de clase, condición de Armijo).

    Verifica el presupuesto ANTES de cada evaluación de prueba. Si eta se
    vuelve < 1e-12 sin cumplir Armijo, reporta "line_search_failed" y conserva
    la mejor solución válida (no acepta el paso).
    """
    x = np.asarray(x0, dtype=float).copy()
    motivo = "max_iter"
    try:
        fx = cont.eval_f(x)
        for _ in range(max_iter):
            if _divergio(x):
                motivo = "divergencia"
                break
            g = cont.eval_grad(grad(x))
            if not np.all(np.isfinite(g)):
                motivo = "divergencia"
                break
            ng2 = float(np.dot(g, g))
            if ng2 < 1e-24:
                motivo = "convergencia"
                break
            eta = eta0
            aceptado = False
            while True:
                if cont.queda() <= 0:
                    motivo = "presupuesto"
                    break
                x_new = x - eta * g
                if _divergio(x_new):
                    motivo = "divergencia"
                    break
                f_new = cont.eval_f(x_new)
                if f_new <= fx - c * eta * ng2:
                    aceptado = True
                    break
                eta *= beta
                if eta < 1e-12:
                    motivo = "line_search_failed"
                    break
            if motivo in ("presupuesto", "divergencia"):
                break
            if not aceptado:  # line_search_failed: conserva x válido
                break
            if np.linalg.norm(x_new - x) < tol:
                x, fx = x_new, f_new
                motivo = "convergencia"
                break
            x, fx = x_new, f_new
    except PresupuestoAgotado:
        motivo = "presupuesto"
    return {"motivo": motivo, "f_final": float(fx) if np.isfinite(fx) else np.inf}
