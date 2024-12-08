import random

class PIDOptimizer:
    def __init__(self, transfer_function, car_mass, pendulum_mass, rod_length, gravity,
                 population_size=20, generations=50, mutation_rate=0.1):
        self.transfer_function = transfer_function
        self.car_mass = car_mass
        self.pendulum_mass = pendulum_mass
        self.rod_length = rod_length
        self.gravity = gravity
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

        # Iniciar población aleatoria con valores iniciales para Kp, Ki y Kd
        self.population = [self.random_parameters() for _ in range(population_size)]

    def random_parameters(self):
        # Devuelve un conjunto aleatorio de parámetros (Kp, Ki, Kd)
        return [random.uniform(0, 10) for _ in range(3)]

    def simulate_system(self, Kp, Ki, Kd):
        # Aquí debes llamar a tu clase InvertedPendulum para simular el sistema
        # y calcular su rendimiento basado en la estabilidad y control del sistema.

        from system.inverted_pendulum import InvertedPendulum

        transfer_function = self.transfer_function
        pendulum = InvertedPendulum(transfer_function)

        # Simula tu sistema con los parámetros PID actuales
        time_pid, response_pid = pendulum.simulate_with_pid(Kp, Ki, Kd)

        # Calcular fitness basándose en el error de respuesta y estabilidad
        error = sum(abs(response_pid))  # Ejemplo básico de fitness basado en error

        return -error  # Queremos minimizar el error

    def fitness(self, parameters):
        Kp, Ki, Kd = parameters
        return self.simulate_system(Kp, Ki, Kd)

    def optimize_parameters(self):
        for generation in range(self.generations):
            # Evaluar la población actual
            scored_population = [(individual, self.fitness(individual)) for individual in self.population]
            scored_population.sort(key=lambda x: x[1], reverse=True)

            # Mantener la mejor población después de cada generación
            self.population = [individual for individual, _ in scored_population]

            new_population = []

            # Asegurarse de que el tamaño de la población sea par
            if len(self.population) % 2 != 0:
                self.population = self.population[:-1]  # Elimina el último individuo si es impar

            # Cruza pares de individuos y aplica mutación
            for i in range(0, self.population_size, 2):
                parent1 = self.population[i]
                parent2 = self.population[i + 1]

                # Cruza promediando parámetros entre padres
                child = [(p1 + p2) / 2 for p1, p2 in zip(parent1, parent2)]

                # Aplica mutación aleatoria con una pequeña probabilidad
                if random.random() < self.mutation_rate:
                    child = [param + random.uniform(-1, 1) for param in child]

                new_population.append(child)

            self.population = new_population

            # Mejor solución encontrada hasta el momento
            best_params = self.population[0]
            print(f'Generación {generation+1}, Mejor PID: Kp={best_params[0]}, Ki={best_params[1]}, Kd={best_params[2]}')

        return self.population[0]  # Mejor conjunto de parámetros PID encontrado
