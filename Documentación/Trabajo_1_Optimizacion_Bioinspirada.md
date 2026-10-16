# Trabajo 1: Optimización numérica, metaheurística y combinatoria

**Integrantes:**
Gian Carlo Mier Estrada
Juan Jose Sanchez Mejia
Nestor Enrique Mendoza Rueda

**Profesor:** Juan David Ospina Arango

**Curso:** Redes Neuronales y algoritmos Bioinspirados — Semestre 2026-2

Facultad de Minas - Universidad Nacional de Colombia, Sede Medellín.
Octubre de 2026

---

## 1.1. Optimización numérica y definición de funciones elegidas para el estudio

Para este trabajo se escogieron las funciones de Rosenbrock y Rastrigin porque son complementarias: la primera tiene un único mínimo pero un valle curvo y mal condicionado que castiga a los métodos de primer orden; la segunda tiene una cantidad exponencial de mínimos locales, lo que castiga a los métodos locales y premia a la exploración poblacional.

Todo lo reportado se obtiene del código del repositorio (<https://github.com/Gmiercrack/Redes-Neuronales-y-algoritmos-Bionispirados>), carpeta `parte1/`, con un único comando (`python run.py`).

## 2. Fundamentación matemática

### 2.1 Funciones de prueba

Sea $x = (x_1,\dots,x_n) \in \mathbb{R}^n$. Ambas funciones están definidas en todo $\mathbb{R}^n$; los intervalos usados abajo son el dominio de inicialización y búsqueda de los experimentos, no el dominio matemático.

**Rosenbrock (Rosenbrock, 1960)**

$$f(x) = \sum_{i=1}^{n-1} \left[ 100\,(x_{i+1} - x_i^2)^2 + (1 - x_i)^2 \right]$$

$$\frac{\partial f}{\partial x_i} = -400\,x_i\,(x_{i+1} - x_i^2) - 2(1 - x_i) \;\;(\text{si } i < n) \;+\; 200\,(x_i - x_{i-1}^2) \;\;(\text{si } i > 1)$$

Dominio de búsqueda: $[-5, 5]^n$. Mínimo global: $x^* = (1,\dots,1)$, $f(x^*) = 0$. Para $n = 2$ y $3$ es el único mínimo en el dominio de búsqueda. En $n = 2$ el Hessiano en $x^*$ es $\begin{pmatrix} 802 & -400 \\ -400 & 200 \end{pmatrix}$, con autovalores $\approx 1001{,}6$ y $\approx 0{,}40$; el número de condición es $\kappa \approx 2{,}5\times10^3$ (calculado numéricamente). Esa disparidad de curvaturas hace que el GD de paso fijo deba usar un paso menor que $2/L \approx 2\times10^{-3}$ y avance muy despacio a lo largo del valle.

**Rastrigin (Rastrigin, 1974; generalización en Mühlenbein et al., 1991)**

$$f(x) = A\,n + \sum_{i=1}^{n} \left[ x_i^2 - A\cos(2\pi x_i) \right], \quad A = 10$$

$$\frac{\partial f}{\partial x_i} = 2x_i + 2\pi A \sin(2\pi x_i)$$

Dominio de búsqueda: $[-5{,}12;\ 5{,}12]^n$. Mínimo global: $x^* = (0,\dots,0)$, $f(x^*) = 0$. Es altamente multimodal: hay un mínimo local cerca de cada punto entero (11 por coordenada en el dominio, es decir, $11^n$: 121 en 2D y 1331 en 3D, conteo aproximado). El Hessiano en el origen es $(2 + 40\pi^2)\,I \approx 397\,I$, así que cada cuenca es estrecha y muy curva ($L \approx 397$, paso estable $\eta < 2/L \approx 5\times10^{-3}$).

### 2.2 Descenso por gradiente

$$x^{(t+1)} = x^{(t)} - \eta\,\nabla f(x^{(t)})$$

Se evalúan tres variantes:

- **(a) GD analítico:** $\nabla f$ con las fórmulas de la sección 2.1 y $\eta$ fijo.
- **(b) GD numérico:** el gradiente se aproxima por diferencias hacia adelante, $\partial f/\partial x_i \approx [f(x + h e_i) - f(x)]/h$ con $h = 10^{-3}$ (error de truncamiento $O(h)$), como en el notebook de clase.
- **(c) GD con backtracking:** se parte de $\eta_0 = 1$ y se reduce $\eta \leftarrow \beta\eta$, con $\beta = 0{,}5$, hasta cumplir la condición de Armijo (Armijo, 1966; Nocedal y Wright, 2006):

$$f(x - \eta g) \le f(x) - c\,\eta\,\|g\|^2, \quad g = \nabla f(x), \; c = 10^{-4}$$

Criterios de parada: $\|x^{(t+1)} - x^{(t)}\| < 10^{-8}$, $\|\nabla f\| < 10^{-12}$, agotamiento del presupuesto o divergencia ($\|x\|_\infty > 10^6$). El punto inicial es aleatorio uniforme en el dominio de búsqueda.

### 2.3 Algoritmo evolutivo (esquema de clase)

Población de $N = 50$ individuos $x \in \mathbb{R}^n$, 100 generaciones. En cada generación la población se ordena por aptitud y la nueva generación se forma con tres grupos: élite (fracción 0,15, copia directa de los mejores), mutación (fracción 0,10) y cruzamiento (fracción 0,75).

- **Mutación gaussiana:** $x'_j = x_j + \sigma_j\,\xi$, $\xi \sim N(0,1)$, $\sigma_j$ = desviación estándar poblacional de la coordenada $j$.
- **Cruzamiento en un punto:** hijo₁ = (padre[1:p], madre[p+1:n]), hijo₂ = (madre[1:p], padre[p+1:n]), $p \in \{1,\dots,n-1\}$.

Los individuos fuera de los límites reciben aptitud $+\infty$ sin gastar evaluación, y la mutación recorta a los límites. Con $N = 50$ y 100 generaciones el consumo es exactamente 5000 evaluaciones.

### 2.4 Optimización por enjambre de partículas (PSO)

Cada partícula $i$ tiene posición $x_i$ y velocidad $v_i$; $b_i$ es su mejor posición personal y $g$ la mejor global (Kennedy y Eberhart, 1995). La actualización estándar con peso de inercia $w$ es:

$$v_i^{(t+1)} = w\,v_i^{(t)} + c_1\,r_1 \odot (b_i - x_i^{(t)}) + c_2\,r_2 \odot (g - x_i^{(t)}), \quad r_1, r_2 \sim U(0,1)^n$$

$$x_i^{(t+1)} = x_i^{(t)} + v_i^{(t+1)}$$

Se usa la implementación `GlobalBestPSO` de PySwarms (Miranda, 2018) con $N = 50$, 100 iteraciones, $c_1 = 0{,}5$, $c_2 = 0{,}3$ y $w = 0{,}9$ (los valores del ejemplo de clase), es decir 5000 evaluaciones.

### 2.5 Evolución diferencial (DE/rand/1/bin)

Para cada individuo $x_i$ se eligen tres índices distintos $r_1, r_2, r_3 \neq i$ (Storn y Price, 1997):

$$v_i = x_{r_1} + F\,(x_{r_2} - x_{r_3})$$

$$u_{i,j} = \begin{cases} v_{i,j} & \text{si } U(0,1) < CR \text{ o } j = j_{rand} \\ x_{i,j} & \text{en otro caso} \end{cases}$$

$$x_i^{(t+1)} = \begin{cases} u_i & \text{si } f(u_i) \le f(x_i) \\ x_i & \text{en otro caso} \end{cases}$$

Parámetros: $N = 50$, $F = 0{,}8$, $CR = 0{,}9$, variante generacional (los candidatos se calculan contra la población actual y se reemplaza al final), con 50 evaluaciones iniciales más 99 generaciones completas de 50, es decir, 5000 evaluaciones.

## 3. Metodología

### 3.1 Regla de comparación justa

**Presupuesto.** Todos los métodos disponen de 5000 evaluaciones de $f$. Toda evaluación pasa por un contador (clase `Contador`) que lanza una excepción al agotar el presupuesto, de modo que ninguna corrida puede excederlo; además registra cada mejora de la mejor solución con el valor exacto de $n_f$ y $n_{\nabla f}$, por lo que las curvas de convergencia no son reconstrucciones aproximadas.

**Conteo separado.** Cada corrida guarda $n_f$ y $n_{\nabla f}$. El GD numérico usa diferencias hacia adelante, que cuestan $n$ evaluaciones de $f$ por gradiente ($f(x)$ se reutiliza), más 1 evaluación de monitoreo por iteración ($n+1$ en total por iteración); estas ya están dentro de $n_f$ y $n_{\nabla f} = 0$. El GD analítico y el backtracking no consumen $f$ para el gradiente, que se cuenta aparte en $n_{\nabla f}$; además evalúan $f$ una vez por iteración (o por intento de línea) y eso sí cuenta en $n_f$. Evolutivo, PSO y DE tienen $n_{\nabla f} = 0$.

**Equivalencia propuesta.** 1 evaluación de $\nabla f \equiv 2n$ evaluaciones de $f$, que es el costo de obtener la misma información por diferencias centrales (el ejemplo del enunciado). Por corrida se define el costo efectivo $C = n_f + 2n \cdot n_{\nabla f}$. Es una equivalencia conservadora con el GD, porque en la práctica un gradiente analítico (o por diferenciación automática) cuesta entre 1 y unas pocas evaluaciones de $f$; por eso las tablas de resultados se comparan además a $n_f$ fijo (la contabilidad más favorable al GD analítico), y se muestra el costo efectivo aparte (Tablas 6 y 7).

### 3.2 Diseño experimental

- Dimensiones 2 y 3; funciones Rosenbrock y Rastrigin; 6 métodos; 30 corridas independientes por configuración ($2 \times 6 \times 30 = 360$ corridas por dimensión, 720 en total).
- **Semillas:** la corrida $r$ ($r = 0,\dots,29$) usa la semilla $1983 + r$. Cada método recibe un flujo aleatorio independiente derivado con `SeedSequence.spawn`; la calibración de $\eta$ usa semillas separadas ($7000 + r$), para no calibrar sobre las mismas condiciones iniciales que se evalúan.
- **Umbral de éxito:** $f_{best} < 10^{-6}$, donde $f_{best}$ es el mejor valor observado durante la corrida. Se justifica porque es varios órdenes menor que la separación típica entre mínimos locales de Rastrigin ($\approx 1$ en $f$) y lo bastante exigente para exigir convergencia real al óptimo global ($f^* = 0$). Se reporta también el intervalo de Wilson al 95 % (Wilson, 1927) en los CSV.
- **Estadísticas:** media, desviación estándar (poblacional, ddof = 0), mejor (mínimo), peor (máximo), mediana y tasa de éxito.
- **Calibración de $\eta$** (solo para el GD de paso fijo): rejilla de 9 valores entre $10^{-5}$ y $5\times10^{-3}$ (rango de estabilidad $\eta < 2/L$), 10 semillas separadas, criterio lexicográfico (fracción de corridas divergidas, mediana de $f_{best}$). Resultado: $\eta = 2\times10^{-4}$ en Rosenbrock y $\eta = 10^{-5}$ en Rastrigin, en 2D y 3D. El backtracking no necesita $\eta$.

**Tabla 1.** *Hiperparámetros de los métodos*

| Método | Parámetros | Origen |
|---|---|---|
| GD (3 variantes) | η calibrado (2×10⁻⁴ Rosenbrock; 10⁻⁵ Rastrigin); backtracking: η₀=1, β=0,5, c=10⁻⁴; h=10⁻³ (numérico) | Calibración con 10 semillas aparte |
| Evolutivo | N=50; élite 0,15; mutación 0,10; cruce 0,75; 100 generaciones | Esquema y fracciones del notebook de clase |
| PSO | N=50; c₁=0,5; c₂=0,3; w=0,9; 100 iteraciones | Ejemplo de clase (PySwarms) |
| DE/rand/1/bin | N=50; F=0,8; CR=0,9 | Valores habituales de Storn y Price (1997) |

*Fuente: elaboración propia a partir de `parte1/README.md` y `experimentos.py` del repositorio.*

La Tabla 1 resume los hiperparámetros de cada método.

### 3.3 Implementación

Python 3.12.3 con numpy 1.26.4, pandas 2.1.4, matplotlib 3.9.4, pyswarms 1.3.0 y Pillow 10.2.0 (versiones fijadas en `requirements.txt`; Harris et al., 2020; Hunter, 2007; Miranda, 2018). Los módulos son `funciones.py` (funciones y gradientes, con verificación del mínimo y del gradiente contra diferencias centrales), `instrumentacion.py` (contador), `descenso_gradiente.py`, `evolutivos.py` (evolutivo y DE), `pso_pyswarms.py`, `experimentos.py` (corridas y tablas), `graficas.py` (figuras y GIFs) y `verificar.py` (consistencia de los artefactos).

## 4. Resultados

### 4.1 Dimensión 2

Las Tablas 2 y 3 resumen el valor final $f_{best}$ de 30 corridas por método en 2D, y la Tabla 6 el costo. Las curvas de la mediana del mejor valor frente a las evaluaciones de $f$ se muestran en las Figuras 1 y 2; la dispersión entre corridas, en las Figuras 3 y 4.

**Tabla 2.** *Rosenbrock 2D: f_best en 30 corridas (5000 evaluaciones de f)*

| Método | Media | Desv. est. | Mejor | Peor | Mediana | Tasa de éxito |
|---|---|---|---|---|---|---|
| GD analítico | 1.225 | 2.156 | 7.93e-04 | 9.136 | 0.109 | 0.0 % (0/30) |
| GD numérico | 1.795 | 2.821 | 6.13e-05 | 10.667 | 0.373 | 0.0 % (0/30) |
| GD backtracking | 0.891 | 2.497 | 4.24e-05 | 13.668 | 0.034 | 0.0 % (0/30) |
| Evolutivo | 0.067 | 0.111 | 3.27e-05 | 0.564 | 0.023 | 0.0 % (0/30) |
| PSO | 3.74e-05 | 6.65e-05 | 6.86e-07 | 3.30e-04 | 1.27e-05 | 3.3 % (1/30) |
| Evol. diferencial | 1.21e-10 | 3.70e-10 | 9.99e-14 | 1.99e-09 | 8.35e-12 | 100.0 % (30/30) |

*Fuente: `parte1/resultados/dim2/tabla_resultados.csv`*

**Tabla 3.** *Rastrigin 2D: f_best en 30 corridas (5000 evaluaciones de f)*

| Método | Media | Desv. est. | Mejor | Peor | Mediana | Tasa de éxito |
|---|---|---|---|---|---|---|
| GD analítico | 19.833 | 12.266 | 0.995 | 49.747 | 17.412 | 0.0 % (0/30) |
| GD numérico | 19.870 | 12.248 | 0.995 | 49.748 | 17.433 | 0.0 % (0/30) |
| GD backtracking | 11.409 | 12.653 | 0 | 49.747 | 6.467 | 10.0 % (3/30) |
| Evolutivo | 0.166 | 0.371 | 5.79e-08 | 0.995 | 3.49e-06 | 33.3 % (10/30) |
| PSO | 2.45e-05 | 4.80e-05 | 6.62e-07 | 2.58e-04 | 8.93e-06 | 6.7 % (2/30) |
| Evol. diferencial | 1.34e-08 | 2.53e-08 | 1.60e-11 | 8.67e-08 | 1.36e-09 | 100.0 % (30/30) |

*Fuente: `parte1/resultados/dim2/tabla_resultados.csv`*

![Figura 1](parte1/resultados/dim2/convergencia_rosenbrock.png)

**Figura 1.** *Convergencia en Rosenbrock 2D: mediana de 30 corridas del mejor valor de f frente a evaluaciones de f (escala log).* Fuente: elaboración propia, `parte1/resultados/dim2/convergencia_rosenbrock.png`.

![Figura 2](parte1/resultados/dim2/convergencia_rastrigin.png)

**Figura 2.** *Convergencia en Rastrigin 2D: mediana de 30 corridas del mejor valor de f frente a evaluaciones de f (escala log).* Fuente: elaboración propia, `parte1/resultados/dim2/convergencia_rastrigin.png`.

![Figura 3](parte1/resultados/dim2/boxplot_rosenbrock.png)

**Figura 3.** *Distribución de f_best por método en Rosenbrock 2D (30 corridas).* Fuente: elaboración propia, `parte1/resultados/dim2/boxplot_rosenbrock.png`.

![Figura 4](parte1/resultados/dim2/boxplot_rastrigin.png)

**Figura 4.** *Distribución de f_best por método en Rastrigin 2D (30 corridas).* Fuente: elaboración propia, `parte1/resultados/dim2/boxplot_rastrigin.png`.

### 4.2 Dimensión 3

Las Tablas 4 y 5 reportan los resultados en 3D; las Figuras 5 a 8 muestran la convergencia y la dispersión.

**Tabla 4.** *Rosenbrock 3D: f_best en 30 corridas (5000 evaluaciones de f)*

| Método | Media | Desv. est. | Mejor | Peor | Mediana | Tasa de éxito |
|---|---|---|---|---|---|---|
| GD analítico | 1.172 | 1.732 | 8.05e-03 | 5.668 | 0.194 | 0.0 % (0/30) |
| GD numérico | 1.817 | 1.765 | 6.19e-03 | 6.171 | 1.044 | 0.0 % (0/30) |
| GD backtracking | 0.655 | 1.614 | 3.41e-03 | 6.787 | 0.047 | 0.0 % (0/30) |
| Evolutivo | 0.791 | 1.191 | 8.33e-04 | 5.620 | 0.519 | 0.0 % (0/30) |
| PSO | 0.067 | 0.079 | 1.10e-04 | 0.282 | 0.034 | 0.0 % (0/30) |
| Evol. diferencial | 3.21e-04 | 5.59e-04 | 8.13e-07 | 2.07e-03 | 7.79e-05 | 3.3 % (1/30) |

*Fuente: `parte1/resultados/dim3/tabla_resultados.csv`*

**Tabla 5.** *Rastrigin 3D: f_best en 30 corridas (5000 evaluaciones de f)*

| Método | Media | Desv. est. | Mejor | Peor | Mediana | Tasa de éxito |
|---|---|---|---|---|---|---|
| GD analítico | 27.726 | 15.184 | 4.975 | 65.667 | 25.869 | 0.0 % (0/30) |
| GD numérico | 28.354 | 15.841 | 4.990 | 65.683 | 25.874 | 0.0 % (0/30) |
| GD backtracking | 18.473 | 13.969 | 0.995 | 65.666 | 15.422 | 0.0 % (0/30) |
| Evolutivo | 0.630 | 0.870 | 1.91e-07 | 2.985 | 4.03e-04 | 20.0 % (6/30) |
| PSO | 0.299 | 0.455 | 3.06e-05 | 1.300 | 8.10e-03 | 0.0 % (0/30) |
| Evol. diferencial | 0.900 | 0.539 | 0.163 | 2.344 | 0.781 | 0.0 % (0/30) |

*Fuente: `parte1/resultados/dim3/tabla_resultados.csv`*

![Figura 5](parte1/resultados/dim3/convergencia_rosenbrock.png)

**Figura 5.** *Convergencia en Rosenbrock 3D: mediana de 30 corridas del mejor valor de f frente a evaluaciones de f (escala log).* Fuente: elaboración propia, `parte1/resultados/dim3/convergencia_rosenbrock.png`.

![Figura 6](parte1/resultados/dim3/convergencia_rastrigin.png)

**Figura 6.** *Convergencia en Rastrigin 3D: mediana de 30 corridas del mejor valor de f frente a evaluaciones de f (escala log).* Fuente: elaboración propia, `parte1/resultados/dim3/convergencia_rastrigin.png`.

![Figura 7](parte1/resultados/dim3/boxplot_rosenbrock.png)

**Figura 7.** *Distribución de f_best por método en Rosenbrock 3D (30 corridas).* Fuente: elaboración propia, `parte1/resultados/dim3/boxplot_rosenbrock.png`.

![Figura 8](parte1/resultados/dim3/boxplot_rastrigin.png)

**Figura 8.** *Distribución de f_best por método en Rastrigin 3D (30 corridas).* Fuente: elaboración propia, `parte1/resultados/dim3/boxplot_rastrigin.png`.

### 4.3 Evaluaciones de f y de ∇f, y costo efectivo

Las Tablas 6 y 7 separan las evaluaciones de $f$ y de $\nabla f$ y calculan el costo efectivo $C = n_f + 2n \cdot n_{\nabla f}$. Por ejemplo, en Rosenbrock 2D el GD analítico agota 5000 evaluaciones de $f$ y 5000 de $\nabla f$, lo que equivale a $C = 5000 + 4 \cdot 5000 = 25\,000$, cinco veces el presupuesto de los demás métodos. Las Figuras 9 a 12 repiten las curvas de convergencia en función de $C$.

**Tabla 6.** *Evaluaciones y costo efectivo en 2D (mediana de 30 corridas)*

| Función | Método | Eval. f (mediana) | Eval. ∇f (mediana) | Costo efectivo (mediana) | Costo efectivo (máx.) |
|---|---|---|---|---|---|
| Rosenbrock | GD analítico | 5000 | 5000 | 25000 | 25000 |
| Rosenbrock | GD numérico | 5000 | 0 | 5000 | 5000 |
| Rosenbrock | GD backtracking | 5000 | 486 | 6946 | 7188 |
| Rosenbrock | Evolutivo | 5000 | 0 | 5000 | 5000 |
| Rosenbrock | PSO | 5000 | 0 | 5000 | 5000 |
| Rosenbrock | Evol. diferencial | 5000 | 0 | 5000 | 5000 |
| Rastrigin | GD analítico | 3178 | 3178 | 15888 | 21516 |
| Rastrigin | GD numérico | 5000 | 0 | 5000 | 5000 |
| Rastrigin | GD backtracking | 276 | 31 | 400 | 523 |
| Rastrigin | Evolutivo | 5000 | 0 | 5000 | 5000 |
| Rastrigin | PSO | 5000 | 0 | 5000 | 5000 |
| Rastrigin | Evol. diferencial | 5000 | 0 | 5000 | 5000 |

*Fuente: `parte1/resultados/dim2/tabla_costo_efectivo.csv`.*

**Tabla 7.** *Evaluaciones y costo efectivo en 3D (mediana de 30 corridas)*

| Función | Método | Eval. f (mediana) | Eval. ∇f (mediana) | Costo efectivo (mediana) | Costo efectivo (máx.) |
|---|---|---|---|---|---|
| Rosenbrock | GD analítico | 5000 | 5000 | 35000 | 35000 |
| Rosenbrock | GD numérico | 5000 | 0 | 5000 | 5000 |
| Rosenbrock | GD backtracking | 5000 | 518 | 8108 | 8240 |
| Rosenbrock | Evolutivo | 5000 | 0 | 5000 | 5000 |
| Rosenbrock | PSO | 5000 | 0 | 5000 | 5000 |
| Rosenbrock | Evol. diferencial | 5000 | 0 | 5000 | 5000 |
| Rastrigin | GD analítico | 3283 | 3282 | 22975 | 30122 |
| Rastrigin | GD numérico | 5000 | 0 | 5000 | 5000 |
| Rastrigin | GD backtracking | 275 | 31 | 461 | 524 |
| Rastrigin | Evolutivo | 5000 | 0 | 5000 | 5000 |
| Rastrigin | PSO | 5000 | 0 | 5000 | 5000 |
| Rastrigin | Evol. diferencial | 5000 | 0 | 5000 | 5000 |

*Fuente: `parte1/resultados/dim3/tabla_costo_efectivo.csv`.*

![Figura 9](parte1/resultados/dim2/costo_efectivo_rosenbrock.png)

**Figura 9.** *Convergencia en Rosenbrock 2D frente al costo efectivo C = n_f + 2n·n_∇f (mediana de 30 corridas).* Fuente: elaboración propia, `parte1/resultados/dim2/costo_efectivo_rosenbrock.png`.

![Figura 10](parte1/resultados/dim2/costo_efectivo_rastrigin.png)

**Figura 10.** *Convergencia en Rastrigin 2D frente al costo efectivo C = n_f + 2n·n_∇f (mediana de 30 corridas).* Fuente: elaboración propia, `parte1/resultados/dim2/costo_efectivo_rastrigin.png`.

![Figura 11](parte1/resultados/dim3/costo_efectivo_rosenbrock.png)

**Figura 11.** *Convergencia en Rosenbrock 3D frente al costo efectivo C = n_f + 2n·n_∇f (mediana de 30 corridas).* Fuente: elaboración propia, `parte1/resultados/dim3/costo_efectivo_rosenbrock.png`.

![Figura 12](parte1/resultados/dim3/costo_efectivo_rastrigin.png)

**Figura 12.** *Convergencia en Rastrigin 3D frente al costo efectivo C = n_f + 2n·n_∇f (mediana de 30 corridas).* Fuente: elaboración propia, `parte1/resultados/dim3/costo_efectivo_rastrigin.png`.

### 4.4 Animaciones

Se generaron dos GIF animados sobre Rastrigin 2D: el del descenso por gradiente (401 cuadros) y el de evolución diferencial (61 cuadros, uno por generación). Las Figuras 13 y 14 muestran cuatro cuadros representativos de cada uno; los GIF completos están en el repositorio (`parte1/resultados/dim2/gif_gd_rastrigin.gif` y `gif_de_rastrigin.gif`) y se regeneran con `python graficas.py 2 3`. El GD de la animación es una corrida ilustrativa (semilla 1990) que no pertenece a las 30 corridas de las estadísticas.

**Figura 13.** *Cuadros 0, 40, 120 y 400 del GIF del descenso por gradiente en Rastrigin 2D: la trayectoria desciende al mínimo local más cercano al punto inicial.* Fuente: `parte1/resultados/dim2/gif_gd_rastrigin.gif` (cuadros extraídos).

**Figura 14.** *Cuadros 0, 8, 25 y 60 del GIF de evolución diferencial en Rastrigin 2D: la población se concentra en torno al mínimo global.* Fuente: `parte1/resultados/dim2/gif_de_rastrigin.gif` (cuadros extraídos).

## 5. Discusión

### 5.1 Qué aportó el descenso por gradiente

**Rapidez cuando la cuenca es favorable.** El GD con backtracking en Rastrigin 2D converge, cuando lo hace, con una mediana de apenas 400 de costo efectivo (Tabla 6) y llega a $f = 0$ exacto en la mejor corrida (Tabla 3), frente a las 5000 evaluaciones de las metaheurísticas. Su tasa de éxito, 10 % (3 de 30), la fija únicamente la cuenca donde cae el punto inicial: el gradiente de Rastrigin es el de un paisaje con muchos mínimos locales y el GD baja al más cercano. Por eso el GD analítico y el numérico, con $\eta$ estable, obtienen 0 % de éxito y valores finales medios de unos 19,8 (2D) y 27,7 a 28,4 (3D), del orden del valor de un mínimo local típico: el resultado depende del punto de partida y no del paso $\eta$.

**Precisión local sin necesidad de población.** En Rosenbrock el GD tiene un único mínimo hacia el que converger, pero el mal condicionamiento ($\kappa \approx 2{,}5\times10^3$ en 2D) obliga a pasos pequeños: con $\eta = 2\times10^{-4}$ el GD analítico no llega al umbral en 5000 iteraciones (mediana 0,109 en 2D y 0,194 en 3D). El backtracking mejora la mediana (0,034 en 2D y 0,047 en 3D) y logra valores mínimos de $4\times10^{-5}$ (2D), pero con un costo efectivo mediano de 6946 en 2D (más que el presupuesto de las metaheurísticas) y sin alcanzar $f < 10^{-6}$. Es decir, el GD aporta una dirección de descenso garantizada y barata de calcular, pero su eficiencia está limitada por la curvatura, y el paso fijo requiere calibración.

**Coste oculto del gradiente.** Con la equivalencia $1\,\nabla f \equiv 2n$ evaluaciones de $f$, el GD analítico cuesta entre 3 y 7 veces el presupuesto de los demás ($C$ mediana de 15 889 y 25 000 en 2D; 22 975 y 35 000 en 3D). Como la contabilidad a $n_f$ fijo es la más favorable al GD, su posición relativa solo puede empeorar bajo cualquier equivalencia de costo positivo; por eso las conclusiones a favor de las metaheurísticas no dependen de la equivalencia elegida. El GD numérico tiene un costo directo en $n_f$ ($n+1$ por iteración), por lo que hace menos iteraciones ($\approx 1667$ en 2D) que el analítico y no mejora su resultado.

### 5.2 Qué aportaron los métodos heurísticos

**Exploración global.** En Rastrigin 2D, DE alcanza el umbral en 30 de 30 corridas (media $1{,}3\times10^{-8}$), el evolutivo en 10 de 30 y PSO en 2 de 30, mientras que ningún GD de paso fijo lo logra. La población y los operadores (diferencia de individuos en DE; mutación y cruzamiento en el evolutivo; memoria personal y global en PSO) permiten saltar entre cuencas, que es justo lo que el gradiente local no puede hacer. En el evolutivo la distribución es bimodal: mediana $3{,}5\times10^{-6}$ pero media 0,166, porque algunas corridas se quedan en el mínimo local de $f \approx 0{,}995$, vecino del global.

**Robustez frente al condicionamiento.** En Rosenbrock 2D, DE llega a una media de $1{,}2\times10^{-10}$ con 100 % de éxito, y PSO a $3{,}7\times10^{-5}$, es decir, unos cuatro (PSO) y diez (DE) órdenes de magnitud mejor que cualquier variante de GD en la media, porque no usan información de curvatura y la búsqueda poblacional recorre el valle. El evolutivo de clase (media 0,067) es notablemente más débil: su mutación gaussiana escala con la dispersión poblacional y el cruce en un punto en 2D es un intercambio de coordenadas, operadores poco eficaces en un valle curvo y estrecho. PSO con los parámetros de clase ($w = 0{,}9$, $c_1 = 0{,}5$, $c_2 = 0{,}3$) converge lento y no pasa el umbral de $10^{-6}$ en casi ninguna corrida (3,3 % en Rosenbrock y 6,7 % en Rastrigin, 2D), aunque su media es pequeña; el umbral de éxito es exigente y por eso la tasa subestima su calidad. El README del repositorio recoge que con $c_1 = c_2 = 1{,}5$ y $w = 0{,}7$ PSO alcanza 100 % de éxito en Rastrigin 2D, lo que muestra que el ranking depende de los hiperparámetros, algo que debe tenerse presente al leer esta comparación.

**Efecto de la dimensión.** Al pasar de 2D a 3D el espacio de búsqueda crece de forma exponencial con presupuesto constante y los resultados cambian: en Rastrigin 3D (1331 mínimos locales aproximadamente) DE se degrada hasta 0 % de éxito con media 0,90 (mejor 0,16), el evolutivo conserva 20 % de éxito (6 de 30) con mediana $4{,}0\times10^{-4}$, y PSO tiene la mejor media entre los heurísticos (0,30) pero 0 % de éxito. En Rosenbrock 3D, DE sigue siendo el mejor (media $3{,}2\times10^{-4}$, 1 éxito de 30), seguido de PSO (0,067); el evolutivo (0,79) queda al nivel de los GD (0,66 a 1,8). Con solo 5000 evaluaciones, ninguno resuelve de forma fiable Rastrigin 3D; DE, que en 2D es el más preciso, converge de forma más homogénea pero más lenta (todas las corridas por debajo de 2,4), lo que sugiere que necesita más generaciones o una población mayor en 3D. Esta conclusión es una hipótesis razonable, pero no se comprobó variando el presupuesto.

### 5.3 Síntesis

La Tabla 8 resume lo aportado por cada familia de métodos.

**Tabla 8.** *Síntesis cualitativa de lo aportado por cada familia de métodos*

| Aspecto | Descenso por gradiente | Metaheurísticas |
|---|---|---|
| Valor final (2D) | Rosenbrock: mediana 0,03 a 0,37; Rastrigin: queda en mínimo local (medias 11 a 20) | DE: 10⁻⁸ a 10⁻¹⁰ (100 % éxito); PSO ≈10⁻⁵; evolutivo 0,07 a 0,17 |
| Valor final (3D) | Rosenbrock: medias 0,66 a 1,8; Rastrigin: 18 a 28 | Rosenbrock: DE 3×10⁻⁴; Rastrigin: medias 0,3 a 0,9 y éxito ≤ 20 % |
| Evaluaciones | Pocas cuando converge (≈400 en Rastrigin con backtracking); costo del gradiente a 2n·n_∇f | Fijo (5000), sin gradiente |
| Geometría que explota | Convexidad local; sufre con mal condicionamiento (Rosenbrock) y con muchos mínimos (Rastrigin) | No usa derivadas; la población explora varias cuencas; costo creciente con la dimensión |
| Sensibilidad | η (calibración) y punto inicial | Hiperparámetros (F, CR, w, c₁, c₂) y tamaño de población |

*Fuente: elaboración propia a partir de las Tablas 2 a 7.*

En conjunto, el gradiente aporta eficiencia y precisión local cuando se parte en la cuenca correcta, y las metaheurísticas aportan exploración global y robustez frente a mínimos locales y a la mala condición, a cambio de un costo fijo en evaluaciones de $f$ que crece con la dimensión. Esto sugiere un enfoque híbrido (exploración poblacional seguida de refinamiento local con gradiente), que no se evaluó en este trabajo.

---

## 6. Optimización combinatoria: El problema del viajero

### 6.1 Formulación del problema del viajero

Un vendedor debe recorrer en carro las $N = 47$ capitales de provincia de la España peninsular y regresar a la ciudad de salida al menor costo posible. Se excluyen Palma, Las Palmas de Gran Canaria y Santa Cruz de Tenerife por ser insulares, y Ceuta y Melilla porque no son accesibles por carretera desde la península. Una solución es una permutación $\pi = (\pi_1, \dots, \pi_N)$ que indica el orden de visita, y se busca la de menor costo total:

$$\min_{\pi} \; f(\pi) = \sum_{k=1}^{N-1} C_{\pi_k,\pi_{k+1}} + C_{\pi_N,\pi_1}$$

El costo de cada tramo combina el valor del tiempo del vendedor, los peajes y el combustible:

$$C_{ij} = v_h\,T_{ij} + P_{ij} + F_{ij}$$

donde $T_{ij}$ es el tiempo de viaje (h), $v_h$ el valor de la hora del vendedor (€/h), $P_{ij}$ el costo de los peajes (€) y $F_{ij}$ el costo del combustible (€). Los datos se describen en la sección 6.2. El valor de la hora se trata como un parámetro y se estudia su efecto sobre la ruta óptima, ya que cambia el peso del tiempo frente al de los peajes y el combustible.

Por carretera, en general $C_{ij} \neq C_{ji}$ (vías de un solo sentido, accesos y peajes distintos), así que el problema es un TSP asimétrico: el sentido del recorrido forma parte de la solución. Además, $f$ no cambia si el mismo ciclo empieza en otra ciudad. Fijando la ciudad de salida, hay $(N-1)! = 46! \approx 5{,}5 \times 10^{57}$ recorridos posibles, lo que hace inviable la enumeración exhaustiva. Como el TSP es NP-difícil (Karp, 1972), se usan dos metaheurísticas bioinspiradas, la colonia de hormigas y los algoritmos genéticos, que no garantizan el óptimo global pero obtienen buenas soluciones con un número controlado de evaluaciones.

### 6.2 Formulación del problema y recolección de datos

**Delimitación del ámbito territorial.** Por definición y restricción inicial del problema, se necesita delimitar el ámbito de estudio a 47 capitales de provincias de la España peninsular. Se excluyeron deliberadamente los territorios insulares (Islas Baleares e Islas Canarias) y las ciudades autónomas del norte de África (Ceuta y Melilla), con el fin de preservar la conexidad física y continua de la red vial terrestre, evitando discontinuidades que requerirían transporte multimodal marítimo o aéreo con estructuras tarifarias ajenas al transporte carretero.

**Geocodificación y adquisición espacial de coordenadas.** La adquisición de las coordenadas geográficas espaciales (latitud y longitud) de las 47 capitales se llevó a cabo mediante el servicio de geocodificación de Nominatim, provisto por la Fundación OpenStreetMap (OSM) e implementado a través de la biblioteca de Python `geopy`. Se implementó una política de uso responsable con control de frecuencia estricto (*rate limiting*) incorporando pausas obligatorias de Δt = 1.1 segundos entre consultas y un tiempo de espera preventivo de timeout = 10 segundos, asegurando la captura sin bloqueos ni distorsiones geográficas. Las coordenadas fueron consolidadas en el archivo `coordenadas_capitales_espana.csv` en grados decimales bajo el sistema elipsoidal WGS84 y se muestran representadas en la Figura 15.

**Figura 15**
*Distribución geográfica espacial de las 47 capitales provinciales de la España peninsular.*

**Adquisición de la matriz temporal de conducción (T_carretera).** En este proyecto se modeló la duración real de conducción vial mediante la API Table del motor de enrutamiento OSRM (Open Source Routing Machine). OSRM utiliza estructuras de aceleración basadas en jerarquías de contracción (*Contraction Hierarchies*) sobre el grafo de carreteras de OpenStreetMap.

La consulta al endpoint `/table/v1/driving/` con anotaciones simultáneas de duración y distancia procesó los 47 × 47 = 2.209 pares interprovinciales. El perfil vehicular de OSRM (`car.lua`) incorpora de manera intrínseca: (a) la jerarquía funcional de la red vial española (autovías y autopistas con velocidades de diseño de 110-120 km/h, carreteras convencionales a 90 km/h y tramos urbanos a 30-50 km/h); (b) límites legales de velocidad por segmento; y (c) penalizaciones por maniobras de giro, rotondas e intersecciones semafóricas (*turn penalties* de 2 a 5 segundos). Los tiempos resultantes fueron convertidos de segundos a horas decimales. A continuación en la Figura 16, se muestra el grafo de las posiciones de las 47 capitales de las provincias conectadas por líneas, formando un grafo cerrado, incluyendo los resultados de tiempos que demora transportarse entre las 4 a 5 ciudades más cercanas.

**Figura 16**
*Grafo de accesibilidad temporal de la red vial española en horas de conducción.*

De la misma forma, se definió el mismo tipo de grafo, pero con las distancias en km entre las 4 a 5 ciudades más cercanas representado en la Figura 17. Es importante aclarar que esta condición solo es para verla reflejada en el gráfico presentados en las Figuras 16 y 17, dado que para el código y la simulación se exportó una matriz simétrica de 47×47, con las distancias y tiempos medios calculados e impartidos por la API previamente mencionada. Estas matrices servirán para la definición del problema de optimización que se pretende resolver.

**Figura 17**
*Grafo de accesibilidad temporal de la red vial española en km entre las capitales de las provincias de España.*

**Análisis de velocidades medias efectivas (V_efectiva).** Relacionando la distancia kilométrica de carretera $d_{carretera}(i,j)$ y la duración temporal $t_{carretera}(i,j)$, se determinó la velocidad media efectiva comercial $V_{efectiva}(i,j) = d_{ij} / t_{ij}$ para los 2.162 trayectos interurbanos del país. El análisis estadístico arrojó una velocidad media global nacional de 85.35 km/h, una mediana de 87.36 km/h y una desviación estándar de 6.79 km/h. La discrepancia entre la media nacional y el límite de crucero de 120 km/h de las autovías radica en el peaje temporal inevitable de penetración urbana (30-50 km/h) al acceder y salir de los núcleos céntricos de cada capital. Estos datos son reportados en la Tabla 9.

**Tabla 9:** *Métricas estadísticas de las velocidades medias efectivas en la red vial española*

| Métrica Estadística | Valor Calculado | Interpretación Logística y Territorial |
|---|---|---|
| Velocidad Promedio Nacional | 85.35 km/h | Velocidad comercial puerta a puerta en desplazamientos interprovinciales. |
| Mediana | 87.36 km/h | El 50% de las conexiones viales del país superan los 87.36 km/h. |
| Desviación Estándar | 6.79 km/h | Refleja una notable homogeneidad y madurez en la red de gran capacidad. |
| Velocidad Mínima | 48.23 km/h | Teruel ↔ Guadalajara (orografía accidentada a través de vías convencionales). |
| Velocidad Máxima | 96.84 km/h | San Sebastián ↔ Girona (corredor continuo 100% autovía/autopista). |

**Modelo de consumo energético y combustible.** La hipótesis anterior se la realizó para poder tomar el dato de los fabricantes en la hoja de especificaciones de automóviles. Generalmente en los catálogos, el dato de consumo de combustible viene dado por L por km recorrido, pero este dato vale para una velocidad que no supere los 100 km/h. Como se evidenció antes en los resultados mostrados en la Tabla 9, el promedio, desviación estándar y mediana colaboran en que, en general, no se supera la velocidad definida para tomar el dato de la eficiencia del consumo de combustible, a pesar de que la normativa española permite hasta 120 km/h como velocidad máxima.

Para modelar el costo de combustible se seleccionó un vehículo utilitario líder en el mercado de distribución español: el Dacia Sandero (Grupo Renault), con motor de gasolina TCe. De acuerdo con la ficha técnica oficial homologada bajo el protocolo WLTP, el consumo mixto es de 4.7 litros por cada 100 kilómetros (0.047 L/km). Considerando la cotización oficial media de la gasolina en las estaciones de servicio de España de 1.787 €/L (reportada por el Geoportal de Gasolineras del MITECO), se deduce el costo unitario de carburante:

$$C_{km,comb} = \left(\frac{4.7\ \text{L}}{100\ \text{km}}\right) \times 1.787\ \text{€/L} \approx 0.083989\ \text{€/km}$$

Por ende, la matriz de costo de combustible $C_{combustible} \in \mathbb{R}^{47 \times 47}$ se define como el producto escalar entre la distancia kilométrica vial y dicho factor unitario:

$$C_{combustible}(i,j) = d_{carretera}(i,j) \times 0.083989\ \text{€}$$

**Modelado estadístico de peajes en España.** El marco normativo de las autopistas en España ha experimentado transformaciones sustanciales entre 2018 y 2021 debido a la finalización de concesiones históricas revertidas al Estado (liberación de la AP-1 Burgos-Armiñón, AP-4 Sevilla-Cádiz, AP-2 Zaragoza-Mediterráneo y tramos centrales de la AP-7). No obstante, persisten concesiones de peaje activo fundamentales en corredores de alta montaña y accesos metropolitanos: la AP-66 del Huerna (León-Oviedo), la AP-68 (Bilbao-Zaragoza), la AP-9 (Eje Atlántico gallego), la AP-15 (Navarra), los túneles de Guadarrama en la AP-6/51/61 (hacia Segovia y Ávila), la AP-41 (Madrid-Toledo) y los tramos privados de la AP-7 en la Costa del Sol y Alicante.

Para incorporar este gasto, se construyó una matriz binaria $M_{peajes} \in \{0,1\}^{47 \times 47}$ que identifica si el corredor directo entre dos capitales involucra una autopista con peaje activo. A partir de una muestra de $n = 11$ corredores representativos autorizados por el Ministerio de Transportes y Movilidad Sostenible (MITMS), consultados y construidos de manera manual, se estimó la tarifa media kilométrica en $\bar{x} = 0.125$ €/km. Este valor es sacado de manera manual tomando los valores depositados de todas las tablas de costos de peaje de las vías, los cuales no están parametrizados, varían entre carreteras, y km recorridos entre carreteras. Esto hace que definir el valor de manera exacta para cada autopista sea un trabajo arduo, por lo cual teniendo en cuenta todos los valores recolectados se estimó un valor "medio" y se asumió que se recorre toda la carretera entre provincias, dado que el problema plantea encontrar la ruta óptima, recorriendo todas las carreteras de España, definidas en el problema.

La matriz económica de costo de peajes se formuló aplicando el producto vectorial de la matriz de 1 y 0, que definen donde existe un peaje, por la cantidad de km que tiene dicha vía, multiplicada por el valor del peaje, previamente definido anteriormente. Esto se representa en la siguiente ecuación y unos resultados de este cálculo se muestran en la Tabla 10.

$$C_{peajes}(i,j) = M_{peajes}(i,j) \cdot d_{carretera}(i,j) \cdot 0.125\ \text{€/km}$$

**Tabla 10:** *Principales corredores viales con peaje activo y estimación monetaria.*

| Corredor Interurbano | Distancia (km) | Costo Estimado (€) |
|---|---:|---:|
| Cádiz ↔ Málaga (AP-7 Costa del Sol) | 238.7 | 29.84 € |
| Pamplona ↔ Zaragoza (AP-15) | 181.7 | 22.71 € |
| Logroño ↔ Zaragoza (AP-68) | 173.6 | 21.70 € |
| A Coruña ↔ Pontevedra (AP-9) | 137.4 | 17.17 € |
| Bilbao ↔ Logroño (AP-68) | 136.9 | 17.11 € |
| León ↔ Oviedo (AP-66 Huerna) | 133.4 | 16.67 € |
| Madrid ↔ Segovia (AP-6 / AP-61) | 94.4 | 11.80 € |

**Matriz de costo económico total del viajero (C_total).** La función de costo objetivo del TSP debe representar la realidad contable de una organización logística. Por ello, el Costo Total del Viajero $C_{total}(i,j)$ se definió como la combinación lineal aditiva de los tres rubros operacionales fundamentales:

$$C_{total}(i,j) = v_h \cdot T_{carretera}(i,j) + C_{combustible}(i,j) + C_{peajes}(i,j)$$

donde $v_h = 8.90$ €/hora corresponde al costo horario del salario bruto del conductor profesional, calculado con base en el Salario Mínimo Interprofesional (SMI) vigente en España más cotizaciones laborales. Al calcular los 2.162 pares de ciudades, se evidenció que el salario del conductor representa el 54.8% del gasto logístico total interurbano (55.27 € de media), el combustible el 44.9% (45.29 € de media) y los peajes el 0.3% distribuido (0.30 € de media), arrojando un costo medio interprovincial de 100.86 €. Esta estructura confirma que en logística contemporánea el factor tiempo humano posee mayor peso financiero que la distancia kilométrica aislada. Esta comparación se la representa de la mejor manera en la Tabla 11.

**Tabla 11:** *Desglose porcentual y valores promedio del costo logístico total en España*

| Componente del Costo | Gasto Medio Interurbano (€) | Participación Porcentual | Impacto en la Optimización |
|---|---:|---:|---|
| Salario del Conductor (8.90 €/h) | 55.27 € | 54.8 % | Factor dominante: prima rutas rápidas sobre cortas. |
| Combustible (Dacia Sandero) | 45.29 € | 44.9 % | Costo directo proporcional al kilometraje. |
| Peajes de Autopista | 0.30 € | 0.3 % | Costo puntual concentrado en pasos de montaña y accesos. |
| **COSTO TOTAL PROMEDIO** | **100.86 €** | **100.0 %** | Costo medio por enlace interprovincial en España. |

### 6.3 Descripción del algoritmo de colonia de hormigas (Ant Colony Optimization)

**Regla de transición y probabilidad de selección.** En la formulación matemática de ACO para el TSP, una población de $m$ hormigas artificiales construye concurrentemente soluciones válidas al problema. En cada paso constructivo, una hormiga $k$ ubicada en la ciudad $i$ decide a qué nodo $j$ desplazarse, dentro del conjunto de ciudades aún no visitadas en su memoria tabú $\mathcal{N}_i^k$, de acuerdo con la regla de transición probabilística (ruleta estocástica):

$$p_{ij}^k = \frac{[\tau_{ij}]^{\alpha} \cdot [\eta_{ij}]^{\beta}}{\sum_{l \in \mathcal{N}_i^k} [\tau_{il}]^{\alpha} \cdot [\eta_{il}]^{\beta}}, \quad \forall j \in \mathcal{N}_i^k \tag{12}$$

Los componentes de la anterior ecuación se definen de la siguiente manera:

1. $\tau_{ij}$ representa la intensidad del rastro de feromona depositado sobre la arista $(i,j)$. Modela la memoria colectiva adaptativa y la experiencia acumulada por las generaciones previas de hormigas.
2. $\eta_{ij}$ denota la información heurística a priori o visibilidad local. En optimización logística económica, se define formalmente como el inverso multiplicativo del costo total en euros entre ambas ciudades: $\eta_{ij} = 1 / C_{total}(i,j)$. Esta formulación otorga preferencia inmediata a los enlaces viales de menor costo económico.
3. $\alpha \ge 0$ es el parámetro de sensibilidad a la feromona. Cuanto mayor sea $\alpha$, mayor será el peso de la historia colectiva, induciendo a la colonia a seguir los caminos ya transitados (alta intensificación). Si $\alpha = 0$, el algoritmo degenera en una búsqueda voraz estocástica basada únicamente en la heurística local.
4. $\beta \ge 1$ es el parámetro de sensibilidad heurística. Controla la voracidad local. Un valor elevado de $\beta$ fuerza a la hormiga a priorizar ciudades cercanas o de bajo costo, mientras que si $\beta = 0$, la colonia seguiría ciegamente por los rastros químicos sin considerar la distancia ni el costo financiero.

**Regla de selección pseudo-aleatoria proporcional.** Para equilibrar de forma determinista la explotación de las mejores aristas y la exploración estocástica del espacio, la variante Ant Colony System (ACS) introduce la regla pseudo-aleatoria proporcional basada en el parámetro `choose_best` ($q_0 \in [0,1]$). En cada decisión, se genera un número aleatorio uniforme $q \sim U(0,1)$:

$$j = \begin{cases} \arg\max_{l \in \mathcal{N}_i^k} \{[\tau_{il}]^{\alpha} \cdot [\eta_{il}]^{\beta}\}, & \text{si } q \le q_0 \\ J \sim p_{ij}^k, & \text{si } q > q_0 \end{cases}$$

**Evaporación y depósito de feromonas.** Una vez que todas las $m$ hormigas han completado su circuito Hamiltoniano cerrado de 47 capitales, se produce la actualización de feromonas. Este proceso consta de dos fases: evaporación y depósito.

La evaporación es un mecanismo indispensable para evitar la saturación prematura y el estancamiento de la colonia en óptimos locales subóptimos, permitiendo el olvido gradual de malas decisiones pasadas:

$$\tau_{ij} \leftarrow (1 - \rho) \cdot \tau_{ij}, \quad \forall (i,j) \in E$$

donde $\rho \in (0,1]$ es la tasa de evaporación de feromonas. Posteriormente, se procede al depósito de feromona sobre los caminos transitados. En la variante elitista global (*Global-Best Update*), se refuerza intensivamente la mejor solución encontrada hasta el momento:

$$\tau_{ij} \leftarrow \tau_{ij} + \frac{Q}{L_{mejor}}, \quad \forall (i,j) \in \pi_{mejor}$$

donde $L_{mejor}$ representa el costo monetario total en euros de la mejor gira descubierta, y $Q$ es una constante positiva de intensificación.

### 6.4 Aplicación del algoritmo de colonia de hormigas

**Arquitectura del pipeline computacional.** La implementación computacional del optimizador bioinspirado se estructuró a través de un pipeline secuencial de dos módulos acoplados en Jupyter Notebooks: `P_viajero_coordenadas.ipynb` y `ANT_ALGORIMT.IPYNB`. El primer notebook procesa las APIs geográficas y genera la matriz de adyacencia de costo económico total $C_{total}$ de 47 × 47 en euros, exportada como `matriz_costo_total_euros.csv` a la carpeta `Resultados_CSV_ANT/`. El segundo notebook ingesta esta matriz directamente en un arreglo de punto flotante de NumPy (`np.ndarray` con 47 nodos) para ser procesado por el algoritmo `AntColonyOptimizer`. Este algoritmo fue tomado de un repositorio abierto de GitHub a cargo de John Berroa, por lo cual, en este trabajo no se codifica dicho algoritmo, sino que se define el problema para usar dicho algoritmo para la simulación y definición de resultados.

**Diseño experimental de sensibilidad (tres escenarios).** Con el objetivo de caracterizar la sensibilidad del algoritmo frente a sus parámetros de control y evitar caer en mínimos locales prematuros, se diseñó un experimento comparativo evaluando tres escenarios con filosofías operacionales contrapuestas sobre la misma instancia de costos:

1. **Escenario Base:** Representa una parametrización equilibrada con 30 hormigas, evaporación moderada del 10% ($\rho = 0.10$), intensificación $Q = 2.0$, ponderación de feromona $\alpha = 1.0$, heurística $\beta = 2.0$ y una baja explotación determinista (`choose_best` = 0.10).
2. **Escenario Voraz:** Diseñado para simular un comportamiento fuertemente codicioso o explotador. Cuenta con solo 20 hormigas, evaporación rápida del 20% ($\rho = 0.20$), intensificación $Q = 3.0$, mayor peso a la memoria histórica $\alpha = 1.5$, un peso heurístico muy agresivo $\beta = 4.5$ y `choose_best` = 0.25 (25% de elecciones deterministas voraces).
3. **Escenario Explorador:** Diseñado para fomentar la diversidad poblacional y la búsqueda global. Emplea un contingente ampliado de 50 hormigas, evaporación suave y lenta del 5% ($\rho = 0.05$), intensificación $Q = 1.5$, $\alpha = 1.0$, $\beta = 2.5$ y `choose_best` = 0.05 (95% de selección estocástica mediante ruleta probabilística). Esto se lo recopila en la Tabla 12.

**Tabla 12:** *Configuración de hiperparámetros para los tres escenarios evaluados de ACO*

| Hiperparámetro / Variable | Caso Base | Caso Voraz | Caso Explorador |
|---|---|---|---|
| Número de Hormigas (m) | 30 | 20 | 50 |
| Tasa de Evaporación (ρ) | 0.10 (10%) | 0.20 (20%, rápida) | 0.05 (5%, lenta) |
| Constante de Intensificación (Q) | 2.0 | 3.0 | 1.5 |
| Sensibilidad a la Feromona (α) | 1.0 | 1.5 | 1.0 |
| Sensibilidad Heurística (β) | 2.0 (equilibrado) | 4.5 (muy voraz) | 2.5 (moderado) |
| Selección Voraz (choose_best) | 0.10 (10% voraz) | 0.25 (25% voraz) | 0.05 (95% estocástico) |
| Límite de Iteraciones | 200 | 200 | 200 |

**Control de ejecución y parada temprana.** Para optimizar la eficiencia computacional y evitar el consumo redundante de ciclos de CPU, el optimizador incorpora un criterio de parada temprana (*early stopping*). Si transcurren 20 iteraciones consecutivas sin que se produzca una mejora estricta en el mejor costo global de la colonia, la ejecución se interrumpe automáticamente y se retorna la mejor solución alcanzada.

**Trazabilidad y registro histórico generacional.** Adicionalmente, se implementó la clase extendida `AntColonyOptimizerConHistorial`, la cual intercepta cada iteración del bucle evolutivo para registrar la mejor permutación de ciudades y su costo. Estos estados intermedios fueron exportados al archivo `rutas_por_generacion_aco.csv` en la carpeta `Resultados_CSV_ANT/`, sirviendo como insumo indispensable para la renderización de la animación generacional del mapa vial español.

### 6.5 Resultados de la colonia de hormigas

**Análisis comparativo de desempeño y convergencia.** La ejecución de los tres perfiles experimentales demostró marcadas diferencias en la velocidad de convergencia, la calidad de la solución final y la susceptibilidad al estancamiento prematuro, tal como se sintetiza en la Tabla 13 y se muestra en la Figura 18.

**Tabla 13:** *Comparación de resultados y desempeño entre los tres escenarios evaluados de ACO*

| Métrica de Desempeño | Caso Base | Caso Voraz | Caso Explorador (Óptimo) |
|---|---|---|---|
| Mejor Costo Económico Total | 1,474.63 € | 1,489.88 € | 1,421.54 € |
| Diferencia respecto al Óptimo | + 53.09 € (+ 3.73%) | + 68.34 € (+ 4.81%) | 0.00 € (Mínimo Global) |
| Tiempo de Ejecución | 4.7 s | 6.3 s | 18.1 s |
| Condición de Parada | Parada temprana (20 it. estancado) | 200 iteraciones completas | 200 iteraciones completas |
| Diagnóstico de Comportamiento | Convergencia equilibrada pero atrapado en óptimo local. | Caída rápida inicial; atrapado por miopía heurística. | Búsqueda exhaustiva sostenida; desenredo completo de la red. |

**Figura 18**
*Curvas comparativas de convergencia del costo total (€) a lo largo de 200 iteraciones para los tres escenarios de ACO.*

**Discusión del comportamiento algorítmico.** La inspección de la Figura 3 [*sic*; corresponde a la Figura 18] revela claramente la dinámica de optimización bioinspirada. El Escenario Voraz (línea roja), impulsado por su alto parámetro heurístico $\beta = 4.5$ y `choose_best` = 0.25, experimenta una caída dramática durante los primeros 5 ciclos, alcanzando rápidamente la región de los 1.520 €. No obstante, esa misma voracidad provoca una 'miopía' algorítmica: las hormigas eligen aristas individualmente muy baratas en el corto plazo, lo que inevitablemente las fuerza a cerrar el recorrido mediante saltos transversales extensos y costosos hacia ciudades aisladas, quedando atrapadas en una solución subóptima con múltiples cruces espaciales (1.489,88 €).

Por el contrario, el Escenario Explorador (línea verde) combina un mayor contingente de hormigas ($m = 50$), una evaporación lenta ($\rho = 0.05$) que conserva memoria sin borrar prematuramente caminos prometedores, y una regla de selección primordialmente probabilística (`choose_best` = 0.05). Esta configuración otorga la flexibilidad estocástica necesaria para superar las barreras de potencial de los óptimos locales, logrando descensos sucesivos y alcanzando el mínimo económico absoluto de 1.421,54 € (una economía de 68,34 € frente al caso voraz y 53,09 € frente al caso base).

**Auditoría financiera del itinerario óptimo (Escenario Explorador).** Habiendo determinado la superioridad concluyente del Escenario Explorador, se procedió a la auditoría pormenorizada de su itinerario de viaje. En la Tabla 14 se desglosan los 47 tramos del circuito cerrado resultante, extraído directamente de `itinerario_explorador.csv`, indicando el par origen-destino, el costo específico del tramo y el costo acumulado de la gira comercial.

**Tabla 14:** *Itinerario detallado tramo a tramo del circuito óptimo obtenido por el Escenario Explorador (Costo Total: 1.421,54 €)*

| Paso | Ciudad Origen | Ciudad Destino | Costo Tramo (€) | Costo Acumulado (€) |
|---:|---|---|---:|---:|
| 1 | Madrid | Toledo | 24.74 € | 24.74 € |
| 2 | Toledo | Ciudad Real | 26.93 € | 51.67 € |
| 3 | Ciudad Real | Albacete | 39.50 € | 91.17 € |
| 4 | Albacete | Cuenca | 32.07 € | 123.24 € |
| 5 | Cuenca | Guadalajara | 32.28 € | 155.52 € |
| 6 | Guadalajara | Soria | 34.26 € | 189.78 € |
| 7 | Soria | Logroño | 29.84 € | 219.62 € |
| 8 | Logroño | Vitoria-Gasteiz | 23.19 € | 242.81 € |
| 9 | Vitoria-Gasteiz | Pamplona | 18.53 € | 261.34 € |
| 10 | Pamplona | San Sebastián | 16.66 € | 278.00 € |
| 11 | San Sebastián | Bilbao | 19.95 € | 297.95 € |
| 12 | Bilbao | Santander | 19.98 € | 317.93 € |
| 13 | Santander | Oviedo | 36.80 € | 354.73 € |
| 14 | Oviedo | A Coruña | 51.68 € | 406.41 € |
| 15 | A Coruña | Lugo | 19.76 € | 426.17 € |
| 16 | Lugo | Pontevedra | 32.58 € | 458.75 € |
| 17 | Pontevedra | Ourense | 33.86 € | 492.61 € |
| 18 | Ourense | Zamora | 52.12 € | 544.73 € |
| 19 | Zamora | León | 38.58 € | 583.31 € |
| 20 | León | Palencia | 35.33 € | 618.64 € |
| 21 | Palencia | Burgos | 17.57 € | 636.21 € |
| 22 | Burgos | Valladolid | 24.18 € | 660.39 € |
| 23 | Valladolid | Segovia | 21.68 € | 682.07 € |
| 24 | Segovia | Ávila | 23.22 € | 705.29 € |
| 25 | Ávila | Salamanca | 21.58 € | 726.87 € |
| 26 | Salamanca | Cáceres | 37.87 € | 764.74 € |
| 27 | Cáceres | Badajoz | 19.91 € | 784.65 € |
| 28 | Badajoz | Sevilla | 40.67 € | 825.32 € |
| 29 | Sevilla | Huelva | 17.34 € | 842.66 € |
| 30 | Huelva | Cádiz | 39.40 € | 882.06 € |
| 31 | Cádiz | Córdoba | 47.64 € | 929.70 € |
| 32 | Córdoba | Jaén | 22.96 € | 952.66 € |
| 33 | Jaén | Granada | 17.80 € | 970.46 € |
| 34 | Granada | Málaga | 26.80 € | 997.26 € |
| 35 | Málaga | Almería | 42.55 € | 1039.81 € |
| 36 | Almería | Murcia | 38.24 € | 1078.05 € |
| 37 | Murcia | Alicante | 28.89 € | 1106.94 € |
| 38 | Alicante | Valencia | 32.84 € | 1139.78 € |
| 39 | Valencia | Castellón de la Plana | 15.44 € | 1155.22 € |
| 40 | Castellón de la Plana | Tarragona | 34.84 € | 1190.06 € |
| 41 | Tarragona | Barcelona | 19.78 € | 1209.84 € |
| 42 | Barcelona | Girona | 20.05 € | 1229.89 € |
| 43 | Girona | Lleida | 42.29 € | 1272.18 € |
| 44 | Lleida | Huesca | 18.57 € | 1290.75 € |
| 45 | Huesca | Zaragoza | 23.12 € | 1313.87 € |
| 46 | Zaragoza | Teruel | 41.18 € | 1355.05 € |
| 47 | Teruel | Madrid | 66.49 € | 1421.54 € |

**Análisis topológico y cartográfico de la solución.** El análisis topológico del itinerario de la Tabla 14 evidencia una coherencia geográfica excepcional. Partiendo desde el nodo central de Madrid hacia Toledo y Ciudad Real, la colonia de hormigas traza una trayectoria periférica continua y elegante que rodea secuencialmente la península ibérica sin retrocesos ni auto-intersecciones. El grafo que representa el orden de recorrido se muestra en la Figura 19.

**Figura 19**
*Cartografía de la ruta óptima cerrada del agente viajero (Escenario Explorador, 1.421,54 €).*

La orientación vectorial de los tramos (representada por flechas direccionales en la Figura 19) es un resultado de vital importancia debido a la asimetría de la matriz de costos. Asimismo, los costos por tramo reflejan fielmente las condiciones de infraestructura: los tramos más económicos corresponden a capitales vecinas conectadas por autovías llanas de alta capacidad (ej. Valencia a Castellón de la Plana: 15.44 €, Pamplona a San Sebastián: 16.66 €, Sevilla a Huelva: 17.34 €), mientras que los segmentos más costosos corresponden a transiciones orográficas complejas o enlaces de largo alcance entre cuadrantes (ej. Teruel a Madrid: 66.49 €, Ourense a Zamora: 52.12 €, Oviedo a A Coruña: 51.68 €). Para tener un punto de comparación en la Figura 20 se muestra el recorrido obtenido por el Escenario Voraz.

**Figura 20**
*Cartografía del circuito obtenido por el Escenario Voraz (1.489,88 €).*

**Artefactos dinámicos y animaciones generacionales (GIF).** Para documentar visualmente la dinámica de aprendizaje adaptativo de la colonia, se implementaron dos productos dinámicos exportados a la carpeta `Resultados_imagenes_ANT_OPT/`: (a) `recorrido_optimo_explorador.gif`, el cual reproduce la trayectoria paso a paso de un móvil sobre las 47 capitales con actualización simultánea de costo acumulado (€) y porcentaje de avance; y (b) `evolucion_ruta.gif`, compilado mediante el script `gif_ruta.py` sobre la cartografía vectorial de la península ibérica (`peninsula_iberica.geojson`), el cual ilustra de manera contundente cómo la población de hormigas, inicialmente desorganizada y con múltiples aristas entrecruzadas en las primeras generaciones, va 'desenredando' el grafo iteración tras iteración hasta converger en el circuito cerrado limpio y óptimo de 1.421,54 €.

### 6.6 Descripción de los algoritmos genéticos usados

Se implementó un algoritmo genético (AG) generacional con representación por permutaciones (Goldberg, 1989), selección por torneo, cruce de orden y mutación por inversión. El código está en `Parte_2/algoritmo_genetico.py`. La matriz de costos definida en la sección 6.1 se construye en `Parte_2/costos.py`, un módulo compartido con la colonia de hormigas para que ambos algoritmos optimicen la misma función.

#### 6.6.1 Representación y función objetivo

Cada individuo es una permutación $\pi = (\pi_1, \pi_2, \dots, \pi_N)$ de las $N = 47$ capitales, que representa el orden de visita. Esta representación garantiza que cada ciudad se visite exactamente una vez sin restricciones adicionales. El recorrido es cerrado: después de $\pi_N$ se regresa a $\pi_1$. El algoritmo genético (o evolutivo) minimiza el costo total del ciclo:

$$f(\pi) = \sum_{k=1}^{N} C(\pi_k, \pi_{k+1}), \quad \text{con } \pi_{N+1} = \pi_1$$

donde $C$ es la matriz de costo generalizado definida en la sección 6.1.

#### 6.6.2 Población inicial y selección

La población inicial está formada por $M = 200$ permutaciones aleatorias uniformes. Cada padre se elige por torneo: se toman $k = 3$ individuos al azar, con reemplazo, y gana el de menor costo (Miller y Goldberg, 1995). Si $r$ es el puesto de un individuo al ordenar la población por costo ($r = 1$ el mejor), su probabilidad de ganar es:

$$P(r) = \left(\frac{M - r + 1}{M}\right)^k - \left(\frac{M - r}{M}\right)^k$$

Con $M = 200$ y $k = 3$, el mejor gana con probabilidad $\approx 1{,}5\ \%$ y el peor con $\approx 10^{-7}$. Un $k$ mayor aumenta la presión selectiva a costa de diversidad.

#### 6.6.3 Cruce de orden (OX)

Con probabilidad $p_c = 0{,}9$ los padres se cruzan con el operador OX (Davis, 1985); si no, el hijo copia al primer padre. Se eligen dos posiciones $a < b$, el hijo copia el segmento $[a, b]$ del primer padre, y las posiciones restantes, desde $b + 1$ y dando la vuelta, se llenan con las ciudades que faltan en el orden en que aparecen en el segundo padre (Tabla 15).

**Tabla 15.** *Ejemplo del cruce OX con N = 8, a = 2 y b = 4 (posiciones desde 0)*

| | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Padre 1 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| Padre 2 | 4 | 7 | 1 | 0 | 6 | 2 | 5 | 3 |
| Hijo | 0 | 6 | 2 | 3 | 4 | 5 | 7 | 1 |

A diferencia del cruce en un punto usado en la Parte 1, que en permutaciones genera ciudades repetidas (Larrañaga et al., 1999), OX siempre produce un recorrido válido y conserva el orden relativo de las ciudades heredadas, y con él el sentido de recorrido, relevante en un problema asimétrico.

#### 6.6.4 Mutación

Cada hijo se muta con probabilidad $p_m = 0{,}3$ invirtiendo el segmento entre dos posiciones aleatorias. En un TSP simétrico esto equivale a un movimiento 2-opt (Croes, 1958). En el asimétrico, además, cambia el costo de las aristas internas, porque pasan a recorrer en sentido contrario. Como alternativa está la mutación por intercambio de dos ciudades.

#### 6.6.5 Reemplazo, parada y evaluaciones

El reemplazo es generacional con elitismo: los $e = 2$ mejores individuos pasan intactos y los 198 restantes son hijos nuevos, de modo que el mejor costo nunca empeora. El algoritmo se detiene tras $G = 1500$ generaciones. Se cuenta una evaluación por cada recorrido nuevo (la población inicial y los hijos; las élites no se reevalúan):

$$n_{eval} = M + G\,(M - e) = 200 + 1500 \times 198 = 297\,200$$

Una corrida tarda unos 14 s en un computador personal. La Tabla 16 resume los parámetros.

**Tabla 16.** *Parámetros del algoritmo genético*

| Parámetro | Valor | Opción en línea de comandos |
|---|---|---|
| Tamaño de la población, M | 200 | `--tam-poblacion` |
| Generaciones, G | 1500 | `--generaciones` |
| Probabilidad de cruce, p_c | 0,9 | `--prob-cruce` |
| Probabilidad de mutación, p_m | 0,3 | `--prob-mutacion` |
| Tipo de mutación | inversión | `--tipo-mutacion` |
| Tamaño del torneo, k | 3 | `--tam-torneo` |
| Élites, e | 2 | `--elitismo` |
| Valor de la hora, v_h | 8,90 €/h | `--valor-hora` |
| Semilla base | 1983 | `--semilla` |

#### 6.6.6 Reproducibilidad y visualización

Los parámetros se leen de `config_tsp.json` y se pueden cambiar por línea de comandos; cada experimento se lanza con un solo comando (por ejemplo, `python algoritmo_genetico.py --valor-hora 40`). La corrida $r$ usa la semilla $1983 + r$ con `numpy.random.default_rng` (Harris et al., 2020), y el mismo comando reproduce exactamente el mismo resultado en otra máquina. El programa guarda en `resultados/ga/` las estadísticas, la mejor ruta tramo a tramo con cada componente del costo, la evolución del costo por generación y la mejor ruta hasta cada generación. A partir de esta última, el script `gif_ruta.py` genera el GIF de la evolución de la ruta sobre el mapa de la península, con el nombre de cada ciudad y flechas que indican el sentido del recorrido. Las coordenadas se obtuvieron una sola vez con Nominatim y están en el repositorio.

### 6.7 Resultados de la solución por algoritmos genéticos

Con los parámetros de la Tabla 10 [*sic*; corresponde a la Tabla 16] y la semilla 1983, el algoritmo genético encontró un recorrido de costo total 1421,04 €, tras 297 200 evaluaciones de la función objetivo y 13,8 s de cómputo. El recorrido, partiendo de Madrid, es:

**Figura 21.** *Mejor recorrido encontrado por el algoritmo genético sobre el mapa de la España peninsular (costo total 1421,04 €). Las flechas indican el sentido del recorrido, que parte de Madrid.*
Fuente: elaboración propia, `Parte_2/resultados/ga/ruta_final.png`.

La Figura 21 muestra el recorrido sobre el mapa. La ruta sale de Madrid hacia el norte por Castilla y León, recorre la cornisa cantábrica y Galicia, baja por el oeste (Zamora, Salamanca, Extremadura) hasta Andalucía, sigue por la costa mediterránea hasta Cataluña y regresa al centro por Aragón, Soria, Guadalajara y Cuenca. No tiene cruces entre tramos, una señal visual habitual de que no quedan mejoras locales evidentes. La Tabla 17 desglosa el costo.

**Tabla 17.** *Desglose del costo del mejor recorrido encontrado*

| Componente | Detalle | Costo (€) | Participación |
|---|---|---:|---:|
| Tiempo del vendedor | 91,36 h × 8,90 €/h | 813,1 | 57,2 % |
| Combustible | 6 797,72 km | 570,91 | 40,2 % |
| Peajes | 4 tramos | 37,03 | 2,6 % |
| **Total** | | **1 421,04** | **100,0 %** |

El tiempo del vendedor es el componente dominante del costo, seguido del combustible. Los peajes pesan poco: la ruta solo usa cuatro tramos con peaje, Madrid–Toledo (9,35 €), Ávila–Segovia (8,62 €), Logroño–Vitoria-Gasteiz (7,92 €) y Murcia–Alicante (11,14 €). El tramo más costoso es Teruel–Tarragona (258,65 km; 59,90 €) y el más barato, Valencia–Castellón de la Plana (76,66 km; 15,43 €).

La Tabla 18 muestra la evolución del costo a lo largo de las generaciones.

**Tabla 18.** *Evolución del mejor costo y del costo medio de la población*

| Generación | Evaluaciones acumuladas | Mejor costo encontrado (€) | Costo medio de la población (€) |
|---:|---:|---:|---:|
| 0 | 200 | 3 846,45 | 4 710,61 |
| 50 | 10 100 | 2 208,68 | 2 581,40 |
| 100 | 20 000 | 1 975,08 | 2 421,47 |
| 250 | 49 700 | 1 609,82 | 2 011,12 |
| 500 | 99 200 | 1 426,98 | 1 590,40 |
| 1000 | 198 200 | 1 421,35 | 1 504,21 |
| 1500 | 297 200 | 1 421,04 | 1 499,69 |

El mejor costo bajó un 63 % respecto al mejor recorrido aleatorio de la población inicial. La mejora se concentra al comienzo: el 90 % de la reducción total se alcanzó en la generación 209 y el 99 % en la generación 477. Después solo hubo ajustes pequeños, el último en la generación 1427, y en total la mejor ruta cambió 98 veces. Al final, el costo medio de la población (1499,69 €) sigue un 5,5 % por encima del mejor, es decir, la población conserva algo de diversidad y no colapsó en una sola solución.

### 6.8 Conclusiones y comparaciones

#### 6.8.1 Parte 1: Optimización numérica

1. **Ningún método domina en todos los escenarios.** Con 5000 evaluaciones, la evolución diferencial (DE) fue claramente superior en 2D: 100 % de éxito en Rosenbrock y Rastrigin, con medias de $1{,}2\times10^{-10}$ y $1{,}3\times10^{-8}$. En 3D su ventaja se mantuvo en Rosenbrock (media $3{,}2\times10^{-4}$) pero se perdió en Rastrigin (0 % de éxito, media 0,90).
2. **El descenso por gradiente depende de dónde empieza.** En Rastrigin cae en el mínimo local más cercano: 0 % de éxito con paso fijo y 10 % con backtracking, que fue la tasa más alta entre las variantes de gradiente. En Rosenbrock el mal condicionamiento ($\kappa \approx 2{,}5\times10^3$) lo hace lento, y ninguna variante alcanzó el umbral. Cuando parte en la cuenca correcta es muy eficiente ($\approx 400$ de costo efectivo frente a 5000 de las metaheurísticas).
3. **El gradiente cuesta más de lo que parece.** Con la equivalencia $1\,\nabla f \equiv 2n$ evaluaciones de $f$, el GD analítico consume entre 3 y 7 veces el presupuesto de los demás métodos, y esta ventaja a favor de las metaheurísticas se mantiene bajo cualquier equivalencia de costo positiva.
4. **El ranking depende de los hiperparámetros y de la dimensión.** Con los valores de clase, PSO y el evolutivo quedaron por debajo de DE, pero PSO alcanza 100 % de éxito en Rastrigin 2D con $c_1 = c_2 = 1{,}5$ y $w = 0{,}7$. En 3D ningún método resolvió Rastrigin de forma fiable. Que DE necesite más generaciones o población es una hipótesis que no se verificó.
5. **Trabajo futuro.** Un enfoque híbrido (exploración poblacional y refinamiento con gradiente) combinaría las fortalezas de ambas familias, pero no se evaluó.

#### 6.8.2 Parte 2: Problema del viajero

1. **Ambos algoritmos llegan a soluciones prácticamente equivalentes.** La colonia de hormigas (escenario Explorador) obtuvo 1.421,54 € y el algoritmo genético 1.421,04 €, una diferencia de 0,50 € ($\approx 0{,}04\ \%$). Esta diferencia no basta para declarar un ganador: proviene de una sola corrida de cada método.
2. **En ACO, los hiperparámetros marcaron la diferencia.** El escenario Explorador (50 hormigas, $\rho = 0{,}05$, `choose_best` = 0,05) superó al Base en 3,73 % y al Voraz en 4,81 %. El Voraz convergió rápido pero quedó atrapado por su sesgo heurístico ($\beta = 4{,}5$). La exploración tiene un costo en tiempo: 18,1 s frente a 4,7 s y 6,3 s.
3. **El algoritmo genético converge rápido y mantiene diversidad.** El 99 % de la mejora total se logró en la generación 477 de 1500, y al final la población seguía 5,5 % por encima del mejor, sin colapsar. El operador OX preserva el sentido del recorrido, que importa en un problema asimétrico.
4. **El costo lo domina el tiempo del conductor.** En la mejor ruta del AG, el tiempo representa el 57,2 %, el combustible el 40,2 % y los peajes solo el 2,6 %. Por eso el modelo favorece rutas rápidas sobre rutas cortas.
5. **Calidad de las rutas.** Ambas soluciones (Explorador y AG) forman circuitos cerrados sin cruces entre tramos, a diferencia de la del escenario Voraz.

---

## 7. Uso de la IA. Principales prompts utilizados

### 7.2 Implementación del algoritmo genético (sección 6.6)

**Prompt:** "Implementa los operadores de un algoritmo genético para el TSP con representación por permutaciones: selección por torneo, cruce de orden y mutación por inversión, y documenta cada operador en el código."

**Impacto:** redujo el tiempo de implementación de los operadores. El diseño de la solución estuvo a cargo del equipo: integrar las matrices de costos, dejar el valor de la hora como parámetro y contar las evaluaciones. Antes de incorporar lo sugerido se verificó que la matriz de costos coincidiera con `matriz_costo_total_euros.csv` y que el ejemplo de la Tabla 9 se reprodujera al ejecutar el código. En esa revisión se detectó el error documentado en la sección 8.1, que no afectó los resultados porque el costo de cada solución siempre se recalcula completo.

### 7.3 Resultados del algoritmo genético y visualización (sección 6.7)

**Prompt:** "Guarda la mejor ruta de cada generación para generar después, en un script aparte, un GIF de su evolución sobre el mapa, con el sentido del recorrido y los nombres de las ciudades."

**Impacto:** facilitó construir las Figuras 15 y 16 a partir de los datos guardados por el algoritmo, sin volver a ejecutarlo. Los resultados de la sección 6.7 se tomaron directamente de los archivos generados, y su reproducibilidad se comprobó obteniendo el mismo costo (1421,04 €) con la misma semilla en dos computadores distintos.

## 8. Cacería de la alucinación

### 8.1 La mutación por inversión no equivale a un 2-opt en un TSP asimétrico

**Categoría:** Conceptos.

**Prompt** (reformulado con el contexto de la conversación): "Implementa los operadores de un algoritmo genético para el TSP con representación por permutaciones: selección por torneo, cruce de orden y mutación por inversión, y documenta cada operador en el código."

**Respuesta de la IA:** en la línea 20 de `Parte_2/algoritmo_genetico.py`, la mutación se documenta como: "invierte el segmento r[i..j] (equivale a un movimiento 2-opt)".

**Cómo se sospechó:** un 2-opt solo cambia las dos aristas de los extremos del segmento, lo cual supone costos simétricos. Aquí $C_{ij} \neq C_{ji}$, así que al invertir el segmento las aristas internas se recorren al revés y su costo también cambia.

**Evidencia:** el cambio real de costo es el del 2-opt más un término que solo se anula si la matriz es simétrica:

$$\Delta_{real} = \Delta_{2\text{-}opt} + \sum_{k=i}^{j-1} \left( C_{\pi_{k+1},\pi_k} - C_{\pi_k,\pi_{k+1}} \right)$$

**Corrección:** la sección 6.6.4 describe el operador correctamente. La implementación no requirió cambios, porque el costo de cada hijo siempre se recalcula completo, nunca con la fórmula del 2-opt.

**Lección aprendida:** una propiedad de un operador solo vale bajo los supuestos en que se demostró, en este caso la simetría. Un experimento numérico rápido que compare el cambio de costo predicho con el recalculado lo habría detectado.

## 9. Links adicionales

### 9.1 Videos explicación aportes individuales

<https://drive.google.com/drive/folders/1hp3Bd6TGe0t1FEH5LlFKd0gPjSxsjq5S>

### 9.2 Repositorio

<https://github.com/Gmiercrack/Redes-Neuronales-y-algoritmos-Bionispirados>

## Referencias

- Ballou, R. H., Rahbar, H., & Amini, M. M. (2002). Development of actual highway distances from network data. *Transportation Research Part E: Logistics and Transportation Review, 38*(4), 267–281. <https://doi.org/10.1016/S1366-5545(02)00008-8>
- Dacia España. (2024). *Ficha técnica: Dacia Sandero TCe (Protocolo WLTP)*. Renault Group. <https://www.dacia.es/>
- Haklay, M., & Weber, P. (2008). OpenStreetMap: User-generated street maps. *IEEE Pervasive Computing, 7*(4), 12–18. <https://doi.org/10.1109/MPRV.2008.80>
- Luxen, D., & Vetter, C. (2011). Real-time routing with Open Source Routing Machine. En *Proceedings of the 19th ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems (GIS '11)* (pp. 513–516). Association for Computing Machinery. <https://doi.org/10.1145/2093973.2094062>
- Miller, C. E., Tucker, A. W., & Zemlin, R. A. (1960). Integer programming formulation of traveling salesman problems. *Journal of the ACM, 7*(4), 326–329. <https://doi.org/10.1145/321043.321046>
- Ministerio de Transportes y Movilidad Sostenible. (2024). *Catálogo de la Red de Carreteras del Estado: Autopistas en régimen de concesión y tarifas aplicables*. Gobierno de España. <https://www.transportes.gob.es/>
- Ministerio para la Transición Ecológica y el Reto Demográfico. (s. f.). *Geoportal de gasolineras: Estadísticas y precios de carburantes en España*. Gobierno de España. Recuperado de <https://geoportalgasolineras.es/>
- Real Decreto 145/2024, de 6 de febrero, por el que se fija el salario mínimo interprofesional para 2024. *Boletín Oficial del Estado, 33*, de 7 de febrero de 2024. <https://www.boe.es/eli/es/rd/2024/02/06/145>
- Croes, G. A. (1958). A method for solving traveling-salesman problems. *Operations Research, 6*(6), 791–812. <https://doi.org/10.1287/opre.6.6.791>
- Davis, L. (1985). Applying adaptive algorithms to epistatic domains. En *Proceedings of the 9th International Joint Conference on Artificial Intelligence* (Vol. 1, pp. 162–164). Morgan Kaufmann.
- Goldberg, D. E. (1989). *Genetic algorithms in search, optimization, and machine learning*. Addison-Wesley.
- Karp, R. M. (1972). Reducibility among combinatorial problems. En R. E. Miller & J. W. Thatcher (Eds.), *Complexity of computer computations* (pp. 85–103). Plenum Press.
- Larrañaga, P., Kuijpers, C. M. H., Murga, R. H., Inza, I., & Dizdarevic, S. (1999). Genetic algorithms for the travelling salesman problem: A review of representations and operators. *Artificial Intelligence Review, 13*(2), 129–170. <https://doi.org/10.1023/A:1006529012972>
- Miller, B. L., & Goldberg, D. E. (1995). Genetic algorithms, tournament selection, and the effects of noise. *Complex Systems, 9*(3), 193–212.
