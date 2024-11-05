import React, { useState } from "react";
import axios from "axios";

function App() {
  const [size, setSize] = useState(5);
  const [mazeString, setMazeString] = useState("0....++++.++++.X++++");
  const [delayMs, setDelayMs] = useState(100);
  const [solutions, setSolutions] = useState([]);

  const solveMaze = async () => {
    try {
      const response = await axios.post("http://localhost:8000/solve_maze", {
        size,
        maze_string: mazeString,
        delay_ms: delayMs,
      });
      setSolutions(response.data.solutions);
    } catch (error) {
      console.error("Error solving maze", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Laberinto Solver</h2>
      <div>
        <label>
          Tamaño del laberinto (n x n):
          <input type="number" value={size} onChange={(e) => setSize(Number(e.target.value))} />
        </label>
      </div>
      <div>
        <label>
          Cadena de laberinto:
          <input
            type="text"
            value={mazeString}
            onChange={(e) => setMazeString(e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          Retraso entre pasos (ms):
          <input
            type="number"
            value={delayMs}
            onChange={(e) => setDelayMs(Number(e.target.value))}
          />
        </label>
      </div>
      <button onClick={solveMaze}>Resolver Laberinto</button>
      <div>
        <h3>Soluciones encontradas:</h3>
        {solutions.map((solution, index) => (
          <div key={index}>
            <h4>Solución {index + 1}:</h4>
            <pre>{JSON.stringify(solution, null, 2)}</pre>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
