"""
Algoritmo genético (AG) para el TSP de las 47 capitales de provincia de la España peninsular.

Representación
    Cada individuo es una PERMUTACIÓN de las ciudades 0..N-1: el orden de visita.
    El recorrido es cerrado: después de la última ciudad se vuelve a la primera.

Función objetivo (se minimiza)
    f(r) = sum_{k=0}^{N-1} C[r_k, r_{(k+1) mod N}]
    donde C es la matriz de costos de costos.py (tiempo + peajes + combustible).
    C puede ser asimétrica: el sentido del recorrido importa.

Ciclo de cada generación
    1. Elitismo: los `elitismo` mejores individuos pasan sin cambios.
    2. Selección por torneo: se toman `tam_torneo` individuos al azar y gana el de menor costo.
    3. Cruce de orden OX (Davis, 1985) con probabilidad `prob_cruce`: el hijo copia un
       segmento del padre 1 y completa las demás posiciones con las ciudades que faltan,
       en el orden en que aparecen en el padre 2. Así el hijo siempre es una permutación válida.
    4. Mutación con probabilidad `prob_mutacion`:
         - "inversion":  invierte el segmento r[i..j]   (equivale a un movimiento 2-opt)
         - "intercambio": intercambia r[i] y r[j]
    5. Se evalúan los hijos nuevos (las élites ya tienen su costo calculado).

Conteo de evaluaciones
    Una evaluación = calcular f(r) para un recorrido completo. Se cuentan la población
    inicial y cada hijo nuevo; las élites no se vuelven a contar.

Salidas (carpeta resultados/ga, o la que se indique con --salida)
    resumen.json              configuración, mejor costo, estadísticas y recorrido
    mejor_ruta.csv            mejor recorrido tramo a tramo con cada componente de costo
    historial.csv             mejor costo y costo medio por generación (curva de convergencia)
    corridas.csv              una fila por corrida
    rutas_por_generacion.csv  mejor ruta encontrada hasta cada generación (para el GIF)
    Este script no hace figuras: el mapa y el GIF se generan en un script aparte.

Uso
    python algoritmo_genetico.py                       # usa config_tsp.json
    python algoritmo_genetico.py --generaciones 300 --tam-poblacion 100 --valor-hora 25
    python algoritmo_genetico.py --corridas 30         # 30 corridas, semillas semilla+r
    python algoritmo_genetico.py --help
"""

import argparse
import json
import os
import platform
import sys
import time

import numpy as np
import pandas as pd

from costos import DIR_PARTE2, cargar_config, construir_costos, costo_ruta, desglose_ruta


# ---------------------------------------------------------------------------
# Operadores genéticos
# ---------------------------------------------------------------------------

def costos_poblacion(pob, C):
    """Costo de cada recorrido de la población (vectorizado).

    pob tiene forma (M, N). np.roll(pob, -1, axis=1) da la ciudad siguiente de cada
    posición, incluido el regreso de la última a la primera.
    """
    return C[pob, np.roll(pob, -1, axis=1)].sum(axis=1)


def seleccion_torneo(rng, costos, tam_torneo):
    """Devuelve el índice del ganador de un torneo entre `tam_torneo` individuos al azar."""
    candidatos = rng.integers(0, len(costos), size=tam_torneo)
    return candidatos[np.argmin(costos[candidatos])]


def cruce_ox(rng, p1, p2):
    """Cruce de orden (OX).

    Ejemplo con N = 8, segmento a=2..b=4 del padre 1:
        p1    = [0 1 | 2 3 4 | 5 6 7]
        p2    = [4 7 | 1 0 6 | 2 5 3]
        hijo  = [_ _ | 2 3 4 | _ _ _]
    Se recorre p2 empezando después de b (posición 5): 2 5 3 4 7 1 0 6, se quitan las que
    ya están (2, 3, 4) -> 5 7 1 0 6, y se colocan desde la posición 5 dando la vuelta:
        hijo  = [0 6 | 2 3 4 | 5 7 1]
    """
    n = len(p1)
    a, b = np.sort(rng.choice(n, size=2, replace=False))
    hijo = np.full(n, -1, dtype=p1.dtype)
    hijo[a:b + 1] = p1[a:b + 1]

    usada = np.zeros(n, dtype=bool)
    usada[hijo[a:b + 1]] = True

    orden_p2 = np.roll(p2, -(b + 1))            # p2 leído a partir de la posición b+1
    faltantes = orden_p2[~usada[orden_p2]]      # ciudades de p2 que el hijo aún no tiene
    posiciones = (np.arange(b + 1, b + 1 + len(faltantes))) % n
    hijo[posiciones] = faltantes
    return hijo


def mutar(rng, ind, tipo):
    """Mutación por inversión de un segmento o por intercambio de dos ciudades."""
    ind = ind.copy()
    i, j = np.sort(rng.choice(len(ind), size=2, replace=False))
    if tipo == "inversion":
        ind[i:j + 1] = ind[i:j + 1][::-1]
    elif tipo == "intercambio":
        ind[i], ind[j] = ind[j], ind[i]
    else:
        raise ValueError(f"Tipo de mutación desconocido: {tipo}")
    return ind


def es_permutacion(ruta, n):
    return len(ruta) == n and np.array_equal(np.sort(ruta), np.arange(n))


# ---------------------------------------------------------------------------
# Algoritmo genético
# ---------------------------------------------------------------------------

def algoritmo_genetico(C, tam_poblacion=200, generaciones=1500, prob_cruce=0.9,
                       prob_mutacion=0.3, tam_torneo=3, elitismo=2,
                       tipo_mutacion="inversion", semilla=1983):
    """Ejecuta el AG sobre la matriz de costos C (N x N).

    Devuelve un diccionario con la mejor ruta, su costo, el número de evaluaciones,
    el historial por generación y la mejor ruta encontrada hasta cada generación.
    """
    if not 0 <= elitismo < tam_poblacion:
        raise ValueError("elitismo debe estar entre 0 y tam_poblacion - 1")
    rng = np.random.default_rng(semilla)
    n = C.shape[0]

    # Población inicial: permutaciones aleatorias
    pob = np.array([rng.permutation(n) for _ in range(tam_poblacion)])
    costos = costos_poblacion(pob, C)
    n_eval = tam_poblacion

    k = int(np.argmin(costos))
    mejor_ruta, mejor_costo = pob[k].copy(), float(costos[k])
    historial = [(0, mejor_costo, float(costos.min()), float(costos.mean()), n_eval)]
    # Mejor ruta encontrada hasta cada generación (la 0 es la mejor de la población inicial)
    rutas_por_generacion = [mejor_ruta.copy()]

    for g in range(1, generaciones + 1):
        orden = np.argsort(costos)

        # 1. Elitismo
        elites = pob[orden[:elitismo]]
        costos_elites = costos[orden[:elitismo]]

        # 2-4. Selección, cruce y mutación para completar la población
        hijos = np.empty((tam_poblacion - elitismo, n), dtype=pob.dtype)
        for h in range(len(hijos)):
            p1 = pob[seleccion_torneo(rng, costos, tam_torneo)]
            p2 = pob[seleccion_torneo(rng, costos, tam_torneo)]
            hijo = cruce_ox(rng, p1, p2) if rng.random() < prob_cruce else p1.copy()
            if rng.random() < prob_mutacion:
                hijo = mutar(rng, hijo, tipo_mutacion)
            hijos[h] = hijo

        # 5. Evaluación de los hijos nuevos
        costos_hijos = costos_poblacion(hijos, C)
        n_eval += len(hijos)

        pob = np.vstack([elites, hijos])
        costos = np.concatenate([costos_elites, costos_hijos])

        k = int(np.argmin(costos))
        if costos[k] < mejor_costo - 1e-9:
            mejor_ruta, mejor_costo = pob[k].copy(), float(costos[k])
        historial.append((g, mejor_costo, float(costos.min()), float(costos.mean()), n_eval))
        rutas_por_generacion.append(mejor_ruta.copy())

    assert es_permutacion(mejor_ruta, n), "La mejor ruta no es una permutación válida"
    assert abs(costo_ruta(mejor_ruta, C) - mejor_costo) < 1e-6 * max(1.0, mejor_costo)

    return {
        "mejor_ruta": mejor_ruta,
        "mejor_costo": mejor_costo,
        "evaluaciones": n_eval,
        "historial": pd.DataFrame(historial, columns=[
            "generacion", "mejor_hasta_ahora", "mejor_generacion", "media_generacion", "evaluaciones"]),
        "rutas_por_generacion": rutas_por_generacion,
    }


def rotar_a(ruta, inicio):
    """Rota el recorrido cerrado para que empiece en la ciudad `inicio` (el costo no cambia)."""
    ruta = np.asarray(ruta)
    return np.roll(ruta, -int(np.where(ruta == inicio)[0][0]))


# ---------------------------------------------------------------------------
# Línea de comandos
# ---------------------------------------------------------------------------

# (nombre en config, opción de línea de comandos, tipo, ayuda)
PARAMETROS = [
    ("tam_poblacion", "--tam-poblacion", int, "individuos por generación"),
    ("generaciones", "--generaciones", int, "número de generaciones"),
    ("prob_cruce", "--prob-cruce", float, "probabilidad de cruce OX"),
    ("prob_mutacion", "--prob-mutacion", float, "probabilidad de mutar un hijo"),
    ("tam_torneo", "--tam-torneo", int, "individuos por torneo"),
    ("elitismo", "--elitismo", int, "mejores individuos que pasan sin cambios"),
    ("tipo_mutacion", "--tipo-mutacion", str, "inversion | intercambio"),
    ("semilla", "--semilla", int, "semilla aleatoria (corrida r usa semilla + r)"),
    ("corridas", "--corridas", int, "corridas independientes"),
    ("valor_hora_eur", "--valor-hora", float, "valor de la hora del vendedor (€/h)"),
    ("ciudad_inicio", "--ciudad-inicio", str, "ciudad desde la que se reporta el recorrido"),
]


def leer_argumentos(argv=None):
    p = argparse.ArgumentParser(description="Algoritmo genético para el TSP de las capitales de España.")
    p.add_argument("--config", default="config_tsp.json", help="archivo JSON de configuración")
    for _, opcion, tipo, ayuda in PARAMETROS:
        p.add_argument(opcion, type=tipo, default=None, help=ayuda)
    p.add_argument("--salida", default=None, help="carpeta de resultados (por defecto resultados/ga)")
    args = p.parse_args(argv)

    cfg = cargar_config(args.config)
    for clave, opcion, _, _ in PARAMETROS:
        valor = getattr(args, opcion.lstrip("-").replace("-", "_"))
        if valor is not None:
            cfg[clave] = valor
    return args, cfg


def main(argv=None):
    args, cfg = leer_argumentos(argv)
    salida = args.salida or os.path.join(DIR_PARTE2, "resultados", "ga")
    os.makedirs(salida, exist_ok=True)

    datos = construir_costos(cfg)
    nombres, C = datos["nombres"], datos["C"]
    if cfg["ciudad_inicio"] not in nombres:
        sys.exit(f"ciudad_inicio '{cfg['ciudad_inicio']}' no está en la matriz.")
    inicio = nombres.index(cfg["ciudad_inicio"])

    params_ag = {k: cfg[k] for k in ["tam_poblacion", "generaciones", "prob_cruce", "prob_mutacion",
                                     "tam_torneo", "elitismo", "tipo_mutacion"]}
    print(f"TSP: {len(nombres)} ciudades | valor de la hora = {cfg['valor_hora_eur']} €/h")
    print("Parámetros del AG:", params_ag)

    filas, mejor = [], None
    for r in range(cfg["corridas"]):
        semilla = cfg["semilla"] + r
        t0 = time.perf_counter()
        res = algoritmo_genetico(C, semilla=semilla, **params_ag)
        dt = time.perf_counter() - t0
        filas.append({"corrida": r, "semilla": semilla, "mejor_costo_eur": res["mejor_costo"],
                      "evaluaciones": res["evaluaciones"], "tiempo_s": dt})
        print(f"  corrida {r:2d} (semilla {semilla}): costo = {res['mejor_costo']:,.2f} € "
              f"| {res['evaluaciones']} evaluaciones | {dt:.1f} s")
        if mejor is None or res["mejor_costo"] < mejor["mejor_costo"]:
            mejor, mejor["semilla"] = res, semilla

    # --- Resultados de la mejor corrida ---
    ruta = rotar_a(mejor["mejor_ruta"], inicio)
    desglose = desglose_ruta(ruta, datos, cfg["valor_hora_eur"])
    desglose.to_csv(os.path.join(salida, "mejor_ruta.csv"), index=False, encoding="utf-8-sig")
    mejor["historial"].to_csv(os.path.join(salida, "historial.csv"), index=False)

    corridas = pd.DataFrame(filas)
    corridas.to_csv(os.path.join(salida, "corridas.csv"), index=False)

    resumen = {
        "fecha_ejecucion": time.strftime("%Y-%m-%d %H:%M:%S"),
        "python": platform.python_version(), "numpy": np.__version__,
        "configuracion": cfg,
        "mejor_costo_eur": mejor["mejor_costo"], "semilla_mejor": mejor["semilla"],
        "evaluaciones_por_corrida": mejor["evaluaciones"],
        "estadisticas_corridas": {
            "n": len(corridas), "media": corridas["mejor_costo_eur"].mean(),
            "desviacion": corridas["mejor_costo_eur"].std(ddof=1) if len(corridas) > 1 else 0.0,
            "mejor": corridas["mejor_costo_eur"].min(), "peor": corridas["mejor_costo_eur"].max(),
        },
        "totales_mejor_ruta": {
            "distancia_km": desglose["distancia_km"].sum(), "tiempo_h": desglose["tiempo_h"].sum(),
            "costo_tiempo_eur": desglose["costo_tiempo_eur"].sum(),
            "peajes_eur": desglose["peajes_eur"].sum(),
            "combustible_eur": desglose["combustible_eur"].sum(),
        },
        "recorrido": [nombres[i] for i in ruta] + [nombres[ruta[0]]],
    }
    with open(os.path.join(salida, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)

    print(f"\nMejor costo: {mejor['mejor_costo']:,.2f} € (semilla {mejor['semilla']})")
    t = resumen["totales_mejor_ruta"]
    print(f"  {t['distancia_km']:,.0f} km | {t['tiempo_h']:.1f} h | tiempo {t['costo_tiempo_eur']:,.0f} € "
          f"| peajes {t['peajes_eur']:,.0f} € | combustible {t['combustible_eur']:,.0f} €")
    print("Recorrido:", " -> ".join(resumen["recorrido"]))

    # Mejor ruta hasta cada generación, para el script que dibuja el GIF sobre el mapa.
    # Cada fila: generación, costo de esa ruta y las ciudades en orden de visita (separadas
    # por " | "), empezando en ciudad_inicio. El recorrido es cerrado: falta el regreso.
    filas_rutas = []
    for g, r in enumerate(mejor["rutas_por_generacion"]):
        r = rotar_a(r, inicio)
        filas_rutas.append({"generacion": g,
                            "costo_eur": costo_ruta(r, C),
                            "ruta": " | ".join(nombres[i] for i in r)})
    pd.DataFrame(filas_rutas).to_csv(os.path.join(salida, "rutas_por_generacion.csv"),
                                     index=False, encoding="utf-8-sig")

    print(f"Resultados en: {salida}")


if __name__ == "__main__":
    main()
