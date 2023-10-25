import tkinter as tk
from EPuzzle import *
import random

class PuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Game")

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.RIGHT, padx=10)

        button_width = 10

        self.solve_button = tk.Button(self.button_frame, text="Solve", command=self.solve_puzzle, width=button_width)
        self.shuffle_button = tk.Button(self.button_frame, text="Reset", command=self.reset_board, width=button_width)

        self.shuffle_button.pack(side=tk.TOP, padx=10, pady=10)
        self.solve_button.pack(side=tk.TOP, padx=10, pady=10)

        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="white")
        self.canvas.pack()

        # Initialize the 8-Puzzle problem and its initial state
        self.problem = EightPuzzleProblem(initial_state=(3, 1, 2, 6, 0, 8, 7, 5, 4), goal_state=(0, 1, 2, 3, 4, 5, 6, 7, 8))
        self.state = self.problem.initial
        self.empty_cell = self.state.index(0)

        self.draw_board()

    def shuffle_board(self):
        # Shuffle the board to create a new puzzle
        state_list = list(self.state)
        random.shuffle(state_list)
        self.state = tuple(state_list)
        self.empty_cell = self.state.index(0)
        self.draw_board()

    def reset_board(self):
        # Khôi phục trạng thái ban đầu của bảng
        self.state = self.problem.initial
        self.empty_cell = self.state.index(0)
        self.draw_board()
    def draw_board(self):
        # Draw the puzzle board based on the current state
        self.canvas.delete("all")
        for i in range(9):
            if self.state[i] != 0:
                row, col = divmod(i, 3)
                self.canvas.create_rectangle(col * 100, row * 100, (col + 1) * 100, (row + 1) * 100, fill="lightgray")
                self.canvas.create_text(col * 100 + 50, row * 100 + 50, text=str(self.state[i]))

    def show_success_message(self):
        success_window = tk.Toplevel(self.root)
        success_window.title("Success")
        success_label = tk.Label(success_window, text="Puzzle solved successfully!", font=("Helvetica", 16))
        success_label.pack(padx=20, pady=20)

    def solve_puzzle(self):
        # Solve the puzzle using the provided algorithm (EightPuzzleSolving)
        solving = EightPuzzleSolving(self.problem)
        solution = solving.solution
        self.apply_solution(solution)

    def apply_solution(self, solution):
        # Apply the solution step by step to visualize it
        self.solve_step(solution, 0)

    def solve_step(self, solution, step):
        if step < len(solution):
            action = solution[step]
            if action in self.problem.Action(self.state):
                self.state = self.problem.Result(self.state, action)
                self.draw_board()
                self.root.update()
                if self.state == self.problem.goal:
                    print("Reached the goal state:", self.state)
                    self.show_success_message()  # Hiển thị thông báo
                    return
            self.root.after(1000, self.solve_step, solution, step + 1)

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGame(root)
    root.mainloop()
