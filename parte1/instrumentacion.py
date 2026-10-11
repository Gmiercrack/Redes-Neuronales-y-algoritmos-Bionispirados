"""Instrumentación común de los experimentos (correcciones de auditoría H2-H6).

Diseño:
- Toda evaluación de f pasa por Contador.eval_f. Si el presupuesto se agota,
  lanza PresupuestoAgotado: ningún método puede exceder el límite.
- Cada evaluación real registra (n_f, n_grad, mejor): las curvas de
  convergencia salen de este registro, sin reconstrucciones aproximadas.
- Las evaluaciones de gradiente analítico se cuentan por separado (n_grad);
  el gradiente numérico consume evaluaciones de f (d+1 por gradiente hacia
  adelante) y queda reflejado en n_f automáticamente.
- Motivos de parada explícitos: "convergencia", "presupuesto", "divergencia",
  "line_search_failed", "max_iter".
"""
import numpy as np


class PresupuestoAgotado(Exception):
    """Se lanza cuando una evaluación excedería el presupuesto de f."""


class Contador:
    def __init__(self, f, max_evals):
        self._f = f
        self.max_evals = max_evals
        self.n_f = 0
        self.n_grad = 0
        self.mejor = np.inf
        self.x_mejor = None
        # Historial DISPERSO: se registra cada mejora del mejor valor más el
        # estado final (vía cerrar()). La curva del mejor acumulado queda
        # exactamente determinada (función escalón) con ~50x menos datos
        # que registrar cada evaluación. Cada entrada es (n_f, n_grad, mejor).
        self.historial = []

    def eval_f(self, x):
        """Evalúa f(x) si queda presupuesto; registra el evento real."""
        if self.n_f >= self.max_evals:
            raise PresupuestoAgotado()
        x = np.asarray(x, dtype=float)
        v = float(self._f(x))
        self.n_f += 1
        if np.isfinite(v) and v < self.mejor:
            self.mejor = v
            self.x_mejor = x.copy()
            self.historial.append((self.n_f, self.n_grad, self.mejor))
        return v

    def cerrar(self):
        """Añade el estado final si la última mejora no coincide con n_f."""
        if not self.historial or self.historial[-1][0] != self.n_f:
            self.historial.append((self.n_f, self.n_grad, self.mejor))

    def eval_grad(self, g):
        """Registra una evaluación de gradiente analítico (no consume f)."""
        self.n_grad += 1
        return g

    def queda(self):
        return self.max_evals - self.n_f

    def resumen(self):
        return {
            "n_eval_f": self.n_f,
            "n_eval_grad": self.n_grad,
            "f_best": float(self.mejor),
            "x_best": None if self.x_mejor is None else self.x_mejor.copy(),
        }
