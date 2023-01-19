import random

import numpy as np

# Evalua la calidad de cada candidato
# Esta evaluacion es modificable por los deseos de la empresa
# Ajustamos los pesos de acuerdo con la prioridad que soliciten

def calcular_fitness(candidato):
    # Inicializa el fitness en cero
    fitness = 0
    
    # Añade puntos por edad (más joven es mejor)
    fitness -= candidato[0] * 0.5
    
    # Añade puntos por años de experiencia (más años son mejores)
    fitness += candidato[1] * 0.1
    
    # Añade puntos por formación (más alta es mejor)
    fitness += candidato[2] * 0.3
        
    # Añade puntos por habilidades
    fitness += candidato[3] * 0.1

    # Devuelve el fitness
    return fitness

random.seed(0)

# Parámetros del algoritmo
N_PARTICLES = 250 # Número de partículas
N_DIMENSIONS = 4 # Número de dimensiones del problema (edad, experiencia, nivel de formación y habilidades)
N_ITERATIONS = 170 # Número de iteraciones del algoritmo
C1 = 0.5 # Constante de aceleración
C2 = 0.47 # Constante de aceleración
W = 0.8 # Inercia

print("SOLUCION AL PROBLEMA DE LA SELECCIÓN CON ENJAMBRE DE PARTICULAS \n")
print("No. de particulas: ", N_PARTICLES)
print("No. iteraciones: ", N_ITERATIONS)
print("")

# Crea un enjambre de partículas
enjambre = []
for i in range(N_PARTICLES):
    # Genera valores aleatorios para cada característica
    edad = random.randint(50, 64)
    años_de_experiencia = 0.5 * edad
    formacion = random.randint(1, 2)
    habilidades = random.randint(1, 2)
    
    # Incializamos las caractersisticas de nuestras particulas
    posicion = [edad, años_de_experiencia, formacion, habilidades]

    velocidad = [random.uniform(-5, 5) for _ in range(N_DIMENSIONS)]
    
    pbest = posicion
    
    particula = [posicion, velocidad, pbest]
    enjambre.append(particula)

# Inicializa la mejor solución global
global_best = enjambre[0][0]

# Ejecuta el algoritmo PSO
for t in range(N_ITERATIONS):
    # Recorre cada partícula del enjambre
    for i in range(N_PARTICLES):
        
        particula = enjambre[i]
        posicion = particula[0]
        velocidad = particula[1]
        
        # Actualizamos la velocidad de la partícula
        velocidad = [W * v + C1 * random.uniform(0, 1) * (pbest - x) + C2 * random.uniform(0, 1) * (gbest - x) for v, pbest, x, gbest in zip(velocidad, particula[2], posicion, global_best)]
        
        # Actualizamos la posición de la partícula
        agrupacion = zip(posicion, velocidad)
        posicion = []
        i = 0
        for j, (x, v) in enumerate(agrupacion):
            nuevaPos = x + v
            # Verificamos si nuestra nueva posicion ha alcanzado los limites propuestos 
            # (los limites van de acuerdo a las condiciones que pida una empresa)
            if i == 0:
                # No se contratan a gente de menos de 25 años
                if nuevaPos < 25:
                    posicion.append(25)
                # No se contrata a a gente de mas de 65 años
                elif nuevaPos > 65:
                    posicion.append(65)
                else:
                    posicion.append(nuevaPos)
            # Para la caracteristica de la experencia, realizamos una validacion
            # que tenga sentido logico, es decir, que la experencia se proporcional
            # a la edad.
            elif i == 1:
                if nuevaPos > posicion[j - 1] - posicion[j - 1] * 0.7:
                    posicion.append(posicion[j - 1] * 0.3)
                else:
                    posicion.append(nuevaPos)
            elif i == 2:
                # No se contrata a gente con mas de 4 formaciones
                if nuevaPos > 4:
                    posicion.append(4)
                else:
                    posicion.append(nuevaPos)
            elif i == 3:
                # No se contrata a gente con mas de 5 habilidades
                if nuevaPos > 5:
                    posicion.append(5)
                else:
                    posicion.append(nuevaPos)
            i += 1
        
        # Actualizamos la mejor posición de la partícula
        if calcular_fitness(posicion) > calcular_fitness(particula[2]):
            particula[2] = posicion
            
        # Actualizamos el mejor resultado global si es necesario
        if calcular_fitness(posicion)  > calcular_fitness(global_best):
            global_best = posicion
        else:
            continue
    
    # Imprimimos el mejor resultado obtenido en cada iteración
    print(f'Iteración {t}: {global_best}')

# Imprime la mejor solución global
print("\nLa mejor combinacion de caracteristicas obtenida es: \n")
print("Edad: ", global_best[0])
print("Experiencia: ", global_best[1])
print("Formacion: ", global_best[2])
print("Habilidades: ", global_best[3])


