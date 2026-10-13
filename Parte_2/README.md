# Parte 2 — TSP de las 47 capitales de la España peninsular

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (en Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
```

## Algoritmo genético

Un solo comando, desde la carpeta `Parte_2`:

```bash
python algoritmo_genetico.py
```

Toma los parámetros de `config_tsp.json`. Cualquiera se puede cambiar por línea de comandos sin editar el código:

```bash
python algoritmo_genetico.py --generaciones 300 --tam-poblacion 100   # demo rápida (~5 s)
python algoritmo_genetico.py --valor-hora 40                         # otro valor de la hora (€/h)
python algoritmo_genetico.py --tipo-mutacion intercambio --prob-mutacion 0.5
python algoritmo_genetico.py --corridas 30                           # 30 corridas, semillas 1983..2012
python algoritmo_genetico.py --help                                  # lista completa
```

Resultados en `resultados/ga/` (o en la carpeta que se indique con `--salida`). Cada ejecución sobrescribe los archivos de esa carpeta.

| Archivo | Contenido |
|---|---|
| `resumen.json` | configuración usada, mejor costo, estadísticas de las corridas, recorrido |
| `mejor_ruta.csv` | el recorrido tramo a tramo con distancia, tiempo, peajes, combustible y costo |
| `historial.csv` | mejor costo y costo medio por generación, evaluaciones acumuladas |
| `corridas.csv` | una fila por corrida: semilla, costo, evaluaciones, tiempo |
| `rutas_por_generacion.csv` | mejor ruta encontrada hasta cada generación (de la mejor corrida): `generacion`, `costo_eur` y `ruta`, con las ciudades en orden de visita separadas por ` \| `, empezando en `ciudad_inicio` |

Este script solo ejecuta el modelo y guarda los datos. El GIF de la evolución de la ruta sobre el mapa se genera
en un script aparte a partir de `rutas_por_generacion.csv`.

### Modelo de costos (`costos.py`)

$$C_{ij} = v_h\,T_{ij} + P_{ij} + F_{ij}$$

| Símbolo | Significado | Archivo |
|---|---|---|
| $T_{ij}$ | tiempo de viaje (h) | `matriz_tiempos_carretera.csv` |
| $P_{ij}$ | peajes (€) | `matriz_costo_peajes_euros.csv` |
| $F_{ij}$ | combustible (€) | `matriz_costo_combustible_euros.csv` |
| $v_h$ | valor de la hora del vendedor (€/h) | parámetro `--valor-hora` (por defecto 8.90) |

`matriz_distancias_carretera.csv` no entra en el costo (el combustible ya la incluye); se usa para reportar los km.
El valor de la hora no está fijo en ninguna matriz, para poder estudiar cómo cambia la ruta óptima al variarlo.
Con $v_h = 8.90$ €/h la matriz coincide con `matriz_costo_total_euros.csv` (diferencias menores a 0.06 € por redondeo).
Las matrices son asimétricas: el sentido del recorrido importa. `costos.py` se comparte con la colonia de hormigas
para que ambos algoritmos optimicen la misma matriz.

### Pendiente

- `coordenadas_capitales.csv` (columnas `ciudad,lat,lon`, exportadas del notebook), necesario para el script del GIF.

El contorno del mapa (`datos/peninsula_iberica.geojson`) viene de Natural Earth (dominio público), recortado a la península.
