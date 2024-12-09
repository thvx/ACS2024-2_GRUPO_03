import matplotlib.pyplot as plt


def plot_step_response(time_steps, response, y_label):
    plt.figure()
    plt.plot(time_steps, response)
    plt.title("Respuesta al escalón del sistema de péndulo invertido")
    plt.xlabel("Tiempo (s)")
    plt.ylabel(y_label)
    plt.grid(True)
    plt.show()
