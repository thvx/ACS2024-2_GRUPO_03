import matplotlib.pyplot as plt


def plot_step_response(time_steps, response):
    plt.figure()
    plt.plot(time_steps, response)
    plt.title("Respuesta al escalón del sistema de péndulo invertido")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Ángulo θ (rad)")
    plt.grid(True)
    plt.show()
