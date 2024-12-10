import tkinter as tk
#tk lets us create a window
from PIL import Image, ImageTk
import random, math
#random package gives us random function
#math package gives us math functions

GRID_SIZE = 25 # All caps mean constant
CELL_SIZE = 20

class TowerDefense(tk.Tk): #class definition, extends the tk.Tk class
    def __init__(self): #class constructor
        super().__init__() #makes self the master window
        self.continue_spawning_enemies = True
        self.title("War Tower Defense")
        self.random_points = self.get_random_points()
        self.empty_spots = self.get_empty_spots_near_path()
        self.geometry(f"{(GRID_SIZE * CELL_SIZE) * 2}x{GRID_SIZE * CELL_SIZE + 200}")

        self.coins = 0
        self.coin_gain = 1
        self.generate_coin_time = 1000 # 1000 milliseconds --> 1 second

        self.canvas = tk.Canvas(self, width=(GRID_SIZE * CELL_SIZE) * 2, 
                                height=GRID_SIZE * CELL_SIZE, 
                                bg="green")

        self.coin_label = tk.Label(self, text=f"Coins: {self.coins}", font=("Helvetica", 16))
        self.coin_label.pack()
        
        self.canvas.pack() #adds canvas to window
        self.display_grid()

        # Initialize lives for each castle
        self.castle_lives = {"castle1": 1000, "castle2": 1000} #Dictionary 
        self.castle1_label = tk.Label(self, text=f"Castle 1 Lives: {self.castle_lives['castle1']}", font=("Helvetica", 16))
        self.castle1_label.pack()
        self.castle2_label = tk.Label(self, text=f"Castle 2 Lives: {self.castle_lives['castle2']}", font=("Helvetica", 16))
        self.castle2_label.pack()

        #Tower Selection 
        self.selected_tower = None
        self.chosen_tower = None
        self.towers = [] #list of towers
        self.range_ids = [] #list of range ids
        self.upgrade_button_ids = [] #list of upgrade button ids
        self.create_tower_buttons() #Function for creating tower buttons

        self.generate_coin_overtime()

        #Basic Units
        self.goblin_image = ImageTk.PhotoImage(Image.open("goblin.png").resize((30,30)))
        self.knight_image = ImageTk.PhotoImage(Image.open("knight.png").resize((30,30)))

        #Medium Units
        self.ogre_image = ImageTk.PhotoImage(Image.open("ogre.png").resize((50,50)))
        self.trebuchet_image = ImageTk.PhotoImage(Image.open("trebuchet.png").resize((50,50)))

        #Large Units
        self.siege_tower_image = ImageTk.PhotoImage(Image.open("siege_tower.png").resize((60,60)))
        self.troll_image = ImageTk.PhotoImage(Image.open("troll.png").resize((60,60)))

        #Boss Units
        self.dragon_image = ImageTk.PhotoImage(Image.open("dragon.png").resize((70,70)))
        self.orc_image = ImageTk.PhotoImage(Image.open("orc.png").resize((70,70)))

        #Enemy and path setup
        self.enemy_spawn_time = 2000
        self.enemies = []   #array
        self.spawn_enemies()

        #Tower Attacks
        self.attack_towers()


    def generate_coin_overtime(self):
        self.coins += self.coin_gain
        self.coin_label.config(text=f"Coins: {self.coins}")
        #after 1 second, run the function again
        self.after(self.generate_coin_time, self.generate_coin_overtime)

    def create_tower_buttons(self):
        #Frame for tower buttons at the bottom of the screen
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        #Button for Archer Tower
        archer_button = tk.Button(button_frame, text="Archer Tower (Cost: 5)", 
                                    command=lambda: self.select_tower("archer"))
        archer_button.pack(side="left", padx=5)

        #Create buttons for cannon tower and wizard tower
        cannon_button = tk.Button(button_frame, text="Cannon Tower (Cost: 10)",
                                    command=lambda: self.select_tower("cannon"))
        cannon_button.pack(side="left", padx=5)

        wizard_button = tk.Button(button_frame, text="Wizard Tower (Cost: 15)",
                                    command=lambda: self.select_tower("wizard"))
        wizard_button.pack(side="left", padx=5)

    def select_tower(self, tower_type):
        """Select a tower type to place on the map"""
        self.selected_tower = tower_type
        print(f"{tower_type.capitalize()} Tower Selected!")

    def display_grid(self): #function definition
        self.canvas.delete("all")
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE * 2):
                if y == GRID_SIZE // 2 and x == 0:
                    self.canvas.create_rectangle((x - 1) * CELL_SIZE, 
                                                 (y - 1) * CELL_SIZE,
                                                 (x + 2) * CELL_SIZE,
                                                 (y + 2) * CELL_SIZE,
                                                 fill="gray",
                                                 tags="castle1")
                    self.castle1_location = (x * CELL_SIZE, (y - 1) * CELL_SIZE + 30)
                elif y == GRID_SIZE // 2 and x == (GRID_SIZE * 2) - 1:
                    self.canvas.create_rectangle((x - 1) * CELL_SIZE, 
                                                 (y - 1) * CELL_SIZE,
                                                 (x + 2) * CELL_SIZE,
                                                 (y + 2) * CELL_SIZE,
                                                 fill="gray",
                                                 tags="castle2")
                    self.castle2_location = (x * CELL_SIZE + 20, (y - 1) * CELL_SIZE + 30)
                else:
                    self.canvas.create_rectangle(x * CELL_SIZE,
                                                 y * CELL_SIZE,
                                                 (x + 1) * CELL_SIZE,
                                                 (y + 1) * CELL_SIZE,
                                                 outline="")
        self.random_points = [self.castle1_location] + self.random_points + [self.castle2_location]

        for i in range(len(self.random_points)):
            if self.random_points[i] != self.random_points[len(self.random_points) - 1]:
                self.canvas.create_line(self.random_points[i][0],
                                        self.random_points[i][1],
                                        self.random_points[i + 1][0],
                                        self.random_points[i + 1][1],
                                        fill="black",
                                        width = 30)
        
        for spot in self.empty_spots:
            x, y = spot
            self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="yellow", outline="black")

        self.canvas.tag_raise("castle1")
        self.canvas.tag_raise("castle2")
                    
    def get_random_points(self):
        random_points = [] #array|list
        width = GRID_SIZE * CELL_SIZE * 2
        height = GRID_SIZE * CELL_SIZE

        #changing the random range with either spawns more lines or less lines
        x_increment = width // (random.randint(10,12))
        current_x = x_increment

        #changing the range would make it straight or curvy
        for _ in range(10):
            y_variation = random.randint(-height //6, height //6)
            point = (current_x, (GRID_SIZE //2) * CELL_SIZE + y_variation)
            random_points.append(point)
            current_x += x_increment

        return random_points

    def get_empty_spots_near_path(self):
        empty_spots = [] #array | list
        for i, (x,y) in enumerate(self.random_points):
            #either above the path or below the path
            if i % 2 == 0:
                empty_spot = (x,y - CELL_SIZE)
            else:
                empty_spot = (x,y + CELL_SIZE)
            empty_spots.append(empty_spot)
        
        #filter to only include spots within the grid boundaries
        empty_spots = [(x,y) for x, y in empty_spots if 0 <= x < GRID_SIZE * CELL_SIZE * 2 and 0 <= y < GRID_SIZE * CELL_SIZE]
        return empty_spots


    def get_coordinates(self, event):
        # Check if the click is on an existing button
        for button in self.upgrade_button_ids:
            button_x = button.winfo_rootx()
            button_y = button.winfo_rooty()
            button_width = button.winfo_width()
            button_height = button.winfo_height()

            # Check if the click falls within the button's dimensions
            if button_x <= event.x_root <= button_x + button_width and \
            button_y <= event.y_root <= button_y + button_height:
                return  # Allow the button's action to trigger without clearing it

        # Clear any previous selections if clicking outside a tower or button
        self.clear_selection()

        # Check if the click is on an existing tower
        for tower in self.towers:
            if (event.x >= tower["x"] - CELL_SIZE // 2 and event.x <= tower["x"] + CELL_SIZE // 2) and \
            (event.y >= tower["y"] - CELL_SIZE // 2 and event.y <= tower["y"] + CELL_SIZE // 2):
                self.chosen_tower = tower

                # Highlight the range of the selected tower
                range_id = self.canvas.create_oval(
                    tower["x"] - tower["range"], 
                    tower["y"] - tower["range"], 
                    tower["x"] + tower["range"],
                    tower["y"] + tower["range"],
                    outline="red", width=1
                )
                self.range_ids.append(range_id)

                # Determine tower type
                tower_name = tower["name"]

                # Create an upgrade button near the tower
                upgrade_button = tk.Button(
                    self, 
                    text=f"Upgrade {tower_name.capitalize()} Tower: {tower["upgrade_cost"]}",
                    command=lambda: self.upgrade_tower(tower)
                )
                upgrade_button.place(x=tower["x"] + 50, y=tower["y"] - 30)  # Position button near the tower
                self.upgrade_button_ids.append(upgrade_button)

                return  # Stop processing since a tower was selected

        # If no tower is selected and the user has coins, place a new tower
        if self.selected_tower and self.coins >= self.get_tower_cost(self.selected_tower):
            for spot in self.empty_spots:
                if (event.x >= spot[0] and event.x <= spot[0] + CELL_SIZE) and \
                (event.y >= spot[1] and event.y <= spot[1] + CELL_SIZE):
                    self.coins -= self.get_tower_cost(self.selected_tower)
                    self.coin_label.config(text=f"Coins: {self.coins}")
                    self.place_tower(spot, self.selected_tower)
                    self.selected_tower = None  # Deselect current tower
                    return

        # If no valid target is clicked, clear the selection
        self.clear_selection()

    def clear_selection(self):
        """Clear the currently selected tower and associated UI elements."""
        self.chosen_tower = None

        # Remove range indicators
        for range_id in self.range_ids:
            self.canvas.delete(range_id)
        self.range_ids.clear()

        # Destroy all upgrade buttons
        for button in self.upgrade_button_ids:
            button.destroy()
        self.upgrade_button_ids.clear()

    def get_tower_cost(self, tower_type):
        return {"archer": 5, "cannon": 10, "wizard": 15}.get(tower_type, 0)

    def upgrade_tower(self, tower):
        if self.coins >= tower["upgrade_cost"]:
            tower["damage"] *= 1.1
            tower["range"] *= 1.1
            tower["attack_speed"] *= 1.1
            self.coins -= tower["upgrade_cost"]
            self.coin_label.config(text=f"Coins: {self.coins}")
            tower["upgrade_cost"] *= 2

    def place_tower(self, spot, tower_type):
        damage = {"archer": 10, "cannon": 20, "wizard": 15}.get(tower_type, 10)
        range_ = {"archer": 200, "cannon": 100, "wizard": 150}.get(tower_type, 200)
        attack_speed = {"archer": 1000, "cannon": 2000, "wizard": 1200}.get(tower_type, 1000)
        color = {"archer": "blue", "cannon": "gray", "wizard": "purple"}.get(tower_type, "blue")
        upgrade_cost = {"archer": 5, "cannon": 10, "wizard": 15}.get(tower_type, 0)

        tower = {
            "x": spot[0] + CELL_SIZE // 2,
            "y": spot[1] + CELL_SIZE // 2,
            "damage": damage,
            "range": range_,
            "attack_speed": attack_speed,
            "target": None,
            "color": color,
            "name": tower_type,
            "upgrade_cost": upgrade_cost
        }
        self.towers.append(tower)

        
        self.canvas.create_rectangle(spot[0], 
                                    spot[1], 
                                    spot[0] + CELL_SIZE, 
                                    spot[1] + CELL_SIZE,
                                    fill=color,
                                    outline="black")

    def attack_towers(self):
        for tower in self.towers:
            if not self.enemies: #if there are no enemies, do nothing
                continue
            for enemy in self.enemies:
                enemy_x, enemy_y = self.canvas.coords(enemy["id"])
                distance = math.sqrt((tower["x"] - enemy_x) ** 2 + (tower["y"] - enemy_y) ** 2) #distance formula
                if distance <= tower["range"]: #find the nearest enemy to shoot
                    enemy["health"] -= tower["damage"]
                    self.update_health_bar(enemy)
                    if enemy["health"] <= 0:
                        self.canvas.delete(enemy["id"])
                        self.canvas.delete(enemy["health_bar"])
                        self.enemies.remove(enemy)

                        if enemy["threat_level"] == "basic":
                            self.coins += 1
                            self.coin_label.config(text=f"Coins: {self.coins}")
                        elif enemy["threat_level"] == "medium": 
                            self.coins += 5
                            self.coin_label.config(text=f"Coins: {self.coins}")
                    break
        self.after(500, self.attack_towers)

        
    def spawn_enemies(self):
        if self.continue_spawning_enemies:
            self.create_enemies(self.castle1_location, target="castle2")
            self.create_enemies(self.castle2_location, target="castle1")
            self.after(self.enemy_spawn_time, self.spawn_enemies) #recursion

    def create_enemies(self, start_location, target):
        image = self.goblin_image if target == "castle1" else self.knight_image
        health = 50 if target == "castle1" else 100
        threat_level = "basic"
        speed = round(random.random() * 10) + 20

        spawn_medium_enemy = math.floor(random.random() * 100)
        spawn_large_enemy = math.floor(random.random() * 100)
        spawn_boss_enemy = math.floor(random.random() * 100)

        if spawn_medium_enemy < 10:
            image = self.ogre_image if target == "castle1" else self.trebuchet_image
            health = 200 if target == "castle1" else 150
            threat_level = "medium"
            speed = 40
        
        if spawn_large_enemy < 5:
            image = self.troll_image if target == "castle1" else self.siege_tower_image
            health = 300 if target == "castle1" else 350
            threat_level = "hard"
            speed = 80

        if spawn_boss_enemy < 2: 
            image = self.orc_image if target == "castle1" else self.dragon_image
            health = 1000 if target == "castle1" else 900
            threat_level = "boss"
            speed = 200

        enemy = {
            "id": self.canvas.create_image(start_location[0], start_location[1], image=image),
            "path_index": 0,
            "path": self.random_points if target == "castle2" else list(reversed(self.random_points)),
            "target": target,
            "health": health,
            "max_health": health,
            "health_bar": None,
            "threat_level": threat_level,
            "speed": speed
        }
        enemy["health_bar"] = self.draw_health_bar(enemy)
        self.enemies.append(enemy)
        self.move_enemy(enemy)

    def draw_health_bar(self, enemy):
        x, y = self.canvas.coords(enemy["id"])
        health_ratio = enemy["health"] / enemy["max_health"]
        return self.canvas.create_rectangle(
            x - 15, y -20, x - 15 + (30 * health_ratio), y - 15,
            fill="red", outline="black"
        )

    def update_health_bar(self,enemy):
        x, y = self.canvas.coords(enemy["id"])
        health_ratio = enemy["health"] / enemy["max_health"]
        self.canvas.coords(
            enemy["health_bar"],
            x - 15, y - 20,
            x - 15 + (30 * health_ratio), y - 15
        )

    def move_enemy(self, enemy):
        if enemy in self.enemies:
            if enemy["path_index"] < len(enemy["path"]) - 1:
                x1, y1 = enemy["path"][enemy["path_index"]]
                x2, y2 = enemy["path"][enemy["path_index"] + 1]
                dx, dy = (x2 - x1) / enemy["speed"], (y2 - y1) / enemy["speed"]

                self.canvas.move(enemy["id"], dx, dy)
                self.canvas.move(enemy["health_bar"], dx, dy)

                current_x, current_y = self.canvas.coords(enemy["id"])

                tolerance = max(12, abs(dx) + abs(dy))

                if abs(current_x - x2) < tolerance and abs(current_y - y2) < tolerance:
                    enemy["path_index"] += 1

                self.after(50, self.move_enemy, enemy)
            else:
                # Enemy has reached the final target (e.g., castle2)
                self.reduce_castle_lives(enemy["target"], enemy["health"])

                # Clean up enemy and health bar
                self.canvas.delete(enemy["id"])
                self.canvas.delete(enemy["health_bar"])
                if enemy in self.enemies:  # Ensure the enemy is still in the list
                    self.enemies.remove(enemy)


    def reduce_castle_lives(self, target_castle, current_enemy_health):
        health_ratio = current_enemy_health / 100
        if target_castle == "castle1":
            self.castle_lives["castle1"] -= (1 * health_ratio) 
            self.castle1_label.config(text=f"Castle 1 Lives: {self.castle_lives["castle1"]:.2f}")
        else:
            self.castle_lives["castle2"] -= (1 * health_ratio) 
            self.castle2_label.config(text=f"Castle 2 Lives: {self.castle_lives["castle2"]:.2f}")

        if self.castle_lives["castle1"] <= 0 or self.castle_lives["castle2"] <= 0:
            print("CALLING GAME OVER")
            self.game_over(target_castle)

    def game_over(self, defeated_castle):
        self.continue_spawning_enemies = False
        self.canvas.delete("all")
        self.canvas.create_text(GRID_SIZE * CELL_SIZE // 2, 
                                GRID_SIZE * CELL_SIZE //2,
                                text=f"Game Over! {defeated_castle.capitalize()} has fallen!",
                                font=("Helvetica", 24), fill="red")
        self.after(3000, self.quit)

game = TowerDefense() #creates a class object
game.bind("<Button-1>", game.get_coordinates)
game.mainloop()