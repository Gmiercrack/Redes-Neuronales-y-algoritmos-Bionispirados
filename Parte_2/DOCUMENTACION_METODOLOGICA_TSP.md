# Documentación Técnica y Metodológica: Modelado de Tiempos de Conducción, Velocidades, Peajes, Combustible y Costos Económicos Totales para el Problema del Agente Viajero (TSP)

**Asignatura:** Redes Neuronales y Algoritmos Bioinspirados  
**Proyecto:** Trabajo 1 - Parte 2: Problema del Agente Viajero (TSP) en las Capitales de España Peninsular  
**Autor:** Gianca  
**Fecha:** Octubre 2026  

---

## Resumen Ejecutivo

El presente documento describe la metodología técnica, formulación física y matemática, modelado estadístico e implementación computacional empleada para la construcción integral de los conjuntos de datos del **Problema del Agente Viajero (TSP - *Traveling Salesperson Problem*)** sobre las 47 capitales de provincia de la España peninsular. 

El análisis se enfoca directamente en la **operación logística y temporal de la red vial de transporte**, prescindiendo del cálculo de distancias teóricas o su optimización aislada para centrarse en los factores reales que determinan el costo y la eficiencia operativa de las rutas comerciales. Se desarrollaron y validaron cinco matrices interurbanas de dimensión $47 \times 47$:
1. **Matriz Temporal de Conducción ($T_{\text{carretera}}$):** Tiempos reales de viaje en horas, calculados con el motor **OSRM (*Open Source Routing Machine*)**, incorporando jerarquía vial, límites legales de velocidad y penalizaciones por maniobras urbanas.
2. **Matriz de Velocidad Media Efectiva ($V_{\text{efectiva}}$):** Caracterización de la velocidad comercial ($D/T$) en km/h a lo largo de las distintas regiones de España.
3. **Matriz de Costo de Combustible ($C_{\text{combustible}}$):** Modelo de consumo energético para el vehículo **Dacia Sandero** (4.7 L / 100 km) con precio de gasolina oficial en España (1.787 €/L), expresado en euros (€).
4. **Matriz Económica de Peajes ($C_{\text{peajes}}$) y Matriz Booleana ($M_{\text{peajes}}$):** Identificación de autopistas de peaje activas en la Red de Carreteras del Estado y estimación estadística del costo monetario en euros mediante un **Intervalo de Confianza al 95%** de tarifa kilométrica.
5. **Matriz de Costo Económico Total del Viajero ($C_{\text{total}}$):** Integración multifactorial del salario del vendedor (8.90 €/h), combustible del vehículo y peajes, expresada en euros (€).

Estos datasets permiten formular tanto el TSP mono-objetivo temporal como variantes **económicas presupuestarias** y **restringidas** (*toll-free routing*) para algoritmos bioinspirados (Algoritmos Genéticos, Colonias de Hormigas [ACO], Optimización por Enjambre de Partículas [PSO]).

---

## Tabla de Contenidos
1. [Definición del Problema e Instancia](#1-definición-del-problema-e-instancia)
2. [Geocodificación y Adquisición de Coordenadas](#2-geocodificación-y-adquisición-de-coordenadas)
3. [Matriz Temporal de Conducción Vial ($T_{\text{carretera}}$)](#3-matriz-temporal-de-conducción-vial-t_textcarretera)
4. [Análisis de Velocidades Medias Efectivas de la Red Vial ($V_{\text{efectiva}}$)](#4-análisis-de-velocidades-medias-efectivas-de-la-red-vial-v_textefectiva)
5. [Modelo de Costo de Combustible (Renault / Dacia Sandero)](#5-modelo-de-costo-de-combustible-renault--dacia-sandero)
6. [Modelado y Estimación de Peajes en España](#6-modelado-y-estimación-de-peajes-en-españa)
7. [Matriz de Costo Económico Total del Viajero ($C_{\text{total}}$)](#7-matriz-de-costo-económico-total-del-viajero-c_texttotal)
8. [Formulación para Algoritmos Bioinspirados](#8-formulación-para-algoritmos-bioinspirados)
9. [Visualización Cartográfica y Análisis de Conectividad](#9-visualización-cartográfica-y-análisis-de-conectividad)
10. [Inventario de Archivos Generados en el Repositorio](#10-inventario-de-archivos-generados-en-el-repositorio)
11. [Diagrama del Flujo Metodológico Integral](#11-diagrama-del-flujo-metodológico-integral)
12. [Referencias Bibliográficas](#12-referencias-bibliográficas)

---

## 1. Definición del Problema e Instancia

El Problema del Agente Viajero es un problema clásico de optimización combinatoria clasificado como **NP-Hard**. Dado un conjunto finito de $N = 47$ nodos (ciudades) $V = \{v_1, v_2, \dots, v_N\}$ y una o varias matrices de costos $C = (c_{ij})_{N \times N}$, el objetivo consiste en hallar una permutación cíclica $\pi = (\pi_1, \pi_2, \dots, \pi_N)$ que minimice la función objetivo de costo total de la ruta:

$$\min f(\pi) = \sum_{k=1}^{N-1} c_{\pi_k, \pi_{k+1}} + c_{\pi_N, \pi_1}$$

### Conjunto de Nodos Seleccionados
Se consideraron las 47 capitales provinciales situadas en la península ibérica (excluyendo los territorios insulares de Baleares y Canarias, y las ciudades autónomas de Ceuta y Melilla, con el fin de preservar la conexidad vial continua):

> *A Coruña, Albacete, Alicante, Almería, Ávila, Badajoz, Barcelona, Bilbao, Burgos, Cáceres, Cádiz, Castellón de la Plana, Ciudad Real, Córdoba, Cuenca, Girona, Granada, Guadalajara, Huelva, Huesca, Jaén, León, Lleida, Logroño, Lugo, Madrid, Málaga, Murcia, Ourense, Oviedo, Palencia, Pamplona, Pontevedra, Salamanca, San Sebastián, Santander, Segovia, Sevilla, Soria, Tarragona, Teruel, Toledo, Valencia, Valladolid, Vitoria-Gasteiz, Zamora, Zaragoza.*

---

## 2. Geocodificación y Adquisición de Coordenadas

Para obtener las coordenadas espaciales $(\text{latitud}_i, \text{longitud}_i)$ de cada capital, se implementó un proceso de geocodificación directa mediante el servicio **Nominatim** provisto por la Fundación **OpenStreetMap (OSM)** a través de la librería Python `geopy`.

### Consideraciones Técnicas y Políticas de Uso
1. **Control de Frecuencia (*Rate Limiting*):** La política de uso aceptable de Nominatim (*Usage Policy*) restringe las peticiones automatizadas a un máximo estricto de **1 petición por segundo**. Por este motivo, se incorporó una pausa obligatoria:
   $$\Delta t = 1.1 \text{ segundos}$$
   entre consultas sucesivas, garantizando la estabilidad del servicio y evitando el bloqueo de la dirección IP cliente.
2. **Tolerancia a Latencia (*Timeout*):** Para mitigar fluctuaciones de red o latencia en el servidor público (que derivan en la excepción `GeocoderTimedOut`), se fijó un umbral de tiempo de espera explícito:
   $$\text{timeout} = 10 \text{ s}$$

Las coordenadas resultantes se expresaron en grados decimales:
$$\text{coords}_i = (\phi_i, \lambda_i) \in [-90^\circ, 90^\circ] \times [-180^\circ, 180^\circ]$$

---

## 3. Matriz Temporal de Conducción Vial ($T_{\text{carretera}}$)

### 3.1. Adquisición de Tiempos de Viaje mediante la API Table de OSRM
Para representar con fidelidad la duración real del desplazamiento vehicular a través de la infraestructura pública de carreteras, se utilizó el motor **OSRM (*Open Source Routing Machine*)**, basado en jerarquías de contracción (*Contraction Hierarchies*) sobre el grafo vial de OpenStreetMap.

Mediante el parámetro `annotations=duration,distance`, se extrajeron los tiempos de trayecto en una sola petición HTTP (registrando simultáneamente la longitud de los corredores para alimentar internamente los cálculos de combustible y peajes):

```http
GET http://router.project-osrm.org/table/v1/driving/{lon1,lat1;lon2,lat2;...}?annotations=duration,distance
```

* **Conversión de Tiempos:** De segundos a horas decimales:
  $$T_{\text{carretera}} = \frac{T_{\text{OSRM}}}{3600.0}$$
* **Configuración de Resiliencia (`timeout=30s`):** Como la consulta evalúa $47 \times 47 = 2.209$ pares de rutas, un timeout preventivo de 30 segundos garantiza que la petición no se cancele por latencia puntual en el servidor público.

### 3.2. Factores Considerados por OSRM para los Tiempos de Viaje
OSRM no realiza un cálculo geométrico simple ni divide distancia entre una velocidad constante arbitraria. Emplea el perfil de automóvil `car.lua` basado en etiquetas viales reales de OpenStreetMap:
1. **Jerarquía vial:** Autopistas/Autovías (`motorway` $\approx 110-120\text{ km/h}$), Carreteras nacionales (`trunk`/`primary` $\approx 90-100\text{ km/h}$), Carreteras secundarias (`secondary` $\approx 70-80\text{ km/h}$), Calles urbanas ($\approx 30-50\text{ km/h}$).
2. **Límites de velocidad explícitos (`maxspeed`):** Señalización específica por tramo vial.
3. **Penalizaciones por giros e intersecciones (*Turn Penalties*):** Penalización de 2 a 5 segundos por giro en cruces, más reducciones de velocidad en rotondas y semáforos.

### 3.3. Justificación Operativa: Primacía del Tiempo sobre la Distancia Física
En logística comercial y distribución real, la distancia física por sí sola carece de relevancia operativa directa frente al tiempo de tránsito:
* Un trayecto por carretera secundaria puede tener menor kilometraje, pero al transitar a $50-60\text{ km/h}$ duplica el tiempo de conducción y el costo de salario del conductor.
* Una autovía puede tener más kilómetros al rodear accidentes orográficos, pero al transitar a $120\text{ km/h}$ reduce notablemente la jornada laboral.
Por tanto, la matriz temporal $T_{\text{carretera}}$ constituye el pilar de la planificación operativa del vendedor viajero.

---

## 4. Análisis de Velocidades Medias Efectivas de la Red Vial ($V_{\text{efectiva}}$)

### 4.1. Relación Física
Relacionando la distancia y el tiempo de viaje entre cada par $(i, j)$ se obtiene la velocidad media efectiva en km/h:
$$V_{\text{efectiva}}(i, j) = \frac{d_{\text{carretera}}(i, j)}{t_{\text{carretera}}(i, j)} \quad (\text{para } i \ne j)$$

### 4.2. Resultados Estadísticos Observados en España
Procesando los 2.162 enlaces interurbanos del país:

| Métrica Estadística | Valor Calculado | Descripción Territorial |
| :--- | :---: | :--- |
| **Velocidad Promedio Global ($\bar{V}$)** | **85.35 km/h** | Velocidad comercial real interprovincial puerta a puerta. |
| **Mediana** | **87.36 km/h** | El 50% de las conexiones superan los 87 km/h. |
| **Desviación Estándar ($\sigma$)** | **6.79 km/h** | Alta homogeneidad de la red de gran capacidad española. |
| **Velocidad Mínima** | **48.23 km/h** | **Teruel $\leftrightarrow$ Guadalajara** (orografía abrupta por carretera convencional). |
| **Velocidad Máxima** | **96.84 km/h** | **San Sebastián $\leftrightarrow$ Girona** (corredor norte 100% autovía continua). |

### 4.3. Fundamento en Ingeniería de Transporte
El promedio nacional de **~85.35 km/h** refleja la realidad de que todo viaje entre capitales incluye tramos urbanos a baja velocidad (30–50 km/h) con semáforos y rotondas al salir y entrar a las ciudades, lo cual reduce la velocidad promedio respecto al límite de crucero de 120 km/h de las autovías.

---

## 5. Modelo de Costo de Combustible (Renault / Dacia Sandero)

### 5.1. Parámetros del Vehículo y Combustible
Para modelar el consumo energético real del agente viajero, se seleccionó uno de los vehículos utilitarios más representativos del mercado español: el **Dacia Sandero** (Grupo Renault):

* **Vehículo:** Dacia Sandero (Motor Gasolina TCe).
* **Consumo Mixto Homologado (WLTP):** $C_{\text{tasa}} = 4.7\text{ L} / 100\text{ km} = 0.047\text{ L/km}$.
* **Precio Medio de Gasolina en España (2026):** $P_{\text{comb}} = 1.787\text{ €/L}$ *(Fuente: Geoportal de Gasolineras del MITECO)*.

### 5.2. Costo Unitario y Matriz de Combustible ($C_{\text{combustible}}$)
El costo unitario de combustible por kilómetro recorrido es:
$$C_{\text{km, comb}} = \left(\frac{4.7\text{ L}}{100\text{ km}}\right) \times 1.787\text{ €/L} = 0.047 \times 1.787 \approx \mathbf{0.08399\text{ €/km}} \quad (\approx 8.4\text{ céntimos de euro/km})$$

La matriz de costo económico de combustible (en euros) entre cada par $(i, j)$ se calcula vectorialmente como:
$$C_{\text{combustible}}(i, j) = d_{\text{carretera}}(i, j) \times C_{\text{km, comb}}$$

* **Diagonal:** $C_{\text{combustible}}(i, i) = 0.0\text{ €}$.
* **Rango:** Desde **~5.29 €** (conexiones cortas como Palencia–Valladolid, 62.9 km) hasta **~101.83 €** (conexiones de extremo a extremo como Girona–Pontevedra, 1.212 km).

---

## 6. Modelado y Estimación de Peajes en España

### 6.1. Contexto Histórico y Normativo de la Red de Peajes
Históricamente, España contaba con un número elevado de autopistas de peaje. Entre **2018 y 2021**, el Gobierno de España aplicó una política de no prórroga de concesiones, liberando autopistas icónicas:
* **Liberadas (Gratuitas):** AP-1 (Burgos–Armiñón), AP-4 (Sevilla–Cádiz), AP-2 (Zaragoza–Mediterráneo) y AP-7 (Tarragona–Alicante y Cataluña).
* **Peajes Activos Relevantes:** Concesiones vigentes a largo plazo como la **AP-66** del Huerna (Asturias–León, hasta 2050), la **AP-68** (Bilbao–Zaragoza, hasta 2026), la **AP-9** (Eje Atlántico Gallego), la **AP-15** (Navarra), la **AP-6/51/61** (Túneles de Guadarrama hacia Segovia y Ávila), la **AP-41** (Madrid–Toledo) y tramos de la **AP-7** en Costa del Sol y Alicante.

### 6.2. Matriz Booleana de Peajes ($M_{\text{peajes}}$)
Se construyó una matriz simétrica binaria $M_{\text{peajes}} \in \{0, 1\}^{47 \times 47}$ donde:
$$M_{\text{peajes}}(i, j) = \begin{cases} 1, & \text{si el corredor principal entre } i \text{ y } j \text{ contiene autopista de peaje} \\ 0, & \text{en caso contrario (autovía gratuita o carretera convencional)} \end{cases}$$

### 6.3. Estimación Estadística de la Tarifa Kilométrica (€/km)
Analizando las tarifas oficiales de las concesionarias (*Abertis, Itínere, Ausol, Aucalsa*) aprobadas por el Ministerio de Transportes para vehículos ligeros (turismos) en una muestra de $n = 11$ corredores activos:

* **Media muestral ($\bar{x}$):** $0.125\text{ €/km}$ (12.5 céntimos de euro por kilómetro).
* **Desviación estándar ($s$):** $0.021\text{ €/km}$.
* **Error estándar ($SE$):** $0.0063\text{ €/km}$.

Aplicando la distribución $t$-Student con $n - 1 = 10$ grados de libertad ($t_{0.025} = 2.228$):
$$\text{IC}_{95\%} = \bar{x} \pm t \cdot \frac{s}{\sqrt{n}} = 0.125 \pm 0.014$$

$$\mathbf{IC}_{95\%} = [\mathbf{0.111\text{ €/km}}, \quad \mathbf{0.139\text{ €/km}}]$$

### 6.4. Matriz Económica de Costo de Peajes ($C_{\text{peajes}}$)
El costo estimado en euros se obtiene mediante el producto matricial de Hadamard:
$$C_{\text{peajes}}(i, j) = M_{\text{peajes}}(i, j) \cdot d_{\text{carretera}}(i, j) \cdot \bar{t}_{\text{km}}$$

### 6.5. Tabla Consolidada de Tramos con Peaje Identificados
Filtrando los pares simétricos ($i < j$), se genera la tabla de referencia para reportes:

| Ciudad Origen | Ciudad Destino | Distancia (km) | Costo Estimado (€) | IC 95% Mín (€) | IC 95% Máx (€) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Cádiz** | **Málaga** | 238.7 | **29.84 €** | 26.50 € | 33.18 € |
| **Pamplona** | **Zaragoza** | 181.7 | **22.71 €** | 20.17 € | 25.26 € |
| **Logroño** | **Zaragoza** | 173.6 | **21.70 €** | 19.27 € | 24.13 € |
| **Guadalajara**| **Madrid** | 143.0 | **17.87 €** | 15.87 € | 19.88 € |
| **A Coruña** | **Pontevedra** | 137.4 | **17.17 €** | 15.25 € | 19.09 € |
| **Bilbao** | **Logroño** | 136.9 | **17.11 €** | 15.20 € | 19.03 € |
| **León** | **Oviedo** | 133.4 | **16.67 €** | 14.81 € | 18.54 € |
| **Madrid** | **Segovia** | 94.4 | **11.80 €** | 10.48 € | 13.12 € |
| **Alicante** | **Murcia** | 89.2 | **11.14 €** | 9.90 € | 12.39 € |
| **Madrid** | **Toledo** | 74.8 | **9.23 €** | 8.30 € | 10.40 € |

---

## 7. Matriz de Costo Económico Total del Viajero ($C_{\text{total}}$)

### 7.1. Formulación Multifactorial del Costo Logístico
Para dotar al problema del agente viajero de un significado económico real y representativo del mundo laboral, se definió el **Costo Total por Trayecto ($C_{\text{total}}$)** como la suma lineal de los tres gastos fundamentales de una empresa de distribución:

$$C_{\text{total}}(i, j) = C_{\text{laboral}}(i, j) + C_{\text{combustible}}(i, j) + C_{\text{peajes}}(i, j)$$

Donde:
1. **Costo Laboral del Vendedor:** Basado en el Salario Mínimo Interprofesional / salario horario bruto de referencia en España ($S_h = 8.90\text{ €/hora}$):
   $$C_{\text{laboral}}(i, j) = t_{\text{carretera}}(i, j) \times 8.90\text{ €/h}$$
2. **Costo de Combustible (Dacia Sandero):**
   $$C_{\text{combustible}}(i, j) = d_{\text{carretera}}(i, j) \times 0.08399\text{ €/km}$$
3. **Costo de Peajes:**
   $$C_{\text{peajes}}(i, j) = \text{Matriz\_costos\_peajes}(i, j)$$
4. **Diagonal:** $C_{\text{total}}(i, i) = 0.0\text{ €}$.

### 7.2. Hallazgos y Desglose Porcentual del Costo en España
Al evaluar los 2.162 pares de ciudades con los datos empíricos de la red española, se obtuvieron las siguientes métricas globales:

| Componente de Costo | Gasto Promedio (€) | Porcentaje del Total | Impacto en la Optimización |
| :--- | :---: | :---: | :--- |
| **Salario del Trabajador** | **55.27 €** | **54.8 %** | **Principal factor de costo.** El tiempo humano pesa más que el kilometraje. |
| **Combustible (Sandero)** | **45.29 €** | **44.9 %** | Costo directo variable proporcional a la distancia. |
| **Peajes de Autopista** | **0.30 €** | **0.3 %** | Costo puntual en corredores específicos de montaña y acceso. |
| **COSTO TOTAL PROMEDIO** | **100.86 €** | **100.0 %** | Gasto promedio interurbano entre dos capitales peninsulares. |

* **Costo Mínimo Interprovincial:** **14.94 €** (Palencia $\leftrightarrow$ Valladolid, 62.9 km, 0.77 h).
* **Costo Máximo Interprovincial:** **220.20 €** (Girona $\leftrightarrow$ Pontevedra, 1.212 km, 12.75 h).

---

## 8. Formulación para Algoritmos Bioinspirados

Con estos datasets, los algoritmos bioinspirados pueden evaluar diversos escenarios de optimización:

### Escenario A: TSP Mono-Objetivo Clásico (Distancia o Tiempo)
Minimizar exclusivamente el kilometraje total o el tiempo de jornada laboral:
$$f_{\text{dist}}(\pi) = \sum_{k=1}^{N} d_{\text{carretera}}(\pi_k, \pi_{k+1}), \qquad f_{\text{tiempo}}(\pi) = \sum_{k=1}^{N} t_{\text{carretera}}(\pi_k, \pi_{k+1})$$

### Escenario B: TSP Presupuestario Integral (Función Objetivo en Euros)
Minimizar el gasto financiero global de la empresa de transporte:
$$f_{\text{económico}}(\pi) = \sum_{k=1}^{N} C_{\text{total}}(\pi_k, \pi_{k+1})$$

```python
# Evaluación ultra-eficiente en NumPy para Algoritmos Genéticos o PSO
C_total = np.load("matriz_costo_total_euros.npy")

def evaluar_fitness_euros(ruta):
    return C_total[ruta[:-1], ruta[1:]].sum() + C_total[ruta[-1], ruta[0]]
```

### Escenario C: TSP Restringido sin Peajes (*Toll-Free TSP*)
Penalización infinita en la función de aptitud (*fitness*) para rutas que incluyan peajes:
$$\text{Fitness}(\pi) = f_{\text{económico}}(\pi) + \infty \cdot \sum_{k=1}^{N} M_{\text{peajes}}(\pi_k, \pi_{k+1})$$

---

## 9. Visualización Cartográfica y Análisis de Conectividad

Se diseñaron dos módulos de visualización gráfica en alta resolución (300 DPI):

1. **Red Vial por Distancia (`red_vial_espana_tsp.png`):** Muestra las 47 capitales con conexiones de líneas discontinuas a sus $k = 4$ vecinos más cercanos por carretera, etiquetando los kilómetros de enlace y coloreando los nodos según la accesibilidad media por distancia (mapa de calor `plasma`).
2. **Red Temporal por Tiempo (`red_tiempos_espana_tsp.png`):** Muestra los enlaces más rápidos en horas de conducción (etiquetas en `h` o `min`), coloreando las ciudades según el tiempo medio de viaje al resto del país (mapa de calor `viridis`).

---

## 10. Inventario de Archivos Generados en el Repositorio

| Archivo | Formato | Descripción |
| :--- | :---: | :--- |
| `matriz_distancias_carretera.csv` | CSV | Matriz de distancias por carretera ($47 \times 47$, km) con nombres. |
| `matriz_tiempos_carretera.csv` | CSV | Matriz de tiempos de conducción ($47 \times 47$, horas) con nombres. |
| `matriz_velocidades_medias_kmh.csv`| CSV | Matriz de velocidades medias efectivas ($47 \times 47$, km/h). |
| `matriz_costo_combustible_euros.csv`| CSV | Matriz de costo de combustible Dacia Sandero ($47 \times 47$, €). |
| `matriz_peajes_espana.csv` | CSV | Matriz booleana de presencia de peajes ($47 \times 47$, binaria 0/1). |
| `matriz_costo_peajes_euros.csv` | CSV | Matriz de costo económico estimado de peajes ($47 \times 47$, €). |
| `matriz_costo_total_euros.csv` | CSV | Matriz de costo total multifactorial (Salario + Combustible + Peajes, €). |
| `matriz_costo_total_euros.npy` | NPY | Formato binario ultrarrápido para optimización bioinspirada ($\mathcal{O}(1)$ I/O). |
| `tabla_reporte_peajes.csv` | CSV | Tabla resumen de tramos de peaje e intervalo de confianza al 95%. |
| `red_vial_espana_tsp.png` | PNG | Mapa de grafo vial de k-vecinos en kilómetros (300 DPI). |
| `red_tiempos_espana_tsp.png` | PNG | Mapa de grafo temporal de k-vecinos en horas (300 DPI). |

---

## 11. Diagrama del Flujo Metodológico Integral

```mermaid
flowchart TD
    A[47 Capitales de España Peninsular] --> B[Nominatim / OpenStreetMap]
    B -->|Control 1.1s + timeout 10s| C[Coordenadas Geográficas: latitud, longitud]
    
    C --> F[API Table OSRM: duration,distance]
    F --> G[Matriz D_carretera 47x47 km]
    F --> H[Matriz T_carretera 47x47 horas]
    
    G & H --> V[Matriz V_efectiva = D / T en km/h]
    
    G --> COMB[Modelo Combustible Dacia Sandero: 4.7 L/100km, 1.787 €/L]
    COMB --> C_COMB[Matriz Costo Combustible 47x47 €]
    
    H --> LAB[Modelo Laboral: 8.90 €/hora]
    LAB --> C_LAB[Matriz Costo Salario Vendedor 47x47 €]
    
    A --> I[Catálogo RCE / MITMS Concesiones]
    I --> J[Matriz Booleana Peajes M_peajes 0/1]
    
    G & J --> K[Modelo Estadístico IC 95%: 0.125 €/km]
    K --> L[Matriz Costo Peajes C_peajes 47x47 €]
    
    C_LAB & C_COMB & L --> C_TOTAL[Matriz Costo Económico Total 47x47 €]
    
    G & H & V & C_COMB & L & C_TOTAL --> M[Exportación CSV y NPY]
    G & H --> N[Visualizaciones Cartográficas PNG 300 DPI]
    
    M --> O[Algoritmos Bioinspirados: AG, ACO, PSO]
```

---

## 12. Referencias Bibliográficas

1. **Applegate, D. L., Bixby, R. E., Chvátal, V., & Cook, W. J. (2006).**  
   *The Traveling Salesman Problem: A Computational Study.* Princeton University Press.
2. **Luxen, D., & Vetter, C. (2011).**  
   *Real-time routing with Open Source Routing Machine.* Proceedings of the 19th ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems (GIS '11), pp. 513–516. DOI: [10.1145/2093973.2094062](https://doi.org/10.1145/2093973.2094062).
3. **Haklay, M., & Weber, P. (2008).**  
   *OpenStreetMap: User-Generated Street Maps.* IEEE Pervasive Computing, 7(4), 12–18. DOI: [10.1109/MPRV.2008.80](https://doi.org/10.1109/MPRV.2008.80).
4. **Ministerio de Transportes y Movilidad Sostenible (MITMS). (2024).**  
   *Catálogo de la Red de Carreteras del Estado: Autopistas en Régimen de Concesión y Actualización de Tarifas.* Gobierno de España. Boletín Oficial del Estado (BOE). Recuperado de: [https://www.transportes.gob.es/](https://www.transportes.gob.es/).
5. **SEOPAN. (2024).**  
   *Informe Anual del Sector de Concesiones de Autopistas de Peaje en España.* Asociación de Empresas Constructoras y Concesionarias de Infraestructuras.
6. **Ministerio para la Transición Ecológica y el Reto Demográfico (MITECO). (2026).**  
   *Geoportal de Gasolineras: Estadísticas y Precios de Carburantes en España.* Gobierno de España. Recuperado de: [https://geoportalgasolineras.es/](https://geoportalgasolineras.es/).
7. **Ministerio de Trabajo y Economía Social. (2024).**  
   *Real Decreto por el que se fija el Salario Mínimo Interprofesional (SMI) en España.* Boletín Oficial del Estado (BOE).
8. **Dacia España - Grupo Renault. (2024).**  
   *Ficha Técnica Oficial y Homologación de Consumo Mixto Dacia Sandero (Protocolo WLTP).* Renault Group.
9. **Walpole, R. E., Myers, R. H., Myers, S. L., & Ye, K. (2012).**  
   *Probability & Statistics for Engineers & Scientists* (9th ed.). Pearson. (Referencia para estimación de Intervalos de Confianza con distribución $t$-Student).
10. **Ballou, R. H., Rahbar, H., & Amini, M. M. (2002).**  
    *Development of actual highway distances from network data.* Transportation Research Part E: Logistics and Transportation Review, 38(4), 267–281.
11. **Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020).**  
    *Array programming with NumPy.* Nature, 585(7825), 357–362. DOI: [10.1038/s41586-020-2649-2](https://doi.org/10.1038/s41586-020-2649-2).
12. **OpenStreetMap Foundation (2024).**  
    *Nominatim Usage Policy (Fair Use).* Recuperado de: [https://operations.osmfoundation.org/policies/nominatim/](https://operations.osmfoundation.org/policies/nominatim/).
13. **Project OSRM (2024).**  
    *OSRM HTTP API Documentation: Table Service.* Recuperado de: [http://project-osrm.org/docs/v5.24.0/api/#table-service](http://project-osrm.org/docs/v5.24.0/api/#table-service).
