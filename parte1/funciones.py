"""Funciones de prueba para la Parte 1 (implementación dimensionalmente general).

Rosenbrock y Rastrigin en su definición ESTÁNDAR. NOTA: el notebook de clase
define Rastrigin como A*p + sum(x_i^2 + cos(2*pi*x_i)), omitiendo el "-A·"
antes del coseno; con esa fórmula el mínimo NO está en el origen (verificado:
f(0,0)=22 en 2D, mínimo ≈ 18.5 cerca de (±0.5,±0.5)). Aquí se usa la estándar,
con mínimo global f(0,...,0) = 0.

Los intervalos [-5,5] y [-5.12,5.12] son DOMINIOS DE BÚSQUEDA del experimento,
no el dominio matemático completo de las funciones.
"""
import numpy as np


def rosenbrock(x):
    """f(x) = sum_{i=1}^{n-1} [100*(x_{i+1} - x_i^2)^2 + (1 - x_i)^2].
    Mínimo global: x* = (1,...,1), f(x*) = 0. Valle estrecho y curvo."""
    x = np.asarray(x, dtype=float)
    return float(np.sum(100.0 * (x[1:] - x[:-1] ** 2) ** 2 + (1 - x[:-1]) ** 2))


def grad_rosenbrock(x):
    x = np.asarray(x, dtype=float)
    n = len(x)
    g = np.zeros(n)
    for i in range(n):
        if i < n - 1:
            g[i] += -400.0 * x[i] * (x[i + 1] - x[i] ** 2) - 2.0 * (1 - x[i])
        if i > 0:
            g[i] += 200.0 * (x[i] - x[i - 1] ** 2)
    return g


def rastrigin(x, A=10.0):
    """f(x) = A*n + sum(x_i^2 - A*cos(2*pi*x_i)).
    Mínimo global: x* = (0,...,0), f(x*) = 0. Multimodal (~10^n mínimos)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    return float(A * n + np.sum(x ** 2 - A * np.cos(2 * np.pi * x)))


def grad_rastrigin(x, A=10.0):
    x = np.asarray(x, dtype=float)
    return 2 * x + 2 * np.pi * A * np.sin(2 * np.pi * x)


def grad_adelante(x, f, h=1e-3):
    """Gradiente por diferencias hacia adelante (variante del notebook de
    clase). Costo: d+1 evaluaciones de f."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    fx = f(x)
    return np.array([(f(x + h * np.eye(n)[i]) - fx) / h for i in range(n)])


FUNCIONES = {
    "rosenbrock": {
        "f": rosenbrock,
        "grad": grad_rosenbrock,
        "dominio": (-5.0, 5.0),       # dominio de búsqueda (no matemático)
        "x_opt": lambda dim: np.ones(dim),
        "f_opt": 0.0,
    },
    "rastrigin": {
        "f": rastrigin,
        "grad": grad_rastrigin,
        "dominio": (-5.12, 5.12),     # dominio de búsqueda (no matemático)
        "x_opt": lambda dim: np.zeros(dim),
        "f_opt": 0.0,
    },
}


def verifica_minimos(dim=2, n_puntos=5, seed=0):
    """Comprueba en `dim` dimensiones:
    1. f(x*) = f_opt y ||grad(x*)|| ~ 0.
    2. gradiente analítico vs. diferencias centrales (h=1e-7).
    3. (H8) gradiente analítico vs. diferencias hacia ADELANTE (h=1e-3, el que
       usa el GD numérico): reporta el error de aproximación real.
    """
    rng = np.random.default_rng(seed)
    for nombre, spec in FUNCIONES.items():
        f, grad = spec["f"], spec["grad"]
        x_opt = spec["x_opt"](dim)
        assert abs(f(x_opt) - spec["f_opt"]) < 1e-12, nombre
        assert np.linalg.norm(grad(x_opt)) < 1e-8, nombre
        err_cen, err_ade = [], []
        for _ in range(n_puntos):
            x = rng.uniform(*spec["dominio"], size=dim)
            g = grad(x)
            gc = np.array([(f(x + 1e-7 * e) - f(x - 1e-7 * e)) / 2e-7
                           for e in np.eye(dim)])
            ga = grad_adelante(x, f, h=1e-3)
            err_cen.append(np.linalg.norm(g - gc) / max(1e-12, np.linalg.norm(g)))
            err_ade.append(np.linalg.norm(g - ga) / max(1e-12, np.linalg.norm(g)))
        print(f"{nombre} (d={dim}): err_rel central={max(err_cen):.2e}, "
              f"hacia-adelante(h=1e-3)={max(err_ade):.2e}")
        # Umbrales explícitos que hacen fallar la prueba.
        # Central (h=1e-7): error ~1e-9 observado; umbral 1e-5.
        # Hacia adelante (h=1e-3, el que usa el GD): error de truncamiento
        # O(h) ~1e-3 observado; umbral 5e-2. Una fórmula mal daría error O(1).
        assert max(err_cen) < 1e-5, f"{nombre}: gradiente vs central discrepa"
        assert max(err_ade) < 5e-2, f"{nombre}: gradiente vs adelante discrepa"
    print("OK: mínimos y gradientes verificados")


if __name__ == "__main__":
    import sys
    verifica_minimos(dim=int(sys.argv[1]) if len(sys.argv) > 1 else 2)
