"""
GIF de la evolución de la mejor ruta sobre el mapa de España.

Qué hace
    Lee la mejor ruta encontrada hasta cada generación (o iteración) y la dibuja sobre el
    mapa de la península. Cada cuadro del GIF es un momento de la optimización: se ve cómo
    el recorrido pasa de uno desordenado a uno casi óptimo. Además guarda una imagen PNG
    con la ruta final.

    En el GIF y en el PNG cada ciudad lleva su nombre, y cada tramo de la ruta tiene una
    flecha en la mitad que indica el sentido del recorrido (importa, porque las matrices
    de costos no son simétricas: ir de A a B no cuesta lo mismo que de B a A).

    Este script NO ejecuta ningún algoritmo: solo dibuja. Primero hay que correr el
    algoritmo (por ejemplo algoritmo_genetico.py), que deja el archivo de rutas.

Archivos que necesita
    1. Rutas por generación (lo genera algoritmo_genetico.py)
           resultados/ga/rutas_por_generacion.csv
       Columnas:
           generacion : número de generación (o iteración)
           costo_eur  : costo total de esa ruta
           ruta       : ciudades en orden de visita separadas por " | "
                        (el regreso a la primera ciudad no se escribe; el script lo agrega)
       La colonia de hormigas puede guardar un CSV con estas mismas columnas y usar este
       mismo script (cambiando --titulo).

    2. Coordenadas de las capitales (lo genera exportar_coordenadas.py)
           coordenadas_capitales.csv        columnas: ciudad, lat, lon

    3. Contorno del mapa (ya está en el repositorio)
           datos/peninsula_iberica.geojson  (Natural Earth, dominio público)

Requisitos
    numpy, pandas, matplotlib, Pillow (todos en requirements.txt). No necesita internet.

Uso (desde la carpeta Parte_2)
    python gif_ruta.py
        Usa resultados/ga/rutas_por_generacion.csv y guarda en resultados/ga/:
            evolucion_ruta.gif   la animación
            ruta_final.png       la mejor ruta con los nombres de las ciudades

    Opciones útiles:
    python gif_ruta.py --rutas resultados/ga_vh_40/rutas_por_generacion.csv
        Dibuja otro experimento (el GIF queda en la misma carpeta del CSV).
    python gif_ruta.py --max-cuadros 40 --fps 4
        GIF más corto y más lento.
    python gif_ruta.py --titulo "Colonia de hormigas" --rutas resultados/aco/rutas_por_generacion.csv
        Para otro algoritmo.
    python gif_ruta.py --help
        Lista completa de opciones.

Qué cuadros se dibujan
    La mejor ruta solo cambia en algunas generaciones (en las demás se repite). El script
    toma únicamente las generaciones en las que la ruta cambió, y si son más de
    --max-cuadros elige --max-cuadros de ellas repartidas uniformemente. La primera
    (población inicial) y la última siempre se incluyen. Al final, la ruta definitiva se
    queda quieta unos cuadros (--pausa-final) para que se alcance a ver.
"""

import argparse
import json
import os
import sys

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")   # dibuja sin abrir ventanas (funciona en cualquier computador)
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

DIR_PARTE2 = os.path.dirname(os.path.abspath(__file__))
SEPARADOR = " | "

# Colores
COLOR_ESPANA = "#f3efe4"
COLOR_VECINOS = "#e6e6e6"
COLOR_MAR = "#dbe9f4"
COLOR_BORDE = "#8a8a8a"
COLOR_CIUDAD = "#1f3b73"
COLOR_RUTA = "#d62728"


def ruta_absoluta(ruta):
    """Las rutas relativas se interpretan respecto a la carpeta Parte_2."""
    return ruta if os.path.isabs(ruta) else os.path.join(DIR_PARTE2, ruta)


# ---------------------------------------------------------------------------
# Lectura de datos
# ---------------------------------------------------------------------------

def leer_rutas(archivo):
    """Lee el CSV de rutas. Devuelve (generaciones, costos, rutas como listas de nombres)."""
    df = pd.read_csv(archivo, encoding="utf-8-sig")
    faltan = {"generacion", "costo_eur", "ruta"} - set(df.columns)
    if faltan:
        sys.exit(f"{archivo} no tiene las columnas {sorted(faltan)}.")
    rutas = [[c.strip() for c in r.split(SEPARADOR)] for r in df["ruta"]]
    return df["generacion"].to_numpy(), df["costo_eur"].to_numpy(), rutas


def leer_coordenadas(archivo):
    """Lee coordenadas_capitales.csv y devuelve un diccionario {ciudad: (lat, lon)}."""
    if not os.path.exists(archivo):
        sys.exit(f"No existe {archivo}.\n"
                 f"Genéralo una vez con:  python exportar_coordenadas.py")
    df = pd.read_csv(archivo, encoding="utf-8-sig")
    df.columns = [c.strip().lower() for c in df.columns]
    if not {"ciudad", "lat", "lon"} <= set(df.columns):
        sys.exit(f"{archivo} debe tener las columnas ciudad, lat, lon.")
    return {str(c).strip(): (la, lo) for c, la, lo in zip(df["ciudad"], df["lat"], df["lon"])}


def elegir_cuadros(rutas, max_cuadros):
    """Índices de las filas a dibujar: solo donde la ruta cambia, a lo sumo max_cuadros."""
    cambios = [0] + [k for k in range(1, len(rutas)) if rutas[k] != rutas[k - 1]]
    if cambios[-1] != len(rutas) - 1:
        cambios.append(len(rutas) - 1)        # la última fila siempre entra
    if len(cambios) > max_cuadros:
        pos = np.linspace(0, len(cambios) - 1, max_cuadros).round().astype(int)
        cambios = [cambios[p] for p in np.unique(pos)]
    return cambios


# ---------------------------------------------------------------------------
# Dibujo
# ---------------------------------------------------------------------------

def dibujar_mapa(ax):
    """Dibuja el contorno de la península (España, Portugal y el sur de Francia)."""
    with open(os.path.join(DIR_PARTE2, "datos", "peninsula_iberica.geojson"), encoding="utf-8") as f:
        geo = json.load(f)
    for feat in geo["features"]:
        color = COLOR_ESPANA if feat["properties"]["nombre"] == "Spain" else COLOR_VECINOS
        for poligono in feat["geometry"]["coordinates"]:
            anillo = np.array(poligono[0])           # [longitud, latitud]
            ax.fill(anillo[:, 0], anillo[:, 1], color=color, ec=COLOR_BORDE, lw=0.8, zorder=0)
    ax.set_xlim(-9.8, 4.0)
    ax.set_ylim(35.8, 44.0)
    # Un grado de longitud mide menos que uno de latitud (por cos(latitud)); se corrige
    # la proporción a 40° N, la latitud media de la península, para que no se vea estirado.
    ax.set_aspect(1 / np.cos(np.radians(40)))
    ax.set_facecolor(COLOR_MAR)
    ax.set_xticks([])
    ax.set_yticks([])


def lat_lon_de(ruta, coords):
    """Latitudes y longitudes de la ruta, cerrando el recorrido (vuelve a la primera ciudad)."""
    cerrada = ruta + [ruta[0]]
    lat = [coords[c][0] for c in cerrada]
    lon = [coords[c][1] for c in cerrada]
    return lat, lon


def dibujar_flechas(ax, lat, lon):
    """Dibuja una flecha en la mitad de cada tramo, apuntando en el sentido del recorrido.

    lat y lon describen la ruta cerrada (la última ciudad vuelve a la primera). Cada flecha
    va del 40 % al 60 % del tramo, así la punta queda justo después de la mitad.
    Devuelve la lista de flechas, para poder borrarlas en el siguiente cuadro del GIF.
    """
    flechas = []
    for k in range(len(lat) - 1):
        x0, y0, x1, y1 = lon[k], lat[k], lon[k + 1], lat[k + 1]
        cola = (x0 + 0.40 * (x1 - x0), y0 + 0.40 * (y1 - y0))
        punta = (x0 + 0.60 * (x1 - x0), y0 + 0.60 * (y1 - y0))
        flechas.append(ax.annotate(
            "", xy=punta, xytext=cola, zorder=2,
            arrowprops=dict(arrowstyle="-|>", color=COLOR_RUTA, lw=1.4,
                            mutation_scale=9, shrinkA=0, shrinkB=0)))
    return flechas


def escribir_nombres(ax, coords, tamano):
    """Escribe el nombre de cada ciudad junto a su punto."""
    for c, (lat, lon) in coords.items():
        ax.annotate(c, (lon, lat), fontsize=tamano, xytext=(2, 2),
                    textcoords="offset points", zorder=5)


def hacer_gif(generaciones, costos, rutas, coords, cuadros, archivo_gif, titulo, fps, pausa_final):
    fig, ax = plt.subplots(figsize=(8, 6.6))
    dibujar_mapa(ax)

    # Lo que no cambia entre cuadros: ciudades, sus nombres y la ciudad de inicio
    todas = list(coords)
    ax.scatter([coords[c][1] for c in todas], [coords[c][0] for c in todas],
               s=14, c=COLOR_CIUDAD, zorder=3)
    escribir_nombres(ax, coords, tamano=5.5)
    inicio = rutas[0][0]
    ax.scatter(coords[inicio][1], coords[inicio][0], s=60, c=COLOR_RUTA, zorder=4,
               label=f"Inicio: {inicio}")
    linea, = ax.plot([], [], c=COLOR_RUTA, lw=1.4, zorder=2)
    texto = ax.set_title("")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()

    secuencia = cuadros + [cuadros[-1]] * pausa_final
    flechas = []

    def dibujar(k):
        # Se borran las flechas del cuadro anterior y se dibujan las de la ruta actual
        for f in flechas:
            f.remove()
        flechas.clear()
        lat, lon = lat_lon_de(rutas[k], coords)
        linea.set_data(lon, lat)
        flechas.extend(dibujar_flechas(ax, lat, lon))
        texto.set_text(f"{titulo} — generación {generaciones[k]} — costo {costos[k]:,.0f} €")
        return [linea, texto] + flechas

    anim = FuncAnimation(fig, dibujar, frames=secuencia, blit=False)
    # dpi 130 para que los nombres de las ciudades se lean bien en el GIF
    anim.save(archivo_gif, writer=PillowWriter(fps=fps), dpi=130)
    plt.close(fig)


def hacer_png_final(ruta, costo, coords, archivo_png, titulo):
    fig, ax = plt.subplots(figsize=(8, 6.6))
    dibujar_mapa(ax)
    lat, lon = lat_lon_de(ruta, coords)
    ax.plot(lon, lat, c=COLOR_RUTA, lw=1.4, zorder=2)
    dibujar_flechas(ax, lat, lon)
    ax.scatter(lon[:-1], lat[:-1], s=14, c=COLOR_CIUDAD, zorder=3)
    ax.scatter(lon[0], lat[0], s=60, c=COLOR_RUTA, zorder=4, label=f"Inicio: {ruta[0]}")
    escribir_nombres(ax, {c: coords[c] for c in ruta}, tamano=5.5)
    ax.set_title(f"{titulo} — mejor recorrido — costo {costo:,.0f} €")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(archivo_png, dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def main(argv=None):
    p = argparse.ArgumentParser(
        description="GIF de la evolución de la mejor ruta del TSP sobre el mapa de España.")
    p.add_argument("--rutas", default="resultados/ga/rutas_por_generacion.csv",
                   help="CSV con la mejor ruta por generación (por defecto el del algoritmo genético)")
    p.add_argument("--coordenadas", default="coordenadas_capitales.csv",
                   help="CSV con columnas ciudad, lat, lon")
    p.add_argument("--salida", default=None,
                   help="carpeta donde guardar el GIF y el PNG (por defecto, la carpeta del CSV de rutas)")
    p.add_argument("--titulo", default="Algoritmo genético", help="nombre del algoritmo en el título")
    p.add_argument("--max-cuadros", type=int, default=60, help="máximo de cuadros con rutas distintas")
    p.add_argument("--fps", type=float, default=5, help="cuadros por segundo del GIF")
    p.add_argument("--pausa-final", type=int, default=8,
                   help="cuántos cuadros se repite la ruta final al terminar el GIF")
    args = p.parse_args(argv)

    archivo_rutas = ruta_absoluta(args.rutas)
    if not os.path.exists(archivo_rutas):
        sys.exit(f"No existe {archivo_rutas}.\nPrimero ejecuta el algoritmo, por ejemplo: "
                 f"python algoritmo_genetico.py")
    salida = ruta_absoluta(args.salida) if args.salida else os.path.dirname(archivo_rutas)
    os.makedirs(salida, exist_ok=True)

    generaciones, costos, rutas = leer_rutas(archivo_rutas)
    coords = leer_coordenadas(ruta_absoluta(args.coordenadas))

    sin_coords = sorted({c for r in rutas for c in r} - set(coords))
    if sin_coords:
        sys.exit(f"Estas ciudades de las rutas no están en el archivo de coordenadas: {sin_coords}")

    cuadros = elegir_cuadros(rutas, args.max_cuadros)
    print(f"{len(rutas)} generaciones leídas; se dibujan {len(cuadros)} rutas distintas "
          f"(+{args.pausa_final} cuadros de pausa al final).")

    archivo_gif = os.path.join(salida, "evolucion_ruta.gif")
    archivo_png = os.path.join(salida, "ruta_final.png")
    hacer_gif(generaciones, costos, rutas, coords, cuadros, archivo_gif,
              args.titulo, args.fps, args.pausa_final)
    hacer_png_final(rutas[-1], costos[-1], coords, archivo_png, args.titulo)
    print(f"Guardado: {archivo_gif}")
    print(f"Guardado: {archivo_png}")


if __name__ == "__main__":
    main()
