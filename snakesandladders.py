import random
import tkinter as tk
from tkinter import messagebox, simpledialog
import time

CELL_SIZE = 60
BOARD_SIZE = 10
BOARD_DIM = CELL_SIZE * BOARD_SIZE

class Player:
    def __init__(self, name, color):
        self.name = name
        self.position = 0
        self.color = color
        self.token = None

    def move(self, steps):
        self.position += steps
        if self.position > 100:
            self.position = 100

    def climb_ladder(self, new_pos):
        self.position = new_pos

    def slide_down(self, new_pos):
        self.position = new_pos

class Board:
    def __init__(self):
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

    def check_snake_or_ladder(self, player):
        pos = player.position
        if pos in self.snakes:
            old = player.position
            player.slide_down(self.snakes[pos])
            return f"Oops, you landed on a snake! Slid from {old} to {player.position}."
        elif pos in self.ladders:
            old = player.position
            player.climb_ladder(self.ladders[pos])
            return f"Congratulations! Climbed a ladder from {old} to {player.position}."
        return ""

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Snakes and Ladders")

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(side=tk.LEFT)

        self.ui_frame = tk.Frame(root)
        self.ui_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        self.canvas = tk.Canvas(self.canvas_frame, width=BOARD_DIM, height=BOARD_DIM, bg="white")
        self.canvas.pack()

        self.status_label = tk.Label(self.ui_frame, text="Welcome to Snakes and Ladders!", font=("Arial", 14), wraplength=200, justify="left")
        self.status_label.pack(pady=10)

        self.roll_button = tk.Button(self.ui_frame, text="Roll Dice", font=("Arial", 12), command=self.play_turn)
        self.roll_button.pack(pady=5)

        self.reset_button = tk.Button(self.ui_frame, text="Reset Game", font=("Arial", 12), command=self.reset_game)
        self.reset_button.pack(pady=5)

        self.quit_button = tk.Button(self.ui_frame, text="End Game", font=("Arial", 12), command=self.root.quit)
        self.quit_button.pack(pady=5)

        self.board = Board()
        name1 = simpledialog.askstring("Player 1", "Enter name for Player 1") or "Player 1"
        name2 = simpledialog.askstring("Player 2", "Enter name for Player 2") or "Player 2"

        self.players = [Player(name1, "red"), Player(name2, "blue")]
        self.turn = 0

        self.draw_board()
        self.draw_snakes_and_ladders()
        self.place_tokens()

    def draw_board(self):
        self.canvas.delete("all")
        ladder_cells = {1, 4, 9, 21, 28, 36, 51, 71, 80}  
        snake_cells = {16, 47, 49, 56, 62, 87, 93, 95, 98}  

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = col * CELL_SIZE
                y1 = (BOARD_SIZE - 1 - row) * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                idx = row * BOARD_SIZE + col + 1 if row % 2 == 0 else (row + 1) * BOARD_SIZE - col

                
                if idx in ladder_cells:
                    fill_color = "lightgreen"
                elif idx in snake_cells:
                    fill_color = "lightcoral"
                elif idx == 1:
                    fill_color = "lightblue"  
                elif idx == 100:
                    fill_color = "gold"
                else:
                    fill_color = "white"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black")
                self.canvas.create_text(x1 + 5, y1 + 5, anchor="nw", text=str(idx), font=("Arial", 10))


    def get_coords(self, position):# essential for determining the position of ;the player tokens,the snakes and ladders and the zigzag functionality is executed without error
        if position == 0:
            return (0, BOARD_DIM - CELL_SIZE)
        row = (position - 1) // BOARD_SIZE
        col = (position - 1) % BOARD_SIZE
        if row % 2 == 1:
            col = BOARD_SIZE - 1 - col
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = (BOARD_SIZE - 1 - row) * CELL_SIZE + CELL_SIZE // 2
        return x, y

    def draw_snakes_and_ladders(self):
        for start, end in self.board.snakes.items():
            x1, y1 = self.get_coords(start)
            x2, y2 = self.get_coords(end)
            self.canvas.create_line(x1, y1, x2, y2, fill="green", width=4, arrow="last", smooth=True)
        for start, end in self.board.ladders.items():
            x1, y1 = self.get_coords(start)
            x2, y2 = self.get_coords(end)
            self.canvas.create_line(x1, y1, x2, y2, fill="orange", width=4, arrow="last", dash=(4, 2), smooth=True)

    def place_tokens(self):
        for player in self.players:
            x, y = self.get_coords(player.position)
            if player.token:
                self.canvas.delete(player.token)
            player.token = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill=player.color)

    def animate_move(self, player, target_pos):
        while player.position < target_pos:
            player.position += 1
            self.place_tokens()
            self.root.update()
            time.sleep(0.1)

    def roll_dice(self):
        return random.randint(1, 6)

    def play_turn(self):
        player = self.players[self.turn]
        dice = self.roll_dice()
        msg = f"{player.name} rolled a {dice}."

        prev_position = player.position
        new_position = min(player.position + dice, 100)
        self.animate_move(player, new_position)
        msg += f" Moved from {prev_position} to {player.position}."

        action_msg = self.board.check_snake_or_ladder(player)
        if action_msg:
            self.place_tokens()
            msg += " " + action_msg

        next_player = self.players[1 - self.turn].name
        self.status_label.config(text=msg + f"\nIt's now {next_player}'s turn.")

        if player.position == 100:
            messagebox.showinfo("Game Over", f"\U0001F3C6 {player.name} wins the game!")
            self.roll_button.config(state="disabled")
            return

        self.turn = 1 - self.turn

    def reset_game(self):
        for player in self.players:
            player.position = 0
        self.turn = 0
        self.draw_board()
        self.draw_snakes_and_ladders()
        self.place_tokens()
        self.roll_button.config(state="normal")
        self.status_label.config(text="Game reset! Ready to play again.")

root = tk.Tk()
game_gui = GameGUI(root)
root.mainloop()
