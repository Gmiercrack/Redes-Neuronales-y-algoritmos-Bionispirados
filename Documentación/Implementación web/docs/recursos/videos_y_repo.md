# Recursos, Videos y Repositorio

En esta sección se centralizan los enlaces de acceso al código fuente reproducible, los cuadernos computacionales interactivos y las grabaciones audiovisuales de sustentación del equipo.

---

## 1. Grabaciones de Sustentación Individual

Cada integrante del equipo grabó una sustentación audiovisual detallada explicando sus contribuciones técnicas, la fundamentación matemática y el análisis de resultados obtenidos en las diferentes fases del proyecto:

[Acceder a la Carpeta de Videos en Google Drive :material-google-drive:](https://drive.google.com/drive/folders/1hp3Bd6TGe0t1FEH5LlFKd0gPjSxsjq5S){ .md-button .md-button--primary target="_blank" }

---

## 2. Repositorio Oficial en GitHub

Todo el código fuente, conjuntos de datos geoespaciales, scripts de generación de figuras y cuadernos Jupyter se encuentran bajo control de versiones:

[Ir al Repositorio en GitHub :material-github:](https://github.com/Gmiercrack/Redes-Neuronales-y-algoritmos-Bionispirados){ .md-button target="_blank" }

---

## 3. Guía Rápida de Reproducibilidad

### 3.1 Ejecución de la Parte 1 (Optimización Numérica)
Para reproducir las 720 corridas experimentales completas, generar los archivos CSV y las gráficas estadísticas y animaciones GIF:

```bash
cd parte1
python run.py
```

### 3.2 Ejecución de la Parte 2 (Problema del Viajero en España)
Para consultar las APIs de OSRM y Nominatim, generar las matrices de costo logístico y ejecutar el Algoritmo Genético y la Colonia de Hormigas:

```bash
cd Parte_2

# 1. Geocodificación y matrices viales
python exportar_coordenadas.py
python costos.py

# 2. Ejecución del Algoritmo Genético
python algoritmo_genetico.py --generaciones 1500 --tam-poblacion 200

# 3. Generación del GIF de la ruta sobre el mapa peninsular
python gif_ruta.py
```
