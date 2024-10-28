import tkinter as tk
from PIL import Image, ImageTk
import random, math

GRID_SIZE = 25
CELL_SIZE = 20

class MedievalDefense(tk.Tk):
    def __init__(self):
        super().__init__() # makes self the master window
        self.random_points = self.get_random_points()
        self.title("Medieval Tower Defense")
        self.geometry(f"{(GRID_SIZE * CELL_SIZE) * 2}x{GRID_SIZE * CELL_SIZE + 200}")

        self.canvas = tk.Canvas(self, width=(GRID_SIZE * CELL_SIZE) * 2, height=GRID_SIZE * CELL_SIZE, bg="green")
        self.canvas.pack() #adds canvas to window
        self.display_grid()
        

    def display_grid(self):
        self.canvas.delete("all")
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE * 2):
                # Middle left gray square
                if y == GRID_SIZE // 2 and x == 0:
                    self.canvas.create_rectangle(
                        (x - 1) * CELL_SIZE, (y - 1) * CELL_SIZE, (x + 2) * CELL_SIZE, (y + 2) * CELL_SIZE, 
                        fill="gray")
                    castle1_location  = (x * CELL_SIZE, (y - 1) * CELL_SIZE + 30)
                # Middle right gray square
                elif y == GRID_SIZE // 2 and x == (GRID_SIZE * 2) - 1:
                    self.canvas.create_rectangle(
                        (x - 1) * CELL_SIZE, (y - 1) * CELL_SIZE, (x + 2) * CELL_SIZE, (y + 2) * CELL_SIZE, 
                        fill="gray")
                    castle2_location = (x * CELL_SIZE + 20, (y - 1) * CELL_SIZE + 30)
                else:
                    self.canvas.create_rectangle(
                        x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, outline="")
        self.random_points = [castle1_location] + self.random_points + [castle2_location]

        for i in range(len(self.random_points)):
            if self.random_points[i] != self.random_points[len(self.random_points) - 1]:
                # print(self.random_points[i], self.random_points[i + 1])
                self.canvas.create_line(self.random_points[i][0], self.random_points[i][1],
                                        self.random_points[i + 1][0], self.random_points[i + 1][1], 
                                        fill="black", width=30)
                    
    def get_random_points(self):
        random_points = []
        width = GRID_SIZE * CELL_SIZE * 2
        height = GRID_SIZE * CELL_SIZE
        for i in range(round(random.random() * 8)):
            point = (math.floor(random.random() * width), math.floor(random.random() * height))
            random_points.append(point)
        random_points.sort()

        return random_points


game = MedievalDefense()
game.mainloop()
