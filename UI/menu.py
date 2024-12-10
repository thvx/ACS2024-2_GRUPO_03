import tkinter as tk
from run_simulations import (
    run_system_function_position,
    run_system_function_angle,
    run_pid_simulacion,
    run_pid_optimized,
    run_pid_with_kalman_filter
)

class SimulationMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Menú de Simulación PID")
        self.create_widgets()

    def create_widgets(self):
        # Etiqueta principal
        label = tk.Label(self.root, text="Seleccione una opción:", font=("Arial", 14))
        label.pack(pady=10)

        # Botones de opciones
        buttons = [
            ("Sistema sin PID (posición)", run_system_function_position),
            ("Sistema sin PID (ángulo)", run_system_function_angle),
            ("Simulación PID", run_pid_simulacion),
            ("PID Optimizado", run_pid_optimized),
            ("PID Optimizado con Filtro de Kalman", run_pid_with_kalman_filter),
        ]

        for text, command in buttons:
            btn = tk.Button(self.root, text=text, font=("Arial", 12), command=command)
            btn.pack(pady=5)

        btn_exit = tk.Button(self.root, text="Salir", font=("Arial", 12), command=self.root.quit)
        btn_exit.pack(pady=20)

    def run(self):
        self.root.mainloop()
