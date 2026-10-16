# Fundamentos Matemáticos y Algoritmos Evaluados

En esta primera parte del trabajo se estudian y comparan métodos clásicos de optimización basados en gradiente frente a metaheurísticas bioinspiradas de base poblacional. 

Para este estudio se seleccionaron dos funciones de prueba canónicas de la literatura de optimización global continua: **Rosenbrock** y **Rastrigin**. Ambas son complementarias:
- **Rosenbrock:** Presenta un único mínimo global, pero situado en un valle parabólico estrecho, curvado y mal condicionado que dificulta severamente el avance de métodos de primer orden.
- **Rastrigin:** Presenta una cantidad exponencial de mínimos locales periódicos, castigando la miopía de los métodos locales y premiando la exploración diversa de las metaheurísticas poblacionales.

---

## 1. Funciones de Prueba

Sea $x = (x_1, \dots, x_n) \in \mathbb{R}^n$.

### 1.1 Función de Rosenbrock (Valle del Plátano)
Introducida por Rosenbrock (1960), se formula como:

$$f(x) = \sum_{i=1}^{n-1} \left[ 100\,(x_{i+1} - x_i^2)^2 + (1 - x_i)^2 \right]$$

El gradiente analítico respecto a cada coordenada $x_i$ viene dado por:

$$\frac{\partial f}{\partial x_i} = -400\,x_i\,(x_{i+1} - x_i^2) - 2(1 - x_i) \;\;(\text{si } i < n) \;+\; 200\,(x_i - x_{i-1}^2) \;\;(\text{si } i > 1)$$

- **Dominio de búsqueda:** $[-5, 5]^n$.
- **Mínimo global:** $x^* = (1, \dots, 1)$, con $f(x^*) = 0$.
- **Condicionamiento:** Para $n = 2$, el Hessiano en $x^*$ es:
  
  $$\nabla^2 f(x^*) = \begin{pmatrix} 802 & -400 \\ -400 & 200 \end{pmatrix}$$
  
  con autovalores $\lambda_1 \approx 1001{,}6$ y $\lambda_2 \approx 0{,}40$. El número de condición es $\kappa \approx 2{,}5 \times 10^3$. Esta severa disparidad de curvatura impone que el descenso de gradiente con paso fijo deba usar un paso $\eta < 2/L \approx 2 \times 10^{-3}$, avanzando a un ritmo extremadamente lento a lo largo del valle.

---

### 1.2 Función de Rastrigin (Paisaje Altamente Multimodal)
Propuesta por Rastrigin (1974) y generalizada por Mühlenbein et al. (1991):

$$f(x) = A\,n + \sum_{i=1}^{n} \left[ x_i^2 - A\cos(2\pi x_i) \right], \quad A = 10$$

Su gradiente analítico es:

$$\frac{\partial f}{\partial x_i} = 2x_i + 2\pi A \sin(2\pi x_i)$$

- **Dominio de búsqueda:** $[-5{,}12;\ 5{,}12]^n$.
- **Mínimo global:** $x^* = (0, \dots, 0)$, con $f(x^*) = 0$.
- **Paisaje:** Existen aproximadamente $11^n$ mínimos locales dentro del dominio (121 en 2D y 1331 en 3D). El Hessiano en el origen es $(2 + 40\pi^2)\,I \approx 397\,I$, lo cual conforma cuencas muy estrechas y pronunciadas ($L \approx 397$, paso estable $\eta < 2/L \approx 5 \times 10^{-3}$).

---

## 2. Métodos Basados en Gradiente

El esquema de actualización general del descenso por gradiente es:

$$x^{(t+1)} = x^{(t)} - \eta\,\nabla f(x^{(t)})$$

Se evalúan tres variantes:

1. **GD Analítico:** Utiliza la expresión matemática exacta de $\nabla f$ y una tasa de aprendizaje $\eta$ fija, calibrada previamente.
2. **GD Numérico:** El gradiente se aproxima mediante diferencias hacia adelante:
   
   $$\frac{\partial f}{\partial x_i} \approx \frac{f(x + h e_i) - f(x)}{h}, \quad h = 10^{-3}$$
   
   lo cual induce un error de truncamiento $O(h)$ y requiere $n$ evaluaciones adicionales de $f$ por iteración.
3. **GD con Búsqueda Lineal Backtracking (Condición de Armijo):** Inicia en $\eta_0 = 1$ y reduce $\eta \leftarrow \beta\eta$ con $\beta = 0{,}5$ hasta satisfacer:
   
   $$f(x - \eta g) \le f(x) - c\,\eta\,\|g\|^2, \quad g = \nabla f(x), \; c = 10^{-4}$$

!!! note "Criterios de parada"
    Las iteraciones se detienen si $\|x^{(t+1)} - x^{(t)}\| < 10^{-8}$, si $\|\nabla f\| < 10^{-12}$, si se agota el presupuesto estricto de 5000 evaluaciones o ante divergencia numérica ($\|x\|_\infty > 10^6$).

---

## 3. Metaheurísticas Bioinspiradas

### 3.1 Algoritmo Evolutivo (Esquema Canónico)
- **Población:** $N = 50$ individuos en $\mathbb{R}^n$, 100 generaciones (5000 evaluaciones de $f$).
- **Selección y Reemplazo:** En cada generación la población se ordena por aptitud y se conforma por tres grupos:
  - **Élite (15%):** Los mejores individuos se copian directamente sin alteración.
  - **Mutación (10%):** Mutación gaussiana $x'_j = x_j + \sigma_j\,\xi$, con $\xi \sim N(0,1)$ y $\sigma_j$ igual a la desviación estándar de la coordenada en la población.
  - **Cruzamiento (75%):** Cruzamiento en un punto de corte aleatorio $p \in \{1, \dots, n-1\}$.

### 3.2 Optimización por Enjambre de Partículas (PSO)
Implementado mediante `GlobalBestPSO` de la biblioteca PySwarms (Miranda, 2018):

$$v_i^{(t+1)} = w\,v_i^{(t)} + c_1\,r_1 \odot (b_i - x_i^{(t)}) + c_2\,r_2 \odot (g - x_i^{(t)})$$
$$x_i^{(t+1)} = x_i^{(t)} + v_i^{(t+1)}$$

- **Parámetros:** $N = 50$ partículas, 100 iteraciones (5000 evaluaciones). Coeficiente cognitivo $c_1 = 0{,}5$, social $c_2 = 0{,}3$, e inercia $w = 0{,}9$.

### 3.3 Evolución Diferencial (DE/rand/1/bin)
Estrategia propuesta por Storn y Price (1997):
1. **Mutación:** Para cada vector $x_i$, se seleccionan tres índices mutuamente excluyentes $r_1, r_2, r_3 \neq i$:
   
   $$v_i = x_{r_1} + F\,(x_{r_2} - x_{r_3})$$
   
2. **Cruce binomial:** Se genera el vector de prueba $u_i$:
   
   $$u_{i,j} = \begin{cases} v_{i,j} & \text{si } U(0,1) < CR \text{ o } j = j_{rand} \\ x_{i,j} & \text{en otro caso} \end{cases}$$
   
3. **Selección codiciosa:**
   
   $$x_i^{(t+1)} = \begin{cases} u_i & \text{si } f(u_i) \le f(x_i) \\ x_i & \text{en otro caso} \end{cases}$$

- **Parámetros:** $N = 50$ individuos, factor de escala $F = 0{,}8$, constante de cruce $CR = 0{,}9$.
