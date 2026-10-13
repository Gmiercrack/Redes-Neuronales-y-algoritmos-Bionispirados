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
python algoritmo_genetico.py --valor-hora 40                         # otro valor de la hora
python algoritmo_genetico.py --tipo-mutacion intercambio --prob-mutacion 0.5
python algoritmo_genetico.py --corridas 30                           # 30 corridas, semillas 1983..2012
python algoritmo_genetico.py --sin-graficas                          # sin figuras ni GIF
python algoritmo_genetico.py --help                                  # lista completa
```

Resultados en `resultados/ga/`:

| Archivo | Contenido |
|---|---|
| `resumen.json` | configuración usada, mejor costo, estadísticas de las corridas, recorrido |
| `mejor_ruta.csv` | el recorrido tramo a tramo con distancia, tiempo, peajes, combustible y costo |
| `historial.csv` | mejor costo y costo medio por generación, evaluaciones acumuladas |
| `corridas.csv` | una fila por corrida: semilla, costo, evaluaciones, tiempo |
| `convergencia.png` | curva de convergencia |
| `evolucion_ruta.gif`, `mejor_ruta.png` | la mejor ruta sobre el mapa (requieren `coordenadas_capitales.csv`) |

### Modelo de costos (`costos.py`)

$$C_{ij} = v_h\,T_{ij} + P_{ij} + \frac{c}{100}\,p\,D_{ij}$$

con $v_h$ el valor de la hora (€/h), $T$ el tiempo (h), $P$ los peajes (€), $c$ el consumo (L/100 km),
$p$ el precio del litro (€/L) y $D$ la distancia por carretera (km). La matriz puede ser asimétrica.
`costos.py` se comparte con la colonia de hormigas para que ambos algoritmos optimicen la misma matriz.

### Datos pendientes

Mientras falten, el programa lo avisa al ejecutar y usa valores provisionales:

- `matriz_tiempos_carretera.csv`: tiempos de OSRM (`annotations=duration`). Provisional: $T = D / 90$ km/h.
- `matriz_peajes.csv`: peajes por tramo, con fuente y fecha de consulta. Provisional: 0 €.
- `coordenadas_capitales.csv`: columnas `ciudad,lat,lon`, exportadas del notebook.
- Vehículo y precio del combustible en `config_tsp.json`, con fuente citada.

El contorno del mapa (`datos/peninsula_iberica.geojson`) viene de Natural Earth (dominio público), recortado a la península.
