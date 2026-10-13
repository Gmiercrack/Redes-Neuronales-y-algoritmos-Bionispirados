"""
Exporta las coordenadas (latitud, longitud) de las 47 capitales a coordenadas_capitales.csv.

Qué hace
    Geocodifica cada capital con Nominatim (OpenStreetMap), con el mismo método del notebook
    P_viajero_coordenadas.ipynb: consulta "<ciudad>, España", user_agent "tp-tsp-espana",
    timeout de 10 s y una pausa de 1.1 s entre consultas (la política de uso de Nominatim
    permite como máximo 1 consulta por segundo).

    Los nombres y el orden de las ciudades se toman de matriz_distancias_carretera.csv, para
    que las coordenadas queden alineadas con las matrices de costos.

Para qué sirve
    El archivo coordenadas_capitales.csv lo usa gif_ruta.py para dibujar los recorridos sobre
    el mapa. Se genera UNA sola vez y se sube al repositorio, así el resto del proyecto no
    depende de internet (lo exige el enunciado).

Requisitos
    pip install geopy pandas      (geopy ya está en requirements.txt)
    Conexión a internet. Tarda alrededor de 1 minuto (47 consultas x 1.1 s).

Uso (desde la carpeta Parte_2)
    python exportar_coordenadas.py

Salida
    coordenadas_capitales.csv con columnas: ciudad, lat, lon (grados decimales).

Verificaciones que hace al final
    1. Que todas las coordenadas caigan dentro de la España peninsular.
    2. Que, para cada par de ciudades, la distancia por carretera (OSRM) no sea menor que la
       distancia en línea recta (Haversine). Si lo es, alguna coordenada quedó mal ubicada,
       por ejemplo en el centro de la provincia en vez de en la ciudad.
"""

import os
import sys
import time

import numpy as np
import pandas as pd

DIR_PARTE2 = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DISTANCIAS = os.path.join(DIR_PARTE2, "matriz_distancias_carretera.csv")
ARCHIVO_SALIDA = os.path.join(DIR_PARTE2, "coordenadas_capitales.csv")


def geocodificar(ciudades):
    """Devuelve una lista de (lat, lon) en el mismo orden que `ciudades`."""
    from geopy.geocoders import Nominatim

    geo = Nominatim(user_agent="tp-tsp-espana", timeout=10)
    coords = []
    for k, c in enumerate(ciudades, start=1):
        loc = geo.geocode(f"{c}, España")
        if loc is None:
            sys.exit(f"No se encontraron coordenadas para '{c}'. No se guardó nada.")
        coords.append((loc.latitude, loc.longitude))
        print(f"  {k:2d}/{len(ciudades)}  {c:<22s} {loc.latitude:9.5f} {loc.longitude:9.5f}")
        time.sleep(1.1)
    return np.array(coords)


def haversine_km(coords):
    """Matriz N x N de distancias en línea recta (km) con la fórmula de Haversine."""
    lat, lon = np.radians(coords[:, 0])[:, None], np.radians(coords[:, 1])[:, None]
    a = np.sin((lat - lat.T) / 2) ** 2 + np.cos(lat) * np.cos(lat.T) * np.sin((lon - lon.T) / 2) ** 2
    return 2 * 6371.0 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def verificar(ciudades, coords, D_carretera):
    """Imprime las coordenadas sospechosas. Devuelve True si todo está bien."""
    ok = True

    # 1. Dentro de la península (caja aproximada)
    for c, (lat, lon) in zip(ciudades, coords):
        if not (35.9 <= lat <= 43.9 and -9.5 <= lon <= 3.4):
            print(f"  [REVISAR] {c} quedó fuera de la península: ({lat:.4f}, {lon:.4f})")
            ok = False

    # 2. Carretera >= línea recta
    D_recta = haversine_km(coords)
    n = len(ciudades)
    for i in range(n):
        for j in range(n):
            if i != j and D_carretera[i, j] < D_recta[i, j]:
                print(f"  [REVISAR] {ciudades[i]} -> {ciudades[j]}: carretera {D_carretera[i, j]:.1f} km "
                      f"< línea recta {D_recta[i, j]:.1f} km")
                ok = False
    return ok


def main():
    df = pd.read_csv(ARCHIVO_DISTANCIAS, index_col=0, encoding="utf-8-sig")
    ciudades = [str(c).strip() for c in df.index]
    D_carretera = df.to_numpy(dtype=float)

    print(f"Geocodificando {len(ciudades)} capitales con Nominatim (≈ {1.1 * len(ciudades):.0f} s)...")
    coords = geocodificar(ciudades)

    salida = pd.DataFrame({"ciudad": ciudades, "lat": coords[:, 0], "lon": coords[:, 1]})
    salida.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8-sig")
    print(f"\nGuardado: {ARCHIVO_SALIDA}")
    print(f"Fecha de consulta (para el reporte): {time.strftime('%Y-%m-%d')}")

    print("\nVerificaciones:")
    if verificar(ciudades, coords, D_carretera):
        print("  Todo bien: coordenadas dentro de la península y carretera >= línea recta en todos los pares.")


if __name__ == "__main__":
    main()
