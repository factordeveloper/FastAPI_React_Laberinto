from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple, Dict
from collections import deque
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MazeInput(BaseModel):
    size: int
    maze_string: str
    delay_ms: int

class MazeSolution(BaseModel):
    path: List[Tuple[int, int]]
    time_found: float
    length: int

class MazeSolver:
    def __init__(self, size: int, maze_string: str):
        self.size = size
        self.maze = self._create_maze_matrix(maze_string)
        self.start = self._find_position('0')
        self.end = self._find_position('X')
        self.solutions = []

    def _create_maze_matrix(self, maze_string: str) -> List[List[str]]:
        return [list(maze_string[i:i + self.size]) for i in range(0, len(maze_string), self.size)]

    def _find_position(self, char: str) -> Tuple[int, int]:
        for i in range(self.size):
            for j in range(self.size):
                if self.maze[i][j] == char:
                    return (i, j)
        return (-1, -1)

    def is_reachable(self) -> bool:
        visited = set()
        queue = deque([self.start])
        while queue:
            x, y = queue.popleft()
            if (x, y) == self.end:
                return True
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.size and 0 <= ny < self.size and 
                    self.maze[nx][ny] != '+' and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return False

    def solve(self) -> List[Tuple[int, int]]:
        self.solutions.clear()
        if not self.is_reachable():
            return []
        visited = set()
        current_path = []
        self._dfs(self.start[0], self.start[1], visited, current_path)
        return self.solutions

    def _dfs(self, x: int, y: int, visited: set, current_path: List[Tuple[int, int]]):
        if (x, y) == self.end:
            self.solutions.append(list(current_path))
            return
        visited.add((x, y))
        current_path.append((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.size and 0 <= ny < self.size and 
                self.maze[nx][ny] != '+' and (nx, ny) not in visited):
                self._dfs(nx, ny, visited, current_path)
        visited.remove((x, y))
        current_path.pop()

@app.post("/solve_maze", response_model=Dict[str, List[Tuple[int, int]]])
def solve_maze(maze_input: MazeInput):
    solver = MazeSolver(maze_input.size, maze_input.maze_string)
    solutions = solver.solve()
    return {"solutions": solutions}
