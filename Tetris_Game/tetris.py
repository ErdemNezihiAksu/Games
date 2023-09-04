import tkinter as tk
from PIL import Image
from tkinter import messagebox
import random
import copy
import time

F_G_WIDTH = 420
F_G_HEIGHT = 720
F_I_WIDTH = 250
F_I_HEIGHT = 450
F_O_WIDTH = 250
F_O_HEIGHT = 200
S_WIDTH =  800
S_HEIGHT = 800
SPEED = SIZE =  30
DT = 150 #miliseconds
SHAPES = (("I","orange"), ("J","green"), ("L","blue"), ("O","red"), ("S","gold"), ("Z","light blue"), ("T","purple"))
START_COORDS = {
    "I": [[150,-SIZE],[150 + SIZE,-SIZE],[150 + 2*SIZE ,-SIZE],[150 + 3*SIZE,-SIZE]],
    "J": [[180,-SIZE],[180 + SIZE,-SIZE],[180 + SIZE,-(2*SIZE)],[180+SIZE,-(3*SIZE)]],
    "L": [[180,-(3*SIZE)],[180,-(2*SIZE)],[180,-SIZE],[180 + SIZE,-SIZE]],
    "O": [[180,-(2*SIZE)],[180,-SIZE],[180+SIZE,-(2*SIZE)],[180 + SIZE,-SIZE]],
    "S": [[180,-(3*SIZE)],[180,-(2*SIZE)],[180 + SIZE,-(2*SIZE)],[180 + SIZE,-SIZE]],
    "Z": [[180,-SIZE],[180,-(2*SIZE)],[180 + SIZE,-(2*SIZE)],[180 + SIZE ,-(3*SIZE)]],
    "T": [[150,-SIZE],[150 + SIZE,-(2*SIZE)],[150 + SIZE,-SIZE],[150 + 2*SIZE ,-SIZE]]
}
current_shapes = []
rot = 0
rot_flag = False
direction = ""
highest_y_coord = F_G_HEIGHT
score = 0
lines = 0

############  SHAPE CLASS AND FUNCTIONS  ##############
class Shape():
    def __init__(self, shape:tuple,coords:list):
        self.coords = copy.deepcopy(coords)
        self.initial_coords = copy.deepcopy(coords)
        self.squares = []
        self.shape , self.color = shape

        canvas_object.delete("shape")
        for x,y in self.coords:
            square = canvas_game.create_rectangle(x,y,x+SIZE,y+SIZE, fill = self.color, tags= ("shape",))
            canvas_object.create_rectangle(x-80,y+140, x-80 + SIZE, y+140 + SIZE, fill = self.color, tags = ("shape",))
            self.squares.append(square)


def create_object():
    obj = SHAPES[random.randint(0,6)]
    #obj = SHAPES[0]
    if obj[0] == "I":
        shape = Shape(obj, START_COORDS["I"])
    elif obj[0] == "J":
        shape = Shape(obj,START_COORDS["J"])
    elif obj[0] == "L":
        shape = Shape(obj, START_COORDS["L"])
    elif obj[0] == "O":
        shape = Shape(obj,START_COORDS["O"])
    elif obj[0] == "S":
        shape = Shape(obj,START_COORDS["S"])
    elif obj[0] == 'Z':
        shape = Shape(obj,START_COORDS["Z"])
    elif obj[0] == "T":
        shape = Shape(obj,START_COORDS["T"])
    return shape


##############  MOTION AND ROTATION FUNCTIONS  ##############

# Clockwise and anti-clockwise rotations
def Rotate(shape:Shape):
    global rot_flag, rot
    temp_coords = copy.deepcopy(shape.coords)
    if shape.shape == "J":
        if rot == 90 or rot == 270:
            temp_coords[1][0] = shape.initial_coords[1][0] - SIZE
            temp_coords[1][1] = shape.initial_coords[1][1] - SIZE
            temp_coords[3][0] = shape.initial_coords[3][0] + SIZE
            temp_coords[3][1] = shape.initial_coords[3][1] + SIZE
            if rot == 90:
                temp_coords[0][1] = shape.initial_coords[0][1] - 2*SIZE
                temp_coords[0][0] = shape.initial_coords[0][0]
            else:
                temp_coords[0][0] = shape.initial_coords[0][0] + 2*SIZE
                temp_coords[0][1] = shape.initial_coords[0][1]
        else:
            temp_coords = copy.deepcopy(shape.initial_coords)
            if rot == 180:
                temp_coords[0][0] += 2*SIZE
                temp_coords[0][1] -= 2*SIZE
    elif shape.shape == "I":
        if rot == 90 or rot == 270:
            temp_coords[0][0] = shape.initial_coords[0][0] + 2*SIZE
            temp_coords[0][1] = shape.initial_coords[0][1] - 2*SIZE
            temp_coords[1][0] = shape.initial_coords[1][0] + SIZE
            temp_coords[1][1] = shape.initial_coords[1][1] - SIZE
            temp_coords[3][0] = shape.initial_coords[3][0] - SIZE
            temp_coords[3][1] = shape.initial_coords[3][1] + SIZE
        else:
            temp_coords = copy.deepcopy(shape.initial_coords)

    elif shape.shape == "L":
        if rot == 90 or rot == 270:
            temp_coords[0][0] = shape.initial_coords[0][0] + SIZE
            temp_coords[0][1] = shape.initial_coords[0][1] + SIZE
            temp_coords[2][0] = shape.initial_coords[2][0] - SIZE
            temp_coords[2][1] = shape.initial_coords[2][1] - SIZE
            if rot == 90:
                temp_coords[3][0] = shape.initial_coords[3][0] - 2*SIZE
                temp_coords[3][1] = shape.initial_coords[3][1]
            else:
                temp_coords[3][1] = shape.initial_coords[3][1] - 2*SIZE
                temp_coords[3][0] = shape.initial_coords[3][0]
        else:
            temp_coords = copy.deepcopy(shape.initial_coords)
            if rot == 180:
                temp_coords[3][0] -= 2*SIZE
                temp_coords[3][1] -= 2*SIZE

    elif shape.shape == "S":
        if rot == 90 or rot == 270:
            temp_coords[0][0] = shape.initial_coords[0][0] + 2*SIZE
            temp_coords[3][1] = shape.initial_coords[3][1] - 2*SIZE
        else:
            temp_coords = copy.deepcopy(shape.initial_coords)

    elif shape.shape == "Z":
        if rot == 90 or rot == 270:
            temp_coords[0][1] = shape.initial_coords[0][1] - 2*SIZE
            temp_coords[1][0] = shape.initial_coords[1][0] + 2*SIZE
        else:
            temp_coords = copy.deepcopy(shape.initial_coords)

    elif shape.shape == "T":
        if rot == 90 or rot == 270:
            temp_coords[1][0] = shape.initial_coords[1][0]
            temp_coords[1][1] = shape.initial_coords[1][1]
            if rot == 90:
                temp_coords[0][0] = shape.initial_coords[0][0] + SIZE
                temp_coords[0][1] = shape.initial_coords[0][1] + SIZE
            else:
                temp_coords[3][0] = shape.initial_coords[3][0] - SIZE
                temp_coords[3][1] = shape.initial_coords[3][1] + SIZE
        else:
            temp_coords = copy.deepcopy(shape.initial_coords)
            if rot == 180:
                temp_coords[1][1] = shape.initial_coords[1][1] + 2*SIZE
    
    #Here we check if the rotation can actually be made
    flag = False
    for x,y in temp_coords:
        if x == F_G_WIDTH or x < 0 or y == F_G_HEIGHT:
            flag = True
            break
        for i in current_shapes[:-1]:
            for x_i, y_i in i.coords:
                if x == x_i and y == y_i - SIZE:
                    flag = True
                    break
            if flag == True:
                break
        if flag == True:
            break
    if flag == False:
        shape.coords = copy.deepcopy(temp_coords)
    rot_flag = False


def change_direction(dir):
    global direction
    if dir == "left":
        direction = "left"
    else:
        direction = "right"

def change_rot(Q):
    global rot,rot_flag
    if Q == "+":
        if rot == 270:
            rot = 0
        else:
            rot += 90
    elif Q == "-" :
        if rot == 0:
            rot = 270
        else:
            rot -= 90
    rot_flag = True


def Direct(shape:Shape):
    global direction
    if direction == "right":
        for i in shape.coords:
            if i[0] == F_G_WIDTH - SIZE:
                direction = ""
                return
            for x in current_shapes[:-1]:
                for x_i, y_i in x.coords:
                    if i[0] == x_i - SIZE and i[1] == y_i - SIZE:
                        direction = ""
                        return
        for i , x in zip(shape.coords, shape.initial_coords):
            i[0] += SIZE
            x[0] += SIZE
            canvas_game.delete(shape.squares[0])
            del shape.squares[0]
            shape.squares.append(canvas_game.create_rectangle(i[0],i[1],i[0]+SIZE,i[1]+SIZE,fill=shape.color,tags=("shape,")))
    else:
        for i in shape.coords:
            if i[0] == 0:
                direction = ""
                return
            for x in current_shapes[:-1]:
                for x_i, y_i in x.coords:
                    if i[0] == x_i + SIZE and i[1] == y_i - SIZE:
                        direction = ""
                        return
        for i , x in zip(shape.coords, shape.initial_coords):
            i[0] -= SIZE
            x[0] -= SIZE
            canvas_game.delete(shape.squares[0])
            del shape.squares[0]
            shape.squares.append(canvas_game.create_rectangle(i[0],i[1],i[0]+SIZE,i[1]+SIZE,fill=shape.color,tags=("shape,")))

    direction = ""

###########   GAMPE PLAY FUNCTIONS   ###########

#checks if a row is completed
def check_row(row):
    shape_ids = []
    shape_count = 0
    for x in range(0, F_G_WIDTH, SIZE):
        id = canvas_game.find_overlapping(x+SIZE//4,row+SIZE//4,x+SIZE//4+1,row+SIZE//4+1)
        if id:
            shape_ids.append(id)
            shape_count += 1
    if shape_count == F_G_WIDTH  // SIZE:
        return shape_ids
    return []
    
#returns all the rows that are competed if there are any
def check_tetris():
    global highest_y_coord, current_shapes
    rows = []
    for y in range(F_G_HEIGHT - SIZE, highest_y_coord - SIZE, -SIZE):
        shape_ids = check_row(y)
        if shape_ids:
            combined = [y, shape_ids]
            rows.append(combined)
    if rows:
        return rows

#if a row is completed, that line wll be deleted and the shapes above will be shifted down
def delete_line():
    global current_shapes,txt_var_line,txt_var_score,score,lines
    rows = []
    rows = check_tetris()
    #deletion starts
    if rows:
        animation(rows)
        for i in rows:
            for square in i[1]:
                for shape in current_shapes:
                    if square[0] in shape.squares:
                        shape.squares.remove(square[0])
                        x, _ ,_, _ = canvas_game.coords(square[0])
                        canvas_game.delete(square)
                        shape.coords.remove([x,i[0]])
                        if not shape.coords:
                            current_shapes.remove(shape)
                        break
        #shifting starts
        for shape in current_shapes:
            while True:
                for n,i in enumerate(shape.coords):
                    if i[1] > rows[0][0]:
                        continue
                    i[1] += SIZE
                    canvas_game.delete(shape.squares[n])
                    del shape.squares[n]
                    square = canvas_game.create_rectangle(i[0],i[1], i[0]+SIZE, i[1]+SIZE, fill=shape.color, tags = ("shape,"))
                    shape.squares.insert(n,square)
                if check_landing(shape):
                    break
        lines += len(rows)
        score += 200*len(rows)
        txt_var_line.set(str(lines))
        txt_var_score.set(str(score))

def check_landing(shape:Shape):
    global current_shapes
    for x,y in shape.coords:
        if y == F_G_HEIGHT - SIZE:
            return True
        for i in current_shapes:
            if i is shape:
                continue
            for x_i, y_i in i.coords:
                if x == x_i and y == y_i - SIZE:
                    return True
    return False

def game_over(shape:Shape):
    for i in shape.coords:
        if i[1] < 0:
            return True
    return False

def Tick(shape: Shape):
    global highest_y_coord,rot,direction
    if not check_landing(shape):
        if rot_flag == True:
            Rotate(shape)
        if direction != "":
            Direct(shape)
        for i , x in zip(shape.coords, shape.initial_coords):
            i[1] += SIZE
            x[1] += SIZE
            canvas_game.delete(shape.squares[0])
            del shape.squares[0]
            square = canvas_game.create_rectangle(i[0],i[1], i[0]+SIZE, i[1]+SIZE, fill=shape.color, tags = ("shape,"))
            shape.squares.append(square)
        canvas_game.after(DT,Tick,shape)

    elif game_over(shape):
        messagebox.showwarning(message= "THANKS FOR PLAYING")
        exit()

    else:
        rot = 0
        y = F_G_HEIGHT
        for i in shape.coords:
            if i[1] < y:
                y = i[1]
        if y < highest_y_coord :
            highest_y_coord = y
        delete_line()
        canvas_game.after(DT,Game_Play)

def Game_Play():
    global current_shapes
    shape = create_object()
    current_shapes.append(shape)
    Tick(shape)

############ ANIMATIONS ##################

def GIF(count):
    gif_lbl.configure(image= frames[count])
    count += 1
    if count == frame_count:
        count = 0
    root.after(100,GIF,count)

def animation(rows):
    for count in range(6):
        for row in rows:
            for square in row[1]:
                if count == 0:
                    canvas_game.itemconfig(square, fill = "white")
                elif count == 1:
                    canvas_game.itemconfig(square, fill = "tomato2")
                elif count == 2:
                    canvas_game.itemconfig(square, fill = "medium orchid")
                elif count == 3:
                    canvas_game.itemconfig(square, fill = "firebrick2")
                elif count == 4:
                    canvas_game.itemconfig(square, fill = "OliveDrab1")
                else:
                    canvas_game.itemconfig(square, fill = "cyan")
        root.update()
        count += 1
        time.sleep(0.001)

############ GUI HANDLING #################

root = tk.Tk()
root.title("TETRIS")
root.config(bg="gray")
s_w = root.winfo_screenwidth()
s_h = root.winfo_screenheight()
x = (s_w - S_WIDTH) // 2
y = (s_h - S_HEIGHT) // 2 - 25
root.geometry(f"{S_WIDTH}x{S_HEIGHT}+{x}+{y}")
root.resizable(width=False,height=False)

with Image.open("resized.gif") as img:
    frame_count = img.n_frames
frames = [tk.PhotoImage(file= "resized.gif", format= f"gif -index {i}") for i in range(frame_count)]
gif_lbl = tk.Label(root, image="")
gif_lbl.pack(fill="both",expand=True)

frame_game = tk.Frame(root, width=F_G_WIDTH, height= F_G_HEIGHT)
frame_game.place(x=50, y= 30)
frame_object = tk.Frame(root,width=F_O_WIDTH, height=F_O_HEIGHT)
frame_object.place(x = 500 , y= 50)
frame_info = tk.Frame(root, width= F_I_WIDTH, height= F_I_HEIGHT, bg="white")
frame_info.place(x = 500, y = 300)

canvas_game = tk.Canvas(frame_game,bg="black", width= F_G_WIDTH, height= F_G_HEIGHT)
canvas_game.pack(fill="both",expand=True)
for y in range(0,F_G_HEIGHT,SIZE):
    canvas_game.create_line(0 ,y, F_G_WIDTH,y, fill="gray")
for x in range(0,F_G_WIDTH,SIZE):
    canvas_game.create_line(x,0,x,F_G_HEIGHT,fill="gray")
canvas_object = tk.Canvas(frame_object,bg="black",width=250, height=200)
canvas_object.pack(fill="both",expand=True)

txt_var_score = tk.StringVar()
txt_var_score.set("")
txt_var_line = tk.StringVar()
txt_var_line.set("")
label_score = tk.Label(frame_info,text = "SCORE :", font=("Arial", 25), background="white", fg="black")
lbl_score_text = tk.Label(frame_info, font=("Arial", 25),background="white", fg="black", textvariable= txt_var_score)
label_line = tk.Label(frame_info,text = "LINES :", font=("Arial", 25), background="white", fg="black")
lbl_line_txt = tk.Label(frame_info, font=("Arial", 25), background="white", fg="black", textvariable= txt_var_line)
label_score.place(x = 10, y = 300)
label_line.place(x = 10, y = 400)
lbl_line_txt.place(x =140, y = 400)
lbl_score_text.place(x = 140, y = 300)

lbl_gameplay = tk.Label(frame_info,font=("Arial", 20), background="white", fg="blue",text="GAME PLAY")
lbl_w = tk.Label(frame_info,font=("Arial", 17), background="white", fg="red",text="W - UP   : Turn clockwise")
lbl_s = tk.Label(frame_info,font=("Arial", 17), background="white", fg="red",text="S - DOWN : Counter-clockwise")
lbl_a = tk.Label(frame_info,font=("Arial", 17), background="white", fg="red",text="A - LEFT : Go left")
lbl_d = tk.Label(frame_info,font=("Arial", 17), background="white", fg="red",text="D - RIGHT : Go right")
lbl_gameplay.place(x = 10, y = 10)
lbl_w.place(x = 10, y = 60)
lbl_s.place(x = 10, y = 90)
lbl_a.place(x = 10, y = 120)
lbl_d.place(x = 10, y = 150)

root.bind("<Down>", lambda _ : change_rot("-"))
root.bind("s", lambda _ : change_rot("-"))
root.bind("<Up>", lambda _ : change_rot("+"))
root.bind("w", lambda _ : change_rot("+"))
root.bind("<Left>", lambda _ : change_direction("left"))
root.bind("a", lambda _ : change_direction("left"))
root.bind("<Right>", lambda _ : change_direction("right"))
root.bind("d", lambda _ : change_direction("right"))

GIF(0)
Game_Play()

root.mainloop()