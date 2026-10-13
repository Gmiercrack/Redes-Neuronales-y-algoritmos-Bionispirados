"""
Modelo de costos del TSP de las 47 capitales peninsulares.

El costo de ir de la ciudad i a la ciudad j es (enunciado del Trabajo 1):

    C[i, j] = valor_hora * T[i, j]                          (tiempo del vendedor)
            + P[i, j]                                       (peajes)
            + (consumo_l_100km / 100) * precio_litro * D[i, j]   (combustible)

con
    D[i, j] : distancia por carretera en km          (matriz_distancias_carretera.csv)
    T[i, j] : tiempo de viaje en horas               (matriz_tiempos_carretera.csv)
    P[i, j] : costo de peajes en euros               (matriz_peajes.csv)

Las matrices NO tienen que ser simétricas (por carretera, i->j puede diferir de j->i).

Este módulo lo pueden usar tanto el algoritmo genético como la colonia de hormigas,
así ambos optimizan exactamente la misma matriz de costos.
"""

import json
import os
import warnings

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
    if ruta is None:
        return None
    return ruta if os.path.isabs(ruta) else os.path.join(DIR_PARTE2, ruta)


def cargar_config(ruta_config):
    """Lee el archivo JSON de configuración (parámetros del modelo de costos y del algoritmo)."""
    with open(_ruta_absoluta(ruta_config), encoding="utf-8") as f:
        cfg = json.load(f)
    # Las claves que empiezan por "_" son comentarios del archivo, no parámetros.
    return {k: v for k, v in cfg.items() if not k.startswith("_")}


def construir_costos(cfg):
    """Construye la matriz de costos C y sus componentes a partir de la configuración.

    Devuelve un diccionario con:
        nombres     : lista de N ciudades
        C           : matriz de costos total (euros)
        D, T, P     : distancia (km), tiempo (h), peajes (euros)
        combustible : costo de combustible (euros)
        avisos      : lista de textos con los datos que todavía son provisionales
    """
    avisos = []

    # 1) Distancias (obligatorias)
    nombres, D = cargar_matriz(_ruta_absoluta(cfg["archivo_distancias"]))
    n = len(nombres)

    # 2) Tiempos de viaje
    ruta_t = _ruta_absoluta(cfg.get("archivo_tiempos"))
    if ruta_t and os.path.exists(ruta_t):
        nombres_t, T = cargar_matriz(ruta_t)
        if nombres_t != nombres:
            raise ValueError("La matriz de tiempos no tiene las mismas ciudades que la de distancias.")
        if cfg.get("tiempos_en_segundos", False):
            T = T / 3600.0
    else:
        v = float(cfg["velocidad_media_provisional_kmh"])
        T = D / v
        avisos.append(f"TIEMPOS PROVISIONALES: no existe '{cfg.get('archivo_tiempos')}', "
                      f"se usa T = D / {v:g} km/h.")

    # 3) Peajes
    ruta_p = _ruta_absoluta(cfg.get("archivo_peajes"))
    if ruta_p and os.path.exists(ruta_p):
        nombres_p, P = cargar_matriz(ruta_p)
        if nombres_p != nombres:
            raise ValueError("La matriz de peajes no tiene las mismas ciudades que la de distancias.")
    else:
        P = np.zeros((n, n))
        avisos.append(f"PEAJES PROVISIONALES: no existe '{cfg.get('archivo_peajes')}', se usan peajes = 0.")

    # 4) Combustible: litros consumidos en el tramo por el precio del litro
    consumo = float(cfg["consumo_l_100km"])
    precio = float(cfg["precio_litro_eur"])
    combustible = (consumo / 100.0) * precio * D

    # 5) Costo total
    valor_hora = float(cfg["valor_hora_eur"])
    C = valor_hora * T + P + combustible
    np.fill_diagonal(C, 0.0)

    if cfg.get("datos_vehiculo_provisionales", False):
        avisos.append("VEHÍCULO/PRECIO PROVISIONALES: consumo y precio del combustible en la "
                      "configuración son de ejemplo; reemplazarlos por datos con fuente y fecha.")

    return {"nombres": nombres, "C": C, "D": D, "T": T, "P": P,
            "combustible": combustible, "avisos": avisos}


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
