import tkinter as tk
import math
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI")
        self.root.configure(bg="#1e1e2f")

        self.board = [" " for _ in range(9)]
        self.buttons = []
        self.difficulty = None

        self.show_start_screen()

    # ---------------- START SCREEN ---------------- #
    def show_start_screen(self):
        self.clear_screen()

        title = tk.Label(self.root, text="Select Difficulty",
                         font=("Arial", 20, "bold"),
                         bg="#1e1e2f", fg="white")
        title.pack(pady=20)

        tk.Button(self.root, text="Easy",
                  font=("Arial", 14),
                  bg="#2ed573", fg="white",
                  width=15,
                  command=lambda: self.start_game("easy")).pack(pady=10)

        tk.Button(self.root, text="Medium",
                  font=("Arial", 14),
                  bg="#ffa502", fg="white",
                  width=15,
                  command=lambda: self.start_game("medium")).pack(pady=10)

        tk.Button(self.root, text="Hard",
                  font=("Arial", 14),
                  bg="#ff4757", fg="white",
                  width=15,
                  command=lambda: self.start_game("hard")).pack(pady=10)

    # ---------------- GAME UI ---------------- #
    def start_game(self, level):
        self.difficulty = level
        self.board = [" " for _ in range(9)]
        self.clear_screen()
        self.create_board()

    def create_board(self):
        title = tk.Label(self.root, text=f"Difficulty: {self.difficulty.upper()}",
                         font=("Arial", 16, "bold"),
                         bg="#1e1e2f", fg="white")
        title.grid(row=0, column=0, columnspan=3, pady=10)

        for i in range(9):
            btn = tk.Button(self.root, text=" ",
                            font=("Arial", 32, "bold"),
                            width=5, height=2,
                            bg="#2d2d44", fg="white",
                            activebackground="#444466",
                            command=lambda i=i: self.human_move(i))
            btn.grid(row=(i//3)+1, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        restart = tk.Button(self.root, text="Change Difficulty",
                            font=("Arial", 12),
                            bg="#57606f", fg="white",
                            command=self.show_start_screen)
        restart.grid(row=4, column=0, columnspan=3, pady=10)

    # ---------------- HUMAN MOVE ---------------- #
    def human_move(self, index):
        if self.board[index] == " ":
            self.board[index] = "X"
            self.buttons[index].config(text="X", fg="#00ffcc")

            if self.check_winner("X"):
                self.end_game("You Win!")
                return
            if self.is_draw():
                self.end_game("Draw!")
                return

            self.ai_move()

    # ---------------- AI MOVE ---------------- #
    def ai_move(self):
        if self.difficulty == "easy":
            move = random.choice([i for i in range(9) if self.board[i] == " "])

        elif self.difficulty == "medium":
            if random.random() < 0.5:
                move = random.choice([i for i in range(9) if self.board[i] == " "])
            else:
                move = self.best_move()

        else:  # Hard
            move = self.best_move()

        self.board[move] = "O"
        self.buttons[move].config(text="O", fg="#ffcc00")

        if self.check_winner("O"):
            self.end_game("AI Wins!")
        elif self.is_draw():
            self.end_game("Draw!")

    # ---------------- MINIMAX ---------------- #
    def best_move(self):
        best_score = -math.inf
        move = None

        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                score = self.minimax(0, False, -math.inf, math.inf)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    move = i
        return move

    def minimax(self, depth, is_max, alpha, beta):
        if self.check_winner("O"):
            return 10 - depth
        if self.check_winner("X"):
            return depth - 10
        if self.is_draw():
            return 0

        if is_max:
            best = -math.inf
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = "O"
                    val = self.minimax(depth+1, False, alpha, beta)
                    self.board[i] = " "
                    best = max(best, val)
                    alpha = max(alpha, val)
                    if beta <= alpha:
                        break
            return best
        else:
            best = math.inf
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = "X"
                    val = self.minimax(depth+1, True, alpha, beta)
                    self.board[i] = " "
                    best = min(best, val)
                    beta = min(beta, val)
                    if beta <= alpha:
                        break
            return best

    # ---------------- UTILITIES ---------------- #
    def check_winner(self, player):
        wins = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        return any(all(self.board[i] == player for i in combo) for combo in wins)

    def is_draw(self):
        return " " not in self.board

    def end_game(self, message):
        for btn in self.buttons:
            btn.config(state="disabled")
        result = tk.Label(self.root, text=message,
                          font=("Arial", 16, "bold"),
                          bg="#1e1e2f", fg="#ff6b6b")
        result.grid(row=5, column=0, columnspan=3)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.buttons = []

# Run
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x500")
    game = TicTacToe(root)
    root.mainloop()