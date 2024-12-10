# ACS2024-2_GRUPO_03
## Integrantes
- Castillo Carranza, Jose Richard
- Espinoza Fabian, Josue Marcelo
- Hinostroza Quispe, Gianlucas Amed
- Ipanaque Pazo, Jorge Paul
- Peña Manuyama, Dafna Nicole

# Péndulo Invertido con Control Moderno
El péndulo invertido es un problema clásico en la ingeniería de control que involucra mantener una varilla en posición vertical sobre un carro móvil mediante la aplicación de fuerzas horizontales. Este sistema es intrínsecamente inestable, lo que lo convierte en un desafío ideal para el diseño, análisis y evaluación de estrategias de control. El objetivo de este proyecto es diseñar e implementar un sistema de control mediante cun controlador PID para estabilizar el péndulo invertido.

# Descripción del Proyecto
Este proyecto implementa un sistema de control para un péndulo invertido utilizando un controlador PID optimizado y un filtro de Kalman para estimar el estado del sistema en presencia de ruido. La simulación incluye:
- Control de estabilidad del péndulo invertido usando un PID.
- Gráficos para visualizar el comportamiento del sistema (ángulo, ruido, posición).
- Animación del péndulo estabilizado.

# Estructura del Repositorio
- Papers/: Contiene artículos elevantes para el proyecto, en formato PDF.
- UI/: Incluye el archivo principal del menú (menu.py) que proporciona una interfaz gráfica para la simulación.
- analysis/: Incluye los scripts de análisis, como variaciones iniciales y curvas de error.
- design_implementation/: Implementa la configuración del controlador PID y su interfaz de ajuste.
- filtro_kalman/: Contiene módulos relacionados con el filtro de Kalman, incluyendo la lógica de estimación y la interfaz gráfica para controlarlo.
- optimization/: Contiene herramientas para optimizar el controlador PID con algoritmos genéticos
- system/: Define el modelo del sistema dinámico (péndulo invertido) y herramientas para graficar y animar su comportamiento.

```bash
ACS2024-2_GRUPO_03/
├── Papers/                     # Documentación del proyecto
├── README.md
├── UI/
│   └── menu.py                 # Interfaz gráfica del menú principal
├── analysis/                   # Scripts de análisis
│   ├── error_curve.py          # Análisis de curvas de error
│   └── initial_variation.py    # Evaluación de variaciones iniciales
├── design_implementation/      # Configuraciones de diseño
│   ├── PID.m                   # Script MATLAB de PID
│   ├── PID.py                  # Controlador PID en Python
│   ├── __init__.py
├── filtro_kalman/              # Implementación del filtro de Kalman
│   ├── kalmanFilter.py         # Lógica del filtro de Kalman
│   ├── kalmanGraphics.py       # Gráficos interactivos con Kalman
│   ├── __init__.py
├── main.py                     # Archivo principal del proyecto
├── optimization/               # Optimización del controlador PID
│   ├── Optimization.py         # Algoritmo de optimización
│   ├── __init__.py
├── requirements.txt            # Lista de dependencias
├── run_simulations.py          # Ejecución de simulaciones desde la CLI
└── system/                     # Modelado y visualización del sistema
    ├── animation.py            # Animación del sistema dinámico
    ├── inverted_pendulum.py    # Modelado del péndulo invertido
    ├── plot.py                 # Funciones de graficado
    ├── __init__.py

```

# Tecnologías Empleadas
- Lenguaje: Python 3.8+
- Librerías: numpy, scipy, matplotlib, control, pyqt5, plotly, tkinter

# Ejecución del Proyecto
- Clonar el Repositorio 
```bash
git clone https://github.com/thvx/ACS2024-2_GRUPO_03.git
```
- Instalar las librerías necesarias: 
```bash
pip install -r requirements.txt
```
- Ejecutar la simulación:
```bash
python main.py
```

# Opciones de Simulación
- Simulación sin PID (posición o ángulo)
- Simulación con PID sin optimizar
- Simulación con PID optimizado
- Simulación con Filtro de Kalman