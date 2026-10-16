# Uso de la IA y Cacería de Alucinaciones

En el desarrollo de este trabajo se integraron herramientas avanzadas de Inteligencia Artificial Generativa como asistentes de co-programación. Esta sección documenta de forma transparente los prompts clave utilizados, su impacto metodológico y la auditoría técnica que permitió detectar una **alucinación conceptual crítica**.

---

## 1. Principales Prompts Empleados

### 1.1 Implementación del Algoritmo Genético
- **Prompt:** *"Implementa los operadores de un algoritmo genético para el TSP con representación por permutaciones: selección por torneo, cruce de orden y mutación por inversión, y documenta cada operador en el código."*
- **Impacto y Supervisión Humana:** Aceleró la codificación de la estructura base de los operadores en `Parte_2/algoritmo_genetico.py`. La integración de las matrices de costo asimétricas reales, la parametrización del valor horario ($v_h$) y la estricta contabilidad de evaluaciones fueron diseñadas y auditadas íntegramente por el equipo.

### 1.2 Pipeline de Animación Espacial de Rutas
- **Prompt:** *"Guarda la mejor ruta de cada generación para generar después, en un script aparte, un GIF de su evolución sobre el mapa, con el sentido del recorrido y los nombres de las ciudades."*
- **Impacto:** Permitió aislar la lógica computacional pesada del optimizador respecto a la renderización gráfica cartográfica (`gif_ruta.py`), garantizando 100% de reproducibilidad sin tener que reejecutar el algoritmo genético.

---

## 2. Cacería de la Alucinación

### 2.1 La Afirmación Errónea de la IA
En el código autogenerado por el modelo de lenguaje (línea 20 de `Parte_2/algoritmo_genetico.py`), se incluyó el siguiente docstring explicativo:

```python
# Mutación: invierte el segmento r[i..j] (equivale a un movimiento 2-opt)
```

### 2.2 ¿Por qué es una Alucinación Conceptual?
El clásico movimiento **2-opt** (Croes, 1958) desconecta dos aristas y reconecta los extremos invirtiendo el sentido del segmento intermedio. 

En un **TSP Simétrico**, la distancia entre cualesquiera dos nodos es idéntica en ambos sentidos ($C_{uv} = C_{vu}$). En consecuencia, el costo de las aristas internas no sufre alteración alguna y el cambio de costo $\Delta$ se calcula en tiempo $O(1)$ evaluando únicamente los dos enlaces que entran y salen del tramo.

Sin embargo, en nuestro problema la red vial española es un **TSP Asimétrico** ($C_{ij} \neq C_{ji}$, debido a orografía, sentidos viales y bifurcaciones de peaje). Al invertir el orden del segmento, **todas las aristas internas pasan a recorrerse en sentido contrario**, alterando su costo total.

El cambio real de costo viene dado por la relación matemática:

$$\Delta_{\text{real}} = \Delta_{2\text{-opt}} + \sum_{k=i}^{j-1} \left( C_{\pi_{k+1},\pi_k} - C_{\pi_k,\pi_{k+1}} \right)$$

Este segundo sumatorio solo se anula si la matriz de adyacencia es estrictamente simétrica. Por tanto, **en un TSP asimétrico, la mutación por inversión no equivale operativamente a un 2-opt**.

### 2.3 Impacto en los Resultados y Corrección
- **Impacto en el Algoritmo:** Nulo en los resultados numéricos, debido a que el algoritmo genético fue programado para evaluar de forma exhaustiva la función objetivo completa $C_{\text{total}}$ en cada hijo, sin confiar en fórmulas de actualización incremental $O(1)$.
- **Corrección:** Se corrigió la documentación teórica en el informe final y en el código para advertir de este efecto direccional.

!!! note "Lección Metodológica"
    Las propiedades y atajos computacionales demostrados para problemas simétricos no son extrapolables de manera directa a grafos dirigidos o redes asimétricas. Toda asunción teórica introducida por un asistente de IA debe ser sometida a verificación formal de sus hipótesis de partida.
