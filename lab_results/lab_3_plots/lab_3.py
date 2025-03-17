import numpy as np
import subprocess
from rigid_body import run_body
import matplotlib.pyplot as plt
import pickle

palm_ = [0.3, 0.4, 0.02, 0.12]

def random_stiffness():
    return 40 * np.random.rand() + 10

def random_phalange_length():
    return 0.08 * np.random.rand() + 0.02

def random_phalange_width():
    return 0.03 * np.random.rand() + 0.02

def random_spring_offset():
    return 0.06 + np.random.rand() + 0.015

def random_phalanx_cnt():
    return np.random.randint(3) + 1

def mutation_scalar():
    return 0.2 * np.random.rand() - 0.1

def clamp(value, min, max):
    return(min(max(value, min), max))

def mutate(individual):
    indi = individual.copy()

    for p in indi[1]:
        p[0] = clamp(p[0] + random_phalange_length() * mutation_scalar(), 0.02, 0.10)
        p[1] = clamp(p[1] + random_phalange_width() * mutation_scalar(), 0.02, 0.05)
        p[2] = clamp(p[2] + random_stiffness() * mutation_scalar(), 10, 50)
    growth = np.random.rand()
    if(growth <= 0.1):
        indi[1].append([random_phalange_length(), random_phalange_width(), random_stiffness()])
    elif(growth >= 0.9):
        indi[1].pop()
    
    for p in indi[2]:
        p[0] = clamp(p[0] + random_phalange_length() * mutation_scalar(), 0.02, 0.10)
        p[1] = clamp(p[1] + random_phalange_width() * mutation_scalar(), 0.02, 0.05)
        p[2] = clamp(p[2] + random_stiffness() * mutation_scalar(), 10, 50)
    growth = np.random.rand()
    if(growth <= 0.1):
        indi[2].append([random_phalange_length(), random_phalange_width(), random_stiffness()])
    elif(growth >= 0.9):
        indi[2].pop()
    
    return indi

def create_individual():
    phalange_1 = []
    for i in range(random_phalanx_cnt()):
        phalange_1.append([random_phalange_length(), random_phalange_width(), random_stiffness()])
    
    phalange_2 = []
    for i in range(random_phalanx_cnt()):
        phalange_2.append([random_phalange_length(), random_phalange_width(), random_stiffness()])

    return [palm_, phalange_1, phalange_2, 0.01]

def create_generation(pop_cnt):
    population = []
    for i in range(pop_cnt):
        population.append(create_individual())
    
    return population

iteration_losses_min = []
iteration_losses_avg = []

def run_generation(population, gen_id):
    losses = []
    for i in range(len(population)):
        file = open('data.pkl', 'wb')
        pickle.dump(population[i], file)
        file.close()
        output = str(subprocess.check_output(["python3", "rigid_body.py", str(gen_id), str(i)])).split('\\n')[2]
        losses.append(float(output))
        print(output)


    iteration_losses_min.append(min(losses))
    iteration_losses_avg.append(sum(losses)/len(losses))
    return losses

def purge_replace_population(population, losses, p_keep=0.3):
    new_population = []
    min_loss = min(losses)
    purged = 0

    print(losses)

    sorted_loss = losses.copy()
    sorted_loss.sort()

    print(sorted_loss)

    for i in range(len(losses)):
        if(losses[i] <= (sorted_loss[int(len(population)*p_keep)])):
            print("Kept!")
            new_population.append(population[i])
    
    while (len(new_population) < len(population)):
        if(True):
            mutate_index = np.random.randint(len(new_population))
            new_population.append(mutate(new_population[mutate_index]))
        else:
            new_population.append(create_individual())
    
    return new_population

    

def main():

    population = create_generation(10)
    

    max_iters = 10

    for i in range(max_iters):
        if(i != max_iters-1):
            losses = run_generation(population, i)
            population = purge_replace_population(population, losses)
        else:
            losses = run_generation(population, i)

    print(iteration_losses_min)
    print(iteration_losses_avg)

    iterations = len(iteration_losses_min)

    plt.plot(np.linspace(1, iterations, iterations), iteration_losses_min)
    plt.title("Minimum Loss Over Iterations")
    plt.xlabel("Iterations")
    plt.ylabel("Loss")
    plt.show()

    plt.plot(np.linspace(1, iterations, iterations), iteration_losses_avg)
    plt.title("Average Loss Over Iterations")
    plt.xlabel("Iterations")
    plt.ylabel("Loss")
    plt.show()

    
main()
