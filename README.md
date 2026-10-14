# Trabajo 1 — Redes Neuronales y Algoritmos Bioinspirados

**Universidad Nacional de Colombia — Facultad de Minas**  
**Semestre 2026-02**

---

## 📌 Estructura General del Proyecto

Este repositorio contiene el desarrollo del **Trabajo 1**, el cual se encuentra dividido en dos secciones independientes:

> **⚠️ Importante:** Cada parte del proyecto (**Parte 1** y **Parte 2**) cuenta con su propio entorno, su propio archivo de dependencias (**`requirements.txt`**) y su propio archivo de instrucciones detalladas (**`README.md`**).  
> Se recomienda ingresar al directorio correspondiente antes de instalar dependencias o ejecutar experimentos.

```text
Trabajo_1/
├── README.md               # Este archivo (visión general del repositorio)
├── parte1/                 # Parte 1: Optimización numérica y metaheurísticas
│   ├── README.md           # Guía completa de instalación, ejecución y detalles de Parte 1
│   ├── requirements.txt    # Dependencias específicas de Parte 1
│   ├── run.py              # Script principal para reproducir experimentos
│   └── ...
└── Parte_2/                # Parte 2: TSP de las 47 capitales de España peninsular
    ├── README.md           # Guía completa de ejecución (ACO y Algoritmo Genético)
    ├── requirements.txt    # Dependencias específicas de Parte 2
    ├── ANT_ALGORIMT.ipynb  # Optimización por Colonia de Hormigas (ACO)
    ├── algoritmo_genetico.py # Algoritmo Genético para TSP
    └── ...
```

---

## 📂 Módulos del Trabajo

### 1. [Parte 1 — Optimización Numérica: Gradiente vs. Metaheurísticas](parte1/README.md)
* **Directorio:** [`parte1/`](parte1/)
* **Documentación detallada:** [`parte1/README.md`](parte1/README.md)
* **Dependencias:** [`parte1/requirements.txt`](parte1/requirements.txt)
* **Descripción:** Comparación sistemática de algoritmos de optimización sobre las funciones benchmark de **Rosenbrock** y **Rastrigin** (en 2D y 3D) bajo un presupuesto fijo de 5000 evaluaciones de función:
  - Descenso por gradiente (analítico, numérico y con búsqueda lineal / *backtracking*).
  - Algoritmo evolutivo continuo.
  - Optimización por enjambre de partículas (PSO - PySwarms).
  - Evolución Diferencial (DE/rand/1/bin).
* **Guía rápida de inicio:**
  ```bash
  cd parte1
  python -m venv .venv
  # En Windows:
  .venv\Scripts\activate
  # En Linux/Mac:
  # source .venv/bin/activate

  pip install -r requirements.txt
  python run.py
  ```

---

### 2. [Parte 2 — Problema del Vendedor Viajero (TSP) en España Peninsular](Parte_2/README.md)
* **Directorio:** [`Parte_2/`](Parte_2/)
* **Documentación detallada:** [`Parte_2/README.md`](Parte_2/README.md)
* **Dependencias:** [`Parte_2/requirements.txt`](Parte_2/requirements.txt)
* **Descripción:** Solución y análisis del Problema del Agente Viajero (TSP) para las 47 capitales de la España peninsular utilizando un modelo económico real (distancia por carretera, tiempos de viaje, costo de peajes y combustible con valor horario del vendedor $v_h = 8.90$ €/h):
  - **Optimización por Colonia de Hormigas (ACO):** Notebooks interactivos (`P_viajero_coordenadas.ipynb` y `ANT_ALGORIMT.ipynb`).
  - **Algoritmo Genético (GA):** Script de optimización (`algoritmo_genetico.py`) con operadores de orden (OX), mutaciones adaptativas y búsqueda local 2-opt.
* **Guía rápida de inicio:**
  ```bash
  cd Parte_2
  python -m venv .venv
  # En Windows:
  .venv\Scripts\activate
  # En Linux/Mac:
  # source .venv/bin/activate

  pip install -r requirements.txt
  ```
  *(Consultar [`Parte_2/README.md`](Parte_2/README.md) para los pasos específicos de ejecución de los notebooks o scripts).*
