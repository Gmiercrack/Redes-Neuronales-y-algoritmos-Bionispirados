# Metodología Experimental y Costo Efectivo

Para garantizar una comparación metodológicamente rigurosa e imparcial entre algoritmos con mecánicas operativas completamente dispares (métodos de primer orden basados en derivadas frente a métodos de orden cero basados en poblaciones), se estableció un protocolo formal de comparación justa.

---

## 1. Regla de Comparación Justa

### 1.1 Presupuesto Estricto de Evaluaciones
Todos los algoritmos disponen de un límite máximo de **5000 evaluaciones de la función objetivo $f$**. 
- Para evitar inconsistencias o sobrecostos, todas las llamadas a la función pasan por un interceptor (`Contador`), el cual levanta una excepción al alcanzar el presupuesto exacto.
- Cada mejora de la mejor solución registrada se almacena junto con el conteo exacto acumulado de $n_f$ y $n_{\nabla f}$, permitiendo graficar curvas de convergencia reales y no aproximadas.

### 1.2 Conteo Separado de Operaciones
- **GD Numérico:** Utiliza diferencias hacia adelante, consumiendo $n$ evaluaciones de $f$ por cada gradiente más 1 evaluación de monitoreo por iteración ($n+1$ evaluaciones en total por iteración). Todo se contabiliza en $n_f$ y $n_{\nabla f} = 0$.
- **GD Analítico y Backtracking:** Evalúan $f$ para monitoreo o prueba de Armijo ($n_f$) y evalúan analíticamente $\nabla f$, registrado en $n_{\nabla f}$.
- **Metaheurísticas (Evolutivo, PSO, DE):** Operan sin información de derivadas, de modo que $n_{\nabla f} = 0$ y $n_f \le 5000$.

### 1.3 Métrica de Costo Efectivo Proyectado ($C$)
En muchas comparativas se suele asumir erróneamente que una evaluación de gradiente es "gratuita" frente a una evaluación de función. Para corregir este sesgo analítico, se propone la equivalencia teórica:

$$1\ \text{evaluación de } \nabla f \equiv 2n\ \text{evaluaciones de } f$$

que corresponde al costo computacional mínimo necesario para obtener dicha información direccional mediante diferencias centrales. Así, se define el **Costo Efectivo**:

$$C = n_f + 2n \cdot n_{\nabla f}$$

!!! info "Neutralidad de la métrica"
    Las tablas de resultados se reportan tanto bajo la métrica tradicional a $n_f$ fijo (la más favorable al descenso por gradiente analítico) como bajo la métrica de costo efectivo $C$.

---

## 2. Diseño Experimental

- **Dimensiones:** $n = 2$ y $n = 3$.
- **Funciones:** Rosenbrock y Rastrigin.
- **Corridas:** 30 corridas independientes por configuración con semillas aleatorias $1983 + r$ ($r = 0, \dots, 29$) utilizando `numpy.random.SeedSequence`. En total se ejecutaron $2 \times 6 \times 30 = 360$ corridas por dimensión (720 en total).
- **Umbral de Éxito:** Se considera convergencia exitosa si el mejor valor alcanzado satisface:
  
  $$f_{\text{best}} < 10^{-6}$$
  
  Este umbral es órdenes de magnitud menor que la barrera entre mínimos locales de Rastrigin ($\approx 1$) y exige precisión rigurosa sobre el óptimo global ($f^* = 0$).

---

## 3. Calibración de Hiperparámetros

Para el GD de paso fijo se realizó una búsqueda en rejilla sobre 9 valores de $\eta \in [10^{-5}, 5\times10^{-3}]$ sobre 10 semillas independientes ($7000 + r$) para no sesgar la calibración sobre las corridas de prueba. La Tabla 1 resume la parametrización final de cada algoritmo:

| Método | Hiperparámetros Clave | Criterio de Selección |
|---|---|---|
| **GD Analítico / Numérico** | $\eta = 2\times10^{-4}$ (Rosenbrock); $\eta = 10^{-5}$ (Rastrigin); $h = 10^{-3}$ | Rejilla de estabilidad $\eta < 2/L$ con semillas de validación |
| **GD Backtracking** | $\eta_0 = 1{,}0$, $\beta = 0{,}5$, $c = 10^{-4}$ | Parámetros estándar de la condición de Armijo |
| **Algoritmo Evolutivo** | $N = 50$, Élite = 0.15, Mutación = 0.10, Cruce = 0.75, 100 gen. | Esquema canónico de clase |
| **PSO (PySwarms)** | $N = 50$, $c_1 = 0{,}5$, $c_2 = 0{,}3$, $w = 0{,}9$, 100 it. | Configuración de referencia de clase |
| **Evolución Diferencial** | $N = 50$, $F = 0{,}8$, $CR = 0{,}9$, 100 gen. | Recomendaciones de Storn y Price (1997) |
