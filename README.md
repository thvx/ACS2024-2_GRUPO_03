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