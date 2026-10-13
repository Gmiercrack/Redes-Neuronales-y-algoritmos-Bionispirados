"""Algoritmo evolutivo (esquema de clase) y evolución diferencial generacional.

Notas de implementación:
- DE es generacional (síncrona): los candidatos de una generación se
  calculan todos contra la población actual y la población se reemplaza al
  final de la generación. Variante DE/rand/1/bin (Storn & Price, 1997).
- Toda evaluación de f pasa por el Contador (presupuesto duro,
  registro de eventos reales). El evolutivo hace exactamente 100x50 = 5000
  evaluaciones; DE hace 50 iniciales + generaciones completas hasta agotar el
  presupuesto (99x50 -> 5000 exactas).
"""
import numpy as np
from numpy.random import SeedSequence, default_rng

from instrumentacion import PresupuestoAgotado


def _spawn(seed, n):
    """Deriva n flujos independientes (rng y pob_inicial no deben
    compartir el mismo default_rng(seed)). Acepta int o SeedSequence."""
    ss = seed if isinstance(seed, SeedSequence) else SeedSequence(seed)
    return ss.spawn(n)


def pob_inicial(N, dim, lim_inf, lim_sup, seed=1983):
    rng = default_rng(seed)
    return rng.uniform(lim_inf, lim_sup, size=(N, dim))


def elitismo(poblacion_ordenada, frac_e):
    n = len(poblacion_ordenada)
    n_elite = max(1, int(round(n * frac_e)))
    return poblacion_ordenada[:n_elite].copy()


def mutacion_gaussiana(poblacion, frac_m, lim_inf, lim_sup, rng):
    n, m = poblacion.shape
    n_mut = max(1, int(n * frac_m))
    idx = rng.choice(n, n_mut, replace=False)
    coord = rng.choice(m, n_mut, replace=True)
    desv = poblacion.std(axis=0)[coord]
    nuevos = poblacion[idx, coord] + rng.standard_normal(n_mut) * desv
    mutada = poblacion.copy()
    mutada[idx, coord] = np.clip(nuevos, lim_inf[coord], lim_sup[coord])
    return mutada[idx]


def cruzamiento_un_punto(poblacion, frac_c, rng):
    n, m = poblacion.shape
    n_cru = max(2, int(n * frac_c) + (int(n * frac_c) % 2))
    idx = rng.choice(n, n_cru, replace=False)
    n_pares = n_cru // 2
    padres, madres = poblacion[idx[:n_pares]], poblacion[idx[n_pares:n_cru]]
    hijos = np.zeros((n_cru, m))
    for i in range(n_pares):
        # punto de cruce en [1, m-1]: siempre hay intercambio real.
        # (rng.choice(m) incluiría p=0, que en 2D clonaría a los padres
        # con probabilidad 1/2.)
        p = rng.integers(1, m)
        hijos[i] = np.concatenate((padres[i, :p], madres[i, p:]))
        hijos[n_pares + i] = np.concatenate((madres[i, :p], padres[i, p:]))
    return hijos


def _aptitud(P, cont, lim_inf, lim_sup):
    """Evalúa la población; fuera de límites -> inf SIN gastar evaluación."""
    vals = np.empty(len(P))
    for j, ind in enumerate(P):
        if np.all((ind >= lim_inf) & (ind <= lim_sup)):
            vals[j] = cont.eval_f(ind)
        else:
            vals[j] = np.inf
    return vals


def _limites(dim, lim_inf, lim_sup):
    li = np.full(dim, lim_inf) if np.isscalar(lim_inf) else np.asarray(lim_inf)
    ls = np.full(dim, lim_sup) if np.isscalar(lim_sup) else np.asarray(lim_sup)
    return li, ls


def evolutivo(cont, dim, lim_inf, lim_sup, N=50, frac_e=0.15, frac_m=0.1,
              frac_c=0.75, n_gen=100, seed=1983):
    """Esquema de clase. Retorna {"motivo", "f_final"}; lo mejor queda en cont.

    Presupuesto exacto: 1 evaluación de la población inicial + (n_gen-1)
    generaciones = n_gen*N evaluaciones (con N=50, n_gen=100 -> 5000).
    """
    s_init, s_ops = _spawn(seed, 2)
    rng = default_rng(s_ops)
    lim_inf, lim_sup = _limites(dim, lim_inf, lim_sup)
    pob = pob_inicial(N, dim, lim_inf, lim_sup, s_init)
    motivo, f_final = "max_iter", np.inf
    try:
        fit = _aptitud(pob, cont, lim_inf, lim_sup)  # población inicial (N)
        for _ in range(n_gen - 1):
            orden = np.argsort(fit)
            elite = elitismo(pob[orden], frac_e)
            mut = mutacion_gaussiana(pob, frac_m, lim_inf, lim_sup, rng)
            cru = cruzamiento_un_punto(pob, frac_c, rng)
            pob = np.concatenate([elite, mut, cru])[:N]
            fit = _aptitud(pob, cont, lim_inf, lim_sup)
        f_final = float(np.min(fit[np.isfinite(fit)])) if np.any(np.isfinite(fit)) else np.inf
    except PresupuestoAgotado:
        pass
    motivo = "presupuesto" if cont.n_f >= cont.max_evals else "max_iter"
    return {"motivo": motivo, "f_final": f_final}


def evolucion_diferencial(cont, dim, lim_inf, lim_sup, N=50, F=0.8, CR=0.9,
                          seed=1983):
    """DE/rand/1/bin generacional (Storn & Price, 1997).

    Por generación: cada individuo i genera un candidato u_i = cruce_binomial(
    x_i, x_r1 + F*(x_r2 - x_r3) ) usando la población ACTUAL; la selección
    (glotona) se aplica sobre la población nueva al final de la generación.
    El bucle avanza por generaciones completas mientras quepa una generación
    (N evaluaciones) en el presupuesto.
    """
    s_init, s_ops = _spawn(seed, 2)
    rng = default_rng(s_ops)
    lim_inf, lim_sup = _limites(dim, lim_inf, lim_sup)
    pob = pob_inicial(N, dim, lim_inf, lim_sup, s_init)
    motivo, f_final, n_gens = "max_iter", np.inf, 0
    try:
        fit = _aptitud(pob, cont, lim_inf, lim_sup)  # población inicial
        while cont.queda() >= N:
            pob_nueva = np.empty_like(pob)
            fit_nueva = np.empty(N)
            for i in range(N):
                r1, r2, r3 = rng.choice([j for j in range(N) if j != i],
                                        3, replace=False)
                v = pob[r1] + F * (pob[r2] - pob[r3])       # mutación diferencial
                j_rand = rng.integers(dim)
                mascara = rng.random(dim) < CR              # cruce binomial
                mascara[j_rand] = True
                u = np.clip(np.where(mascara, v, pob[i]), lim_inf, lim_sup)
                fu = cont.eval_f(u)
                if fu <= fit[i]:                            # selección glotona
                    pob_nueva[i], fit_nueva[i] = u, fu
                else:
                    pob_nueva[i], fit_nueva[i] = pob[i], fit[i]
            pob, fit = pob_nueva, fit_nueva
            n_gens += 1
        f_final = float(np.min(fit[np.isfinite(fit)])) if np.any(np.isfinite(fit)) else np.inf
    except PresupuestoAgotado:
        pass
    motivo = "presupuesto" if cont.n_f >= cont.max_evals else "max_iter"
    return {"motivo": motivo, "f_final": f_final, "n_gens": n_gens}
