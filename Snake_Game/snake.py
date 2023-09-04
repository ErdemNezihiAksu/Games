import tkinter as tk
from tkinter import messagebox
import random

SIZE = 25
LENGTH = 2
WIDTH = 900
HEIGHT = 700
SPEED = 25
BAIT_COLOUR = 'red'
SNAKE_HEAD_COLOR = "#9932CC"
SNAKE_BODY_COLOR = "#68228B" 
OUTLINE = 'black'

class Snake:
    def __init__(self):
        self.coords = []
        self.squares = []
        self.length = LENGTH

        for i in range(LENGTH-1,-1,-1):
            self.coords.append([i*SIZE,0])
        for x , y in self.coords:
            square = canvas.create_rectangle(x,y,x+SIZE,y+SIZE, fill=SNAKE_HEAD_COLOR,outline=OUTLINE)
            self.squares.append(square)
        canvas.itemconfig(self.squares[1], fill = SNAKE_BODY_COLOR)    


class Bait:
    def __init__(self):
        x = random.randint(0,(WIDTH-SIZE*LENGTH)/SIZE - 1) * 25 + SIZE*LENGTH
        y = random.randint(0,(HEIGHT - SIZE)/SIZE -1) * 25 + SIZE
        self.coords = [x,y]
        canvas.create_oval(x,y,x+SIZE,y+SIZE, fill= BAIT_COLOUR,outline=OUTLINE, tags=("bait",))

    def eaten(self):
        global snake
        x_s, y_s = snake.coords[0]
        x_b, y_b = self.coords
        if x_s == x_b and y_s == y_b:
            return True
        return False

    def random_place(self):
        global snake
        while True:
            flag = True
            x_b , y_b = random.randint(0,WIDTH/SIZE - 1) * 25, random.randint(0,HEIGHT/SIZE -1) * 25
            for i in range(snake.length):
                x_s , y_s = snake.coords[i]
                if x_b == x_s and y_b == y_s:
                    flag = False
                    break
            if flag == True:
                break
        canvas.delete("bait")
        self.coords = [x_b,y_b]
        canvas.create_oval(x_b,y_b,x_b+SIZE,y_b+SIZE, fill= BAIT_COLOUR,outline=OUTLINE, tags=("bait",))


def change_dir(dir):
    global direction, pause, key_pressed
    if dir == "up" and direction != 'down':
        direction = 'up'
        pause = False
    elif dir == 'down' and direction != 'up':
        direction = 'down'
        pause = False
    elif dir == 'left' and direction != 'right':
        direction = 'left'
        pause = False
    elif dir == 'right' and direction != 'left':
        direction = 'right'
        pause = False


def game_over():
    global snake
    x,y = snake.coords[0]
    for i in range(4,snake.length):
        x_i,y_i = snake.coords[i]
        if x == x_i and y == y_i:
            return True
    if x < 0 or y < 0 or x + SIZE > WIDTH or y + SIZE > HEIGHT:
        return True
    if snake.length == (WIDTH/SIZE) * (HEIGHT/SIZE):
        return True
    return False

def move():
    global direction,snake
    if pause is True:
        pass
    else:
        if direction != 'none':
            if direction == 'up':
                x , y= snake.coords[0][0], snake.coords[0][1] - SPEED
            elif direction == 'down':
                x, y = snake.coords[0][0], snake.coords[0][1] + SPEED
            elif direction == 'left':
                x, y = snake.coords[0][0] - SPEED, snake.coords[0][1]
            elif direction == 'right':
                x, y = snake.coords[0][0] + SPEED, snake.coords[0][1]
            snake.coords.insert(0,[x,y])
            if game_over():
                messagebox.showinfo(message="GAME OVER")
                exit()
            if  not bait.eaten():
                del snake.coords[-1]
                canvas.delete(snake.squares[-1])
                del snake.squares[-1]
            else:
                snake.length += 1
                bait.random_place()
            snake.squares.insert(0,canvas.create_rectangle(x,y,x+SIZE,y+SIZE,fill= SNAKE_HEAD_COLOR, outline= OUTLINE))
            canvas.itemconfig(snake.squares[1], fill = SNAKE_BODY_COLOR)
            
    canvas.after(80, move)

def Pause():
    global pause
    if pause == True:
        print("False")
        pause = False
    else:
        print("True")
        pause = True

root = tk.Tk()
root.title("SNAKE GAME")
root.resizable(False,False)
s_w = root.winfo_screenwidth()
s_h = root.winfo_screenheight()
x = (s_w - WIDTH) // 2
y = (s_h - HEIGHT) // 2
root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
canvas = tk.Canvas(root,bg="black")
canvas.pack(fill="both",expand=True)
snake = Snake()
bait = Bait()
direction = 'none'
pause = False
root.bind("<Left>", lambda _ : change_dir("left"))
root.bind("<Right>", lambda _ : change_dir("right"))
root.bind("<Up>", lambda _ : change_dir("up"))
root.bind("<Down>", lambda _ : change_dir("down"))
root.bind("w", lambda _ : change_dir("up"))
root.bind("a", lambda _ : change_dir("left"))
root.bind("d", lambda _ : change_dir("right"))
root.bind("s", lambda _ :change_dir("down"))
root.bind("p", lambda _ : Pause())

move()
root.mainloop()