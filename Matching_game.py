import tkinter as tk
import random
import time

class MatchingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Matching Letter Game")

        self.letters = []
        self.selected_tiles = []
        self.score = 0
        self.start_time = None

        # Setup UI
        self.play_button = tk.Button(self.root, text="Play", command=self.start_game, font=('Arial', 16))
        self.play_button.pack(pady=10)

        self.score_label = tk.Label(self.root, text="Score: 0", font=('Arial', 16))
        self.score_label.pack()

        self.timer_label = tk.Label(self.root, text="Time: 0 seconds", font=('Arial', 16))
        self.timer_label.pack()

        self.restart_button = tk.Button(self.root, text="Restart", command=self.reset_game, font=('Arial', 16), state=tk.DISABLED)
        self.restart_button.pack(pady=10)

        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(pady=20)

        self.tiles = []

    def start_game(self):
        self.play_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.NORMAL)
        self.score_label.config(text="Score: 0")
        self.timer_label.config(text="Time: 0 seconds")
        self.score = 0
        self.start_time = None
        self.create_game_board()

    def create_game_board(self):
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        self.tiles = []
        uppercase_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")[:8]
        lowercase_letters = list("abcdefghijklmnopqrstuvwxyz")[:8]
        self.letters = uppercase_letters + lowercase_letters
        random.shuffle(self.letters)

        for i, letter in enumerate(self.letters):
            tile_button = tk.Button(self.game_frame, text=" ", width=5, height=3, font=('Arial', 24), bg="blue", fg="white", command=lambda i=i: self.tile_click(i))
            tile_button.grid(row=i // 4, column=i % 4, padx=10, pady=10)
            self.tiles.append((tile_button, letter))

    def tile_click(self, index):
        if not self.start_time:
            self.start_time = time.time()
            self.update_timer()

        button, letter = self.tiles[index]

        if button['text'] == " ":
            button.config(text=letter, bg="red")
            self.selected_tiles.append((button, letter, index))

            if len(self.selected_tiles) == 2:
                self.root.after(1000, self.check_match)

    def check_match(self):
        if len(self.selected_tiles) == 2:
            first_button, first_letter, first_index = self.selected_tiles[0]
            second_button, second_letter, second_index = self.selected_tiles[1]

            if first_letter.lower() == second_letter.lower() and first_index != second_index:
                first_button.config(bg="green", state=tk.DISABLED)
                second_button.config(bg="green", state=tk.DISABLED)
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
            else:
                first_button.config(text=" ", bg="blue")
                second_button.config(text=" ", bg="blue")

            self.selected_tiles = []

            if self.score == 8:
                elapsed_time = time.time() - self.start_time
                self.timer_label.config(text=f"Time: {int(elapsed_time)} seconds")
                tk.messagebox.showinfo("Congratulations", f"You won the game in {int(elapsed_time)} seconds!")
                self.reset_game()

    def update_timer(self):
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=f"Time: {int(elapsed_time)} seconds")
            self.root.after(1000, self.update_timer)

    def reset_game(self):
        self.play_button.config(state=tk.NORMAL)
        self.restart_button.config(state=tk.DISABLED)
        self.selected_tiles = []
        self.score = 0
        self.start_time = None
        self.score_label.config(text="Score: 0")
        self.timer_label.config(text="Time: 0 seconds")
        for widget in self.game_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = MatchingGame(root)
    root.mainloop()
