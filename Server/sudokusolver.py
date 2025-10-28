from flask import Flask, jsonify, request
import numpy as np
import random
import matplotlib.pyplot as plt
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)
# -------------------------------
# 🧠 Sudoku puzzle input (0 = empty)
# -------------------------------
# -------------------------------
# ⚙️ GA Parameters
# -------------------------------
POP_SIZE = 100
MUTATION_RATE = 0.2
GENERATIONS = 500  # Reduced for speed


# -------------------------------
# 🧬 Helper functions
# -------------------------------
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


# -------------------------------
# 🔁 Genetic Algorithm
# -------------------------------
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


# -------------------------------
# 🌐 Flask Endpoint
# -------------------------------
@app.route("/sudoku", methods=["GET"])
def sudoku_solver():
    # Step 1: Fetch puzzle from external API
    response = requests.get("https://sudoku-api.vercel.app/api/dosuku")
    data = response.json()
    difficulty = data["newboard"]["grids"][0]["difficulty"]
    grid_data = data["newboard"]["grids"][0]
    puzzle_data = np.array(grid_data["value"])
    api_solution = np.array(grid_data["solution"])
    # Step 2: Solve with your GA
    gen_solution = genetic_algorithm(puzzle_data)

    # Step 3: Compute accuracy (optional)
    accuracy = np.sum(gen_solution == api_solution) / 81 * 100
    print(f"GA Solution Accuracy: {accuracy:.2f}%")
    # Step 4: Return everything
    return jsonify({
        "puzzle": puzzle_data.tolist(),
        "api_solution": api_solution.tolist(),
        "ga_solution": gen_solution.tolist(),
        "difficulty": difficulty,
        "accuracy": accuracy
    })


# -------------------------------
# 🚀 Run Flask App
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
