import numpy as np
import random

POP_SIZE = 100
MUTATION_RATE = 0.2
GENERATIONS = 500


def generate_individual(puzzle):
    individual = np.zeros((9, 9), dtype=int)
    for i in range(9):
        nums = set(range(1, 10)) - set(puzzle[i])
        row = puzzle[i].copy()
        for j in range(9):
            if row[j] == 0:
                val = random.choice(list(nums))
                row[j] = val
                nums.remove(val)
        individual[i] = row
    return individual


def calculate_fitness(individual):
    score = 0
    for row in individual:
        score += len(set(row))
    for col in individual.T:
        score += len(set(col))
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block = individual[i:i+3, j:j+3].flatten()
            score += len(set(block))
    return score


def crossover(parent1, parent2):
    child = np.zeros((9, 9), dtype=int)
    for i in range(9):
        child[i] = parent1[i] if random.random() < 0.5 else parent2[i]
    return child


def mutate(individual, fixed_positions):
    for i in range(9):
        if random.random() < MUTATION_RATE:
            available = [j for j in range(9) if not fixed_positions[i][j]]
            if len(available) >= 2:
                a, b = random.sample(available, 2)
                individual[i][a], individual[i][b] = individual[i][b], individual[i][a]
    return individual


def get_fixed_positions(puzzle):
    fixed = np.zeros((9, 9), dtype=bool)
    fixed[puzzle != 0] = True
    return fixed


def genetic_algorithm(puzzle):
    fixed_positions = get_fixed_positions(puzzle)
    population = [generate_individual(puzzle) for _ in range(POP_SIZE)]
    best_individual = None
    best_fitness = 0
    for gen in range(GENERATIONS):
        fitness_scores = [calculate_fitness(ind) for ind in population]
        gen_best = max(fitness_scores)
        if gen_best > best_fitness:
            best_fitness = gen_best
            best_individual = population[fitness_scores.index(gen_best)]
        if best_fitness == 243:
            break
        new_population = []
        for _ in range(POP_SIZE):
            a, b = random.sample(range(POP_SIZE), 2)
            parent1 = population[a] if fitness_scores[a] > fitness_scores[b] else population[b]
            a, b = random.sample(range(POP_SIZE), 2)
            parent2 = population[a] if fitness_scores[a] > fitness_scores[b] else population[b]
            child = crossover(parent1, parent2)
            child = mutate(child, fixed_positions)
            new_population.append(child)
        population = new_population
    return best_individual
