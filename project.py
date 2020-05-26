# Author: sivaguru
# Created: 20 May,2020, 8:30 PM
# Email: sivaguru.n.s@gmail.com
# Escape from falling objects by moving around

from tkinter import *
import random
import time

#Globals
car_move_factor = 2
obs_move_factor = 2
sco_move_factor = 100

def main():
    game_instance = objectEscape()
    game_instance.mainloop()

#Class objectEscape for creating instance and executing
class objectEscape():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        # Creating Tinkter instance
        self.window = Tk()

        # Setting window title
        self.window.title('Escape from falling obstruction')

        # Getting Screen size to calculate canvas
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # Calculating Canvas dimensions
        self.canvas_width = self.screen_width // 5
        self.canvas_height = self.screen_height - 200

        # Calculating Grid dimensions
        self.grid_width = self.canvas_width // 3
        self.grid_height = (self.canvas_height * 80)//1000

        # Calculating car dimensions
        self.car_width = (self.grid_width * 90)//100
        self.car_height = (self.grid_height * 90)//100

        #Creating canvas
        self.canvas = Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg='white')

        # Positions the window in the center of the page.
        self.window.geometry("+{}+{}".format(int(self.screen_width / 2 - self.canvas_width / 2), int(self.screen_height / 2 - self.canvas_height / 2)))
        self.canvas.pack()

        # Binding arrow keys for handling user inputs from user in form of clicks
        self.window.bind('<Left>', self.move_left)
        self.window.bind('<Right>', self.move_right)
        self.window.bind('<Up>', self.move_up)
        self.window.bind('<Down>', self.move_down)

        # Misc variables and objects used in this class
        self.current_pos = 1
        self.car_movement_direction = 1
        self.score    = 0
        self.obstacles = []
        self.car = None
        self.label = None
        self.final_label = None
        self.obs_delay = 10//obs_move_factor

        # Initialize the board
        self.initialize_board()

    # mainloop to run the program infinite
    def mainloop(self):
        # Setting the delay factor
        time_factor = self.score // sco_move_factor
        timer_val   = 0.25
        while self.move_obs_vertical():
            if(time_factor < (self.score//sco_move_factor)):
                time_factor = self.score//sco_move_factor
                timer_val -= 0.05
            self.draw_obstacles()
            self.update_score()
            self.canvas.update()
            time.sleep(timer_val)

        # End of game
        final_score = "Game Over!!! Final score: " + str(self.score)
        self.canvas.itemconfig(self.final_label, text=final_score)
        self.window.unbind('<Left>')
        self.window.unbind('<Right>')
        self.window.unbind('<Up>')
        self.window.unbind('<Down>')
        self.window.mainloop()

    # Initialize the board
    def initialize_board(self):
        # Setting frame in the top
        self.canvas.create_rectangle(0, 0,  self.canvas_width, self.canvas_height*0.1, fill="black")

        # Setting frame in the bottom
        self.canvas.create_rectangle(0, self.canvas_height - (self.canvas_height * 0.1), self.canvas_width, self.canvas_height, fill="black")

        # Setting score panel
        score = "Score: " + str(self.score)
        self.label = self.canvas.create_text(self.canvas_width//2 - len(score)//2, (((self.canvas_height * 100 - self.canvas_height * 10)/100) + ((self.canvas_height * 10)/200)),text=score, fill="white", font="Times 20 italic bold")

        # Setting title panel
        final_score = "Escape from falling objects!!!"
        self.final_label = self.canvas.create_text(self.canvas_width//2 - len(final_score)//2, (self.canvas_height * 10)//200, text=final_score, fill="white", font="Times 20 italic bold")

        # Create a Car
        self.create_car()

    # ------------------------------------------------------------------
    # Car Functions:
    # ------------------------------------------------------------------
    # Create a Car
    def create_car(self):
        x1 = self.current_pos * self.grid_width + 7
        y1 = (self.canvas_height * 90)//100 - self.grid_height
        x2 = x1 + self.car_width
        y2 = y1 + self.car_height
        self.car = self.canvas.create_rectangle(x1, y1, x2, y2, fill = "red")

    # Move the Car in horizontal position
    def move_car(self):
        coords = self.canvas.coords(self.car)
        x1 = self.car_movement_direction * self.car_width // car_move_factor
        y1 = 0

        result_pos = coords[0] + x1

        if (result_pos <= 0):
            x1 = coords[0] * -1
        elif (result_pos + self.car_width) > self.canvas_width:
            x1 = self.canvas_width - coords[2]

        self.canvas.move(self.car, x1, y1)

    # Move the Car in vertical position
    def move_car_vertical(self):
        coords = self.canvas.coords(self.car)
        y1 = self.car_movement_direction * self.car_height// car_move_factor
        x1 = 0
        result_pos = coords[1] + y1

        if (result_pos <= ((self.canvas_height*10)//100)):
            y1 = (coords[1] - ((self.canvas_height*10)//100)) * -1
        elif (result_pos + self.car_height) > (self.canvas_height - ((self.canvas_height * 10)//100)):
            y1 = (self.canvas_height - ((self.canvas_height * 10)//100)) - coords[3]

        self.canvas.move(self.car, x1, y1)

    # ------------------------------------------------------------------
    #  Obstruction Functions:
    # ------------------------------------------------------------------
    # Move the obstruction objects in vertical position
    def move_obs_vertical(self):
        for item in self.obstacles:
            car_coords = self.canvas.coords(self.car)
            coords = self.canvas.coords(item)
            height = (coords[3] - coords[1])
            if (coords[3] + self.grid_height//2) < (self.canvas_height - (self.canvas_height*10)//100):
                y1 = height // obs_move_factor
                x1 = 0
                self.canvas.move(item, x1, y1)
            else:
                self.obstacles.remove(item)
                self.canvas.delete(item)
                self.score += 10

            check = self.canvas.find_overlapping(car_coords[0], car_coords[1], car_coords[2], car_coords[3])

            if item in check:
                return False

        return True

    # Creating objects with random color and random size and random position
    def draw_obstacles(self):
        color = random.choice(["blue", "green", "yellow", "white", "black", "purple", "brown", "orange", "gray", "pink", "tan", "chartreuse"])

        ran = random.randint(0, 5)
        ran_size    = random.randint(20, (self.canvas_width * 1)//3)
        ran_x_coord = random.randint(0, self.canvas_width - ran_size - 1)
        initial_y  = (self.canvas_width * 10)//100 + 10 + (self.grid_height//2)

        if self.obs_delay >= 5:
            self.obs_delay = 0
            if ran == 0:
                self.obstacles.append(self.canvas.create_rectangle(ran_x_coord, initial_y, ran_x_coord + ran_size, initial_y + self.grid_height, fill = color))
            elif ran == 2:
                self.obstacles.append(self.canvas.create_oval(ran_x_coord, initial_y, ran_x_coord + self.grid_height, initial_y + self.grid_height, fill = color))
            else:
                self.obstacles.append(self.canvas.create_rectangle(ran_x_coord, initial_y, ran_x_coord + self.grid_height, initial_y + self.grid_height, fill = color))
        else:
            self.obs_delay += 1

    # ------------------------------------------------------------------
    #  Utility Functions:
    # ------------------------------------------------------------------
    def update_score(self):
        text = "Score: " + str(self.score)
        self.canvas.itemconfig(self.label, text=text)

    def move_left(self, event):
        print('Moving left')
        if self.current_pos != 0:
            self.car_movement_direction = -1
            self.current_pos -= 1

        self.move_car()

    def move_right(self, event):
        print('Moving right')
        if self.current_pos != 2:
            self.car_movement_direction = 1
            self.current_pos += 1

        self.move_car()

    def move_up(self, event):
        print('Moving up')
        if self.current_pos != 0:
            self.car_movement_direction = -1
            self.current_pos -= 1

        self.move_car_vertical()

    def move_down(self, event):
        if self.current_pos != 2:
            self.car_movement_direction = 1
            self.current_pos += 1

        self.move_car_vertical()

if __name__ == '__main__':
    main()