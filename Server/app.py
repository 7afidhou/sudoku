from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import requests

from ga_solver import genetic_algorithm  # ✅ import your GA file

app = Flask(__name__)
CORS(app)


@app.route("/sudoku", methods=["GET"])
def sudoku_solver():
    # Step 1: Fetch puzzle
    response = requests.get("https://sudoku-api.vercel.app/api/dosuku")
    data = response.json()

    difficulty = data["newboard"]["grids"][0]["difficulty"]
    grid_data = data["newboard"]["grids"][0]

    puzzle_data = np.array(grid_data["value"])
    api_solution = np.array(grid_data["solution"])

    # Step 2: Solve with GA
    gen_solution = genetic_algorithm(puzzle_data)

    # Step 3: Accuracy
    accuracy = np.sum(gen_solution == api_solution) / 81 * 100
    print(f"GA Solution Accuracy: {accuracy:.2f}%")

    return jsonify({
        "puzzle": puzzle_data.tolist(),
        "api_solution": api_solution.tolist(),
        "ga_solution": gen_solution.tolist(),
        "difficulty": difficulty,
        "accuracy": accuracy
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
