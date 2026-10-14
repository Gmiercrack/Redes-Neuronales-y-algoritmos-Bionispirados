# Parte 2 — TSP de las 47 capitales de la España peninsular

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (en Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
```

## Optimización por Colonia de Hormigas (ACO)

La ejecución del enfoque bioinspirado mediante Colonia de Hormigas se realiza mediante dos notebooks interactivos en Jupyter / VS Code de forma secuencial:

```text
1. P_viajero_coordenadas.ipynb   ➔  (Preprocesamiento, coordenadas y matrices de costo)
2. ANT_ALGORIMT.IPYNB            ➔  (Optimización ACO, hiperparámetros, rutas y GIF)
```

---

### Paso 1: Ejecutar `P_viajero_coordenadas.ipynb`

Este notebook se encarga de la obtención de datos geográficos, el modelado económico del problema y la consolidación de las matrices de viaje para las 47 capitales peninsulares:

* **Geocodificación y coordenadas:** Obtiene las coordenadas geográficas exactas (latitud y longitud) de las 47 capitales provinciales mediante el servicio OpenStreetMap Nominatim.
* **Modelo económico y costos:** Integra las distancias por carretera ($km$), tiempos de conducción ($h$), peajes de autopista (€) y consumo de combustible (€) con el valor horario del vendedor ($v_h = 8.90$ €/h) para calcular la función de costo total asimétrico:
  $$C_{ij} = v_h\,T_{ij} + P_{ij} + F_{ij}$$
* **Visualización cartográfica:** Genera mapas exploratorios de dispersión de las capitales y diagramas de correlación entre distancia, tiempo y costos.

#### Documentos exportados para la ejecución de ACO:
Todos los archivos se exportan organizados en las subcarpetas del proyecto:

| Carpeta | Archivo | Descripción y Uso en ACO |
|---|---|---|
| `Resultados_CSV_ANT/` | `matriz_costo_total_euros.csv` | **Matriz principal (47×47)** de costos totales en euros. Es la matriz de adyacencia de entrada directa para alimentar el optimizador ACO. |
| `Resultados_CSV_ANT/` | `coordenadas_capitales_espana.csv` | Tabla con `ciudad`, `latitud`, `longitud` para el ploteo espacial del itinerario. |
| `Parte_2/` | `coordenadas_capitales.csv` | Tabla con formato estándar (`ciudad, lat, lon`) requerida por `gif_ruta.py` para generar la animación cartográfica. |
| `Resultados_CSV_ANT/` | `matriz_distancias_carretera.csv` | Matriz de distancias en kilómetros (usada para estadísticas de recorrido). |
| `Resultados_CSV_ANT/` | `matriz_tiempos_carretera.csv` | Matriz de tiempos de viaje en horas. |
| `Resultados_CSV_ANT/` | `matriz_costo_combustible_euros.csv` | Matriz de gasto en combustible en euros. |
| `Resultados_CSV_ANT/` | `matriz_costo_peajes_euros.csv` | Matriz de costos de peaje en euros. |
| `Resultados imagenes/` | `distribucion_capitales_espana.png` | Mapa de nodos con la distribución geográfica de las 47 capitales. |

---

### Paso 2: Ejecutar `ANT_ALGORIMT.IPYNB`

Una vez generadas las matrices en `Resultados_CSV_ANT/`, se ejecuta este notebook para resolver el TSP mediante el algoritmo de Colonia de Hormigas:

1. **Carga y validación:** Carga la matriz de costos `matriz_costo_total_euros.csv` e integra la librería `AntColonyOptimizer`.
2. **Sintonización de hiperparámetros:** Realiza corridas y experimentos de sensibilidad comparando tres perfiles:
   * **Caso Base:** Equilibrio entre exploración de feromonas y visibilidad heurística ($\alpha=1.0$, $\beta=2.5$, $\rho=0.10$).
   * **Caso Explorador:** Mayor número de hormigas, evaporación lenta y selección probabilística ($\alpha=1.0$, $\beta=2.0$, $\text{choose\_best}=0.0$).
   * **Caso Voraz:** Fuerte ponderación por el costo inverso del tramo ($\beta=4.5$, $\text{choose\_best}=0.25$).
3. **Análisis de convergencia:** Grafica las curvas comparativas de la evolución del costo mínimo a lo largo de las iteraciones.
4. **Visualización de la ruta óptima:** Traza el mapa completo del recorrido óptimo cerrado sobre España con flechas direccionales, nodo de inicio resaltado y detalle del itinerario paso a paso con costos acumulados.
5. **Generación de la animación y GIF:**
   * Exporta `Resultados_CSV_ANT/rutas_por_generacion_aco.csv` con la mejor ruta en cada iteración.
   * Invoca `gif_ruta.py` para compilar el GIF de la evolución de la colonia (`evolucion_ruta.gif`) y el mapa final (`ruta_final.png`) en `Resultados imagenes/`.

---

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

### Coordenadas geográficas y mapa base

- `coordenadas_capitales.csv` (columnas `ciudad,lat,lon`), exportado automáticamente por `P_viajero_coordenadas.ipynb` (o generado con `exportar_coordenadas.py`), necesario para el script del GIF.
- El contorno del mapa (`datos/peninsula_iberica.geojson`) viene de Natural Earth (dominio público), recortado a la península.

## GIF de la ruta sobre el mapa

Se hace en dos pasos, con dos scripts. Ninguno corre el algoritmo: solo dibujan lo que este guardó.

### Paso 1 (una sola vez): coordenadas de las capitales

```bash
python exportar_coordenadas.py
```

Geocodifica las 47 capitales con Nominatim (OpenStreetMap), con el mismo método del notebook
(consulta `"<ciudad>, España"`, 1.1 s entre consultas). Necesita internet y tarda ≈ 1 minuto.
Guarda `coordenadas_capitales.csv` (columnas `ciudad,lat,lon`) e imprime la fecha de consulta para el reporte.

Al final verifica que todas las coordenadas estén en la península y que, para cada par de ciudades,
la distancia por carretera no sea menor que la distancia en línea recta. Si alguna línea dice `[REVISAR]`,
esa coordenada probablemente quedó mal ubicada (por ejemplo, en el centro de la provincia y no en la ciudad).

Hay que **subir `coordenadas_capitales.csv` al repositorio**, para que el GIF se pueda regenerar sin internet.

### Paso 2: el GIF

Primero se corre el algoritmo (deja `resultados/ga/rutas_por_generacion.csv`) y después:

```bash
python gif_ruta.py
```

Guarda en la misma carpeta de las rutas:

| Archivo | Contenido |
|---|---|
| `evolucion_ruta.gif` | la mejor ruta de cada generación sobre el mapa, desde la población inicial hasta la final |
| `ruta_final.png` | la mejor ruta final |

En ambos, cada ciudad lleva su nombre y cada tramo tiene una flecha que indica el sentido del recorrido
(importa porque las matrices de costos no son simétricas).

Solo se dibujan las generaciones en las que la ruta cambió, como máximo `--max-cuadros` (60 por defecto),
y la ruta final se queda quieta un momento al terminar. Opciones:

```bash
python gif_ruta.py --rutas resultados/ga_vh_40/rutas_por_generacion.csv   # otro experimento
python gif_ruta.py --max-cuadros 40 --fps 4                              # más corto y más lento
python gif_ruta.py --titulo "Colonia de hormigas" --rutas resultados/aco/rutas_por_generacion.csv
python gif_ruta.py --help                                                # todas las opciones
```

La colonia de hormigas puede usar el mismo script si guarda un CSV con las columnas
`generacion`, `costo_eur` y `ruta` (ciudades separadas por ` | `).
