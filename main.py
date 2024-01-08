import customtkinter as tk
from random import randint
from ships import ships
             
class App(tk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BattleShip")
        self.geometry("850x400")
        tk.set_appearance_mode("dark")
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.score, self.win, self.lose = 0, 0, 0
        self.boxes, self.ship, self.colorful_boxes = [], [], []
        
        self.title_label = tk.CTkLabel(self, text="BattleShip", fg_color="gray30", corner_radius=6)
        self.score_label = tk.CTkLabel(self, text=f"Attempts left: {self.score}", fg_color="gray30", corner_radius=6)
        self.feedback_label = tk.CTkLabel(self, text="")
        self.play_btn = tk.CTkButton(self, text="Play", command=lambda: start_game())
        self.wl_label = tk.CTkLabel(self, text=f"W: {self.win} | L: {self.lose}", fg_color="gray30", corner_radius=6)

        self.title_label.grid(row=0, column=1, padx=10, pady=(10, 0), columnspan = 2, sticky="ew")
        self.score_label.grid(row=0, column=3, padx=10, pady=(10, 0), columnspan = 3, sticky="ew")
        self.feedback_label.grid(row=7, column=0, padx=10, pady=10, columnspan=6, sticky="ew")
        self.play_btn.grid(row=8, column=2, padx=10, pady=10, columnspan=3, sticky="ew")
        self.wl_label.grid(row=8, column=5, padx=10, pady=10, sticky="ew")

        for i in range(5):
            temp = []
            self.row_label = tk.CTkLabel(self, text=i+1, corner_radius=6)
            self.row_label.grid(row=1, column=i+1, padx=5, pady=5, sticky="ew")
            self.column_label = tk.CTkLabel(self, text=chr(i+65), corner_radius=6)
            self.column_label.grid(row=i+2, column=0, padx=5, pady=5, sticky="ew")
            for k in range(5):
                box = tk.CTkButton(self, text="", state="disabled", fg_color="grey", command=lambda box = [i, k]: check_box(box))
                box.grid(row=i+2, column=k+1, padx=5, pady=5, sticky="w")
                temp.append(box)
                if k == 4: self.boxes.append(temp)

        def start_game():
            self.ship, self.colorful_boxes, self.score = [], [], 10
            self.score_label.configure(text=f"Attempts left: {self.score}")
            self.play_btn.configure(state="disabled", fg_color="grey", text="Game Started")
            self.feedback_label.configure(text="", text_color="green")
            enable_boxes()

            random_ship = ships[randint(1, len(ships))]
            for i in range(len(random_ship)):
                self.ship.append(random_ship[i])
            print(self.ship)

        def disable_boxes():
            for i in range(5):
                for k in range(5):
                    if [i, k] not in self.colorful_boxes:
                        self.boxes[i][k].configure(state="disabled", fg_color="grey")

        def enable_boxes():
            for i in range(5):
                for k in range(5):
                    self.boxes[i][k].configure(state="enable", fg_color="#1f6aa5")

        def hit(box):
            self.boxes[box[0]][box[1]].configure(fg_color="green",state="disabled")
            self.feedback_label.configure(text="Hit!", text_color="green")
            self.score_label.configure(text=f"Attempts left: {self.score}")
            self.ship.pop(self.ship.index(box))
            self.colorful_boxes.append(box)

        def miss(box):
            self.feedback_label.configure(text=f"Missed! Try again", text_color="red")
            self.boxes[box[0]][box[1]].configure(fg_color="red",state="disabled")
            self.score_label.configure(text=f"Attempts left: {self.score}")
            self.colorful_boxes.append(box)

        def win():
            disable_boxes()
            self.win += 1
            self.feedback_label.configure(text="You won!", text_color="green")
            self.wl_label.configure(text=f"W: {self.win} | L: {self.lose}")
            self.play_btn.configure(state="enabled", text="Play Again", fg_color="#1f6aa5") 

        def lose():
            disable_boxes()
            self.lose += 1
            self.wl_label.configure(text=f"W: {self.win} | L: {self.lose}")
            remaining_boxes = ""
            for x in self.ship:
                self.boxes[x[0]][x[1]].configure(fg_color="orange")
                remaining_boxes += f"{chr(x[0]+65)}{x[1]+1} "
            self.feedback_label.configure(text=f"You Lose! The ship was in {remaining_boxes}", text_color="red")
            self.play_btn.configure(state="enabled", text="Play Again", fg_color="#1f6aa5")

        def check_box(box):
            self.score -= 1
            if box in self.ship:
                hit(box) 
                if len(self.ship) == 0: win()
                elif self.score == 0: lose()
            elif box not in self.ship: 
                miss(box)
                if self.score == 0: lose()

app = App()
app.mainloop()