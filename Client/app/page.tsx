"use client";

import { useState, useEffect } from "react";

export default function Home() {
  const [puzzle, setPuzzle] = useState([]);
  const [apiSolution, setApiSolution] = useState([]);
  const [gaSolution, setGaSolution] = useState([]);
  const [difficulty, setDifficulty] = useState("");
  const [view, setView] = useState("puzzle");
  const [loading, setLoading] = useState(true);
  const [accuracy, setAccuracy] = useState("");

  // Reusable fetch function (used both on load and "New Puzzle" click)
  const fetchSudoku = async () => {
    try {
      setLoading(true);
      setView("puzzle");

      const res = await fetch("http://localhost:5050/sudoku", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });

      const data = await res.json();

      setPuzzle(data.puzzle);
      setGaSolution(data.ga_solution);
      setApiSolution(data.api_solution);
      setDifficulty(data.difficulty);
      setAccuracy(data.accuracy);
    } catch (err) {
      console.error("Error fetching Sudoku data:", err);
    } finally {
      setLoading(false);
    }
  };

  // Load the first puzzle when the page starts
  useEffect(() => {
    fetchSudoku();
  }, []);

  const getGrid = () => {
    if (view === "ga") return gaSolution;
    if (view === "api") return apiSolution;
    return puzzle;
  };

  const grid = getGrid();

  const nextView = () => {
    if (view === "puzzle") setView("ga");
    else if (view === "ga") setView("api");
    else setView("puzzle");
  };

  return (
    <div className="flex flex-col items-center bg-gray-100 min-h-screen p-10">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">
        🧩 Sudoku GA vs API Solver
      </h1>

      {loading ? (
        <p className="text-gray-600 text-lg">Loading Sudoku...</p>
      ) : (
        <>
          {/* Sudoku Grid */}
          <div className="flex flex-col gap-1 bg-white p-4 shadow-lg rounded-xl">
            {grid.map((row, rowIndex) => (
              <div key={rowIndex} className="flex gap-1">
                {row.map((cell, colIndex) => (
                  <div
                    key={colIndex}
                    className={`size-12 flex items-center justify-center text-lg font-semibold rounded ${
                      cell === 0
                        ? "bg-gray-300 text-gray-600"
                        : view === "puzzle"
                        ? "bg-amber-500 text-white"
                        : view === "ga"
                        ? "bg-blue-600 text-white"
                        : "bg-green-600 text-white"
                    }`}
                  >
                    {cell !== 0 ? cell : ""}
                  </div>
                ))}
              </div>
            ))}
          </div>

          {/* Labels */}
          <div className="mt-4 text-lg font-semibold text-gray-700">
            {view === "puzzle" && "🧠 Puzzle from API"}
            {view === "ga" && "🤖 Genetic Algorithm Solution"}
            {view === "api" && "✅ Official API Solution"}
          </div>

          {/* Accuracy display */}
          {accuracy && (
            <div className="mt-2 text-md text-gray-800">
              🎯 Accuracy (GA vs API):{" "}
              <span className="font-bold text-blue-700">{accuracy}%</span>
            </div>
          )}

          {/* Difficulty display */}
          {difficulty && (
            <div className="text-lg font-semibold text-amber-700">
              ⚙️ Difficulty:{" "}
              <span className="text-amber-600">{difficulty}</span>
            </div>
          )}

          {/* Buttons */}
          <div className="flex gap-4 mt-6">
            <button
              onClick={nextView}
              className="px-6 py-2 bg-amber-600 hover:bg-amber-700 text-white font-semibold rounded-lg transition"
            >
              {view === "puzzle"
                ? "Next → Show GA Solution"
                : view === "ga"
                ? "Next → Show API Solution"
                : "↩ Back to Puzzle"}
            </button>

            {/* 🔄 New Puzzle Button */}
            <button
              onClick={fetchSudoku}
              className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition"
            >
              🔄 New Puzzle
            </button>
          </div>
        </>
      )}
    </div>
  );
}
