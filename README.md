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
├── Parte_2/                # Parte 2: TSP de las 47 capitales de España peninsular
│   ├── README.md           # Guía completa de ejecución (ACO y Algoritmo Genético)
│   ├── requirements.txt    # Dependencias específicas de Parte 2
│   ├── ANT_ALGORIMT.ipynb  # Optimización por Colonia de Hormigas (ACO)
│   ├── algoritmo_genetico.py # Algoritmo Genético para TSP
│   └── ...
└── Documentación/          # Reporte técnico e informe interactivo
    ├── Implementación web/ # Sitio web tipo blog con la documentación completa
    │   ├── index.html      # Página principal interactiva del informe
    │   └── ...
    ├── Trabajo_1_Optimizacion_Bioinspirada.md
    └── Trabajo_1_Aplicaciones de Optimización...pdf
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

---

## 🌐 Documentación y Reporte Web (Blog del Proyecto)

El reporte integral del trabajo, que consolida la fundamentación teórica, análisis estadísticos, gráficos comparativos, mapas de ruta para el TSP y conclusiones, se encuentra implementado como una **aplicación web estática interactiva tipo blog**.

* **Ubicación en el repositorio:** Directorio [`Documentación/Implementación web/`](Documentación/Implementación%20web/)
* **Documento base e informe PDF:** Disponibles en [`Documentación/`](Documentación/)

### 🚀 Cómo acceder a la página desplegada (GitHub Pages)

El proyecto cuenta con un flujo de integración y despliegue continuo configurado mediante **GitHub Actions** (`.github/workflows/deploy.yml`), el cual publica automáticamente el blog en **GitHub Pages** con cada actualización en la rama principal `main`.

1. **Acceso directo en línea:**  
   👉 **[https://gmiercrack.github.io/Redes-Neuronales-y-algoritmos-Bionispirados/](https://gmiercrack.github.io/Redes-Neuronales-y-algoritmos-Bionispirados/)**

2. **Acceso desde la interfaz del repositorio en GitHub:**
   - **Opción A (Deployments):** En la página de inicio del repositorio en GitHub, dirígete a la columna lateral derecha, en la sección **Environments / Deployments**, y haz clic sobre **`github-pages`**.
   - **Opción B (Actions):** Entra a la pestaña **Actions**, selecciona el workflow **"Deploy Web Application to GitHub Pages"**, pulsa sobre la última ejecución exitosa y encontrarás el enlace en el apartado **deploy**.

### 💻 Cómo visualizar la documentación localmente

Si deseas explorar el blog de forma local sin conexión a internet:
* **Opción rápida:** Navega hasta [`Documentación/Implementación web/index.html`](Documentación/Implementación%20web/index.html) y ábrelo con doble clic en cualquier navegador web moderno (Chrome, Edge, Firefox).
* **Vía servidor local HTTP (recomendada):**
  ```bash
  cd "Documentación/Implementación web"
  python -m http.server 8000
  ```
  Luego abre en tu navegador: [http://localhost:8000](http://localhost:8000)

