"""
Modelo de costos del TSP de las 47 capitales peninsulares.

El costo de ir de la ciudad i a la ciudad j es (enunciado del Trabajo 1):

    C[i, j] = valor_hora * T[i, j]  +  P[i, j]  +  F[i, j]
              (tiempo del vendedor)   (peajes)    (combustible)

Las matrices vienen de la Parte 2 del repositorio (notebook P_viajero_coordenadas.ipynb):
    D[i, j] : distancia por carretera en km     (matriz_distancias_carretera.csv)
    T[i, j] : tiempo de viaje en horas          (matriz_tiempos_carretera.csv)
    P[i, j] : costo de peajes en euros          (matriz_costo_peajes_euros.csv)
    F[i, j] : costo de combustible en euros     (matriz_costo_combustible_euros.csv)

El valor de la hora NO está dentro de ninguna matriz: es un parámetro, para poder
estudiar cómo cambia la ruta óptima al variarlo (--valor-hora).

D no entra en el costo (el combustible ya la incluye); se usa para reportar los km.
Las matrices NO son simétricas: por carretera, i->j puede diferir de j->i.

Este módulo lo pueden usar tanto el algoritmo genético como la colonia de hormigas,
así ambos optimizan exactamente la misma matriz de costos.
"""

import json
import os

import numpy as np
import pandas as pd

DIR_PARTE2 = os.path.dirname(os.path.abspath(__file__))


def cargar_matriz(ruta):
    """Lee una matriz cuadrada guardada como CSV con nombres de ciudad en filas y columnas.

    Devuelve (nombres, matriz) donde matriz es un np.ndarray de forma (N, N).
    """
    df = pd.read_csv(ruta, index_col=0, encoding="utf-8-sig")
    nombres = [str(c).strip() for c in df.index]
    columnas = [str(c).strip() for c in df.columns]
    if nombres != columnas:
        raise ValueError(f"{ruta}: las filas y las columnas no tienen las mismas ciudades en el mismo orden.")
    M = df.to_numpy(dtype=float)
    if np.isnan(M).any():
        raise ValueError(f"{ruta}: la matriz tiene valores vacíos (NaN).")
    return nombres, M


def _ruta_absoluta(ruta):
    return ruta if os.path.isabs(ruta) else os.path.join(DIR_PARTE2, ruta)


def cargar_config(ruta_config):
    """Lee el archivo JSON de configuración (parámetros del modelo de costos y del algoritmo)."""
    with open(_ruta_absoluta(ruta_config), encoding="utf-8") as f:
        cfg = json.load(f)
    # Las claves que empiezan por "_" son comentarios del archivo, no parámetros.
    return {k: v for k, v in cfg.items() if not k.startswith("_")}


def construir_costos(cfg):
    """Construye la matriz de costos total C a partir de las matrices de la Parte 2.

    Devuelve un diccionario con:
        nombres     : lista de N ciudades
        C           : matriz de costos total (euros)
        D, T, P     : distancia (km), tiempo (h), peajes (euros)
        combustible : costo de combustible (euros)
    """
    nombres, D = cargar_matriz(_ruta_absoluta(cfg["archivo_distancias"]))
    matrices = {}
    for clave in ["archivo_tiempos", "archivo_peajes", "archivo_combustible"]:
        nombres_m, M = cargar_matriz(_ruta_absoluta(cfg[clave]))
        if nombres_m != nombres:
            raise ValueError(f"{cfg[clave]} no tiene las mismas ciudades, en el mismo orden, "
                             f"que {cfg['archivo_distancias']}.")
        matrices[clave] = M

    T = matrices["archivo_tiempos"]
    P = matrices["archivo_peajes"]
    F = matrices["archivo_combustible"]

    valor_hora = float(cfg["valor_hora_eur"])
    C = valor_hora * T + P + F
    np.fill_diagonal(C, 0.0)

    return {"nombres": nombres, "C": C, "D": D, "T": T, "P": P, "combustible": F}


def costo_ruta(ruta, C):
    """Costo de un recorrido CERRADO: suma de C[ruta[k], ruta[k+1]] y el regreso a la ciudad inicial."""
    ruta = np.asarray(ruta)
    return float(C[ruta, np.roll(ruta, -1)].sum())


def desglose_ruta(ruta, datos, valor_hora):
    """Tabla tramo a tramo (incluye el regreso) con distancia, tiempo y cada componente de costo."""
    ruta = np.asarray(ruta)
    sig = np.roll(ruta, -1)
    nombres = datos["nombres"]
    filas = []
    for k, (i, j) in enumerate(zip(ruta, sig), start=1):
        filas.append({
            "tramo": k,
            "desde": nombres[i],
            "hasta": nombres[j],
            "distancia_km": datos["D"][i, j],
            "tiempo_h": datos["T"][i, j],
            "costo_tiempo_eur": valor_hora * datos["T"][i, j],
            "peajes_eur": datos["P"][i, j],
            "combustible_eur": datos["combustible"][i, j],
            "costo_total_eur": datos["C"][i, j],
        })
    return pd.DataFrame(filas)
