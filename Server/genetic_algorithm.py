import numpy as np
import random

POP_SIZE = 50
MUTATION_RATE = 0.2
GENERATIONS = 5000


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
    
    # List of all 9 block positions (top-left corners)
    blocks = [(r, c) for r in range(0, 9, 3) for c in range(0, 9, 3)]
    random.shuffle(blocks)  # Shuffle block order
    
    i = random.randint(0, 9)  # Number of blocks to take from parent1
    
    # Take first i blocks from parent1
    for r, c in blocks[:i]:
        child[r:r+3, c:c+3] = parent1[r:r+3, c:c+3]
    
    # Take remaining blocks from parent2
    for r, c in blocks[i:]:
        child[r:r+3, c:c+3] = parent2[r:r+3, c:c+3]
    
    return child

# def crossover(parent1, parent2):
#     child = np.zeros((9,9), dtype=int)
    
#     # Random number of rows from parent1
#     i = random.randint(0, 9)  # i rows from parent1, 9-i from parent2
    
#     # Take first i rows from parent1
#     if i > 0:
#         child[:i] = parent1[:i]  
#     # Take remaining rows from parent2
#     if i < 9:
#         child[i:] = parent2[i:] 
#     return child


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
    best_fitness_over_time = []
    best_individual, best_fitness = None, 0
    for gen in range(GENERATIONS):
        # 1️⃣ Calculate fitness
        fitness_scores = [calculate_fitness(ind) for ind in population]

        # 2️⃣ Keep track of best
        gen_best = max(fitness_scores)
        best_fitness_over_time.append(gen_best)
        if gen_best > best_fitness:
            best_fitness = gen_best
            best_individual = population[fitness_scores.index(gen_best)]

        # ✅ Stop early if solved
        if best_fitness == 243:
            print(f"✅ Sudoku solved at generation {gen}!")
            break

        # 3️⃣ Sort population by fitness descending
        sorted_population = [ind for _, ind in sorted(zip(fitness_scores, population), key=lambda x: x[0], reverse=True)]

        # 4️⃣ Elitism: keep top 4 unchanged
        new_population = sorted_population[:4]

        # 5️⃣ Generate remaining children using top 4 as deterministic parents
        while len(new_population) < POP_SIZE:
            parent1, parent2 = random.sample(new_population,2) # selection among elites
            child = crossover(parent1, parent2)
            child = mutate(child, fixed_positions)
            new_population.append(child)

        population = new_population

        # ✅ Print progress every 50 generations
        if gen % 50 == 0 or gen == GENERATIONS - 1:
            print(f"Generation {gen} | Best fitness: {best_fitness}")

    return best_individual
