import tkinter as tk

INPUT_POLY = [10,9,8,7,6,5,4,3,2,1]
OUTPUT_POLY = []
COEFFS = [1, 2, 1] # x^2 + 2x + 1

step_counter = 0

init_len = len(INPUT_POLY)

current_steps = []
app = tk.Tk()

top_frame = tk.Frame(app)
top_frame = top_frame.pack(side=tk.TOP)
bot_frame = tk.Frame(app)
bot_frame = bot_frame.pack(side=tk.BOTTOM)

canvas = tk.Canvas(top_frame, bg="white", height=500, width=1300)

final_coords = []

class Step:
    # class that represent a current step for each polynomial coefficient displayed on the board
    def __init__(self, coef):
        self.xin = None
        self.xout = None
        self.pin = None
        self.pout = None
        self.coef = coef

    def __str__(self):
        return str(self.xin) + " " + str(self.xout) + " " + str(self.pin) + " " + str(self.pout)


for i in range(len(COEFFS)):
    current_steps.append(Step(COEFFS[i])) # create coefficients list


def calc_step():
    # CALCULATE THE NEXT STEP OF THE ALGORITHM (GETS CALLED ON BUTTON CLICK)
    if current_steps[len(current_steps) - 1].pout is not None:
        OUTPUT_POLY.append(current_steps[len(current_steps) - 1].pout)

    i = len(current_steps) - 1

    while i > 0:
        current_steps[i].xin = current_steps[i - 1].xout
        current_steps[i].xout = current_steps[i].xin
        current_steps[i].pin = current_steps[i - 1].pout

        if current_steps[i].pin is not None and current_steps[i].xin is not None:
            current_steps[i].pout = current_steps[i].pin * current_steps[i].xin + current_steps[i].coef
        else:
            current_steps[i].pout = None

        i -= 1

    if INPUT_POLY:

        aux = INPUT_POLY.pop()
        current_steps[0].xin = aux
        current_steps[0].xout = aux
        current_steps[0].pin = 0
        current_steps[0].pout = current_steps[0].pin * current_steps[0].xin + current_steps[0].coef

    else:
        current_steps[0].xin = None
        current_steps[0].xout = None
        current_steps[0].pin = None
        current_steps[0].pout = None

    canvas.delete("DELETEME")

    cont = 0
    for i in COEFFS:
        draw_nums(canvas, app, final_coords[cont][0], final_coords[cont][1],
                  current_steps[cont].pin,current_steps[cont].pout,
              current_steps[cont].xin, current_steps[cont].xout)
        cont += 1

    draw_lists()


def list_to_string(list1):

    string_list = ""

    for elem in list1:

        string_list += str(elem) + " "

    return string_list


def draw_nums(canvas, root, x, y, pin, pout, xin, xout):

    # top left pin value
    if pin is not None:
        canvas.create_text((x - 15, y + 10), tag="DELETEME", text=str(pin), font="Times 16")
    else:
        canvas.create_text((x - 15, y + 10), tag="DELETEME", text="", font="Times 16")

    # top right pout value
    if pout is not None:
        canvas.create_text((x + 115, y + 10), tag="DELETEME", text=str(pout), font="Times 16")
    else:
        canvas.create_text((x + 115, y + 10), tag="DELETEME", text="", font="Times 16")

    # bot left input value
    if xin is not None:
        canvas.create_text((x - 15, y + 170), tag="DELETEME", text=str(xin), font="Times 16")
    else:
        canvas.create_text((x - 15, y + 170), tag="DELETEME", text="", font="Times 16")

    # bot right output value
    if xout is not None:
        canvas.create_text((x + 115, y + 170), tag="DELETEME", text=str(xout), font="Times 16")
    else:
        canvas.create_text((x + 115, y + 170), tag="DELETEME", text="", font="Times 16")


def draw_rectangle(canvas, top_frame, P, poly, x, y, hurdle = False):

    canvas.create_rectangle(x, y, x+100, y+200, fill="white", outline='black')

    #ingoing lines
    canvas.create_line(top_frame, x-50, y+20, x, y+20)
    canvas.create_line(top_frame, x-50, y+180, x, y+180)

    #outgoint lines
    canvas.create_line(top_frame, x+100, y+20, x+150, y+20)
    canvas.create_line(top_frame, x+100, y+180, x+150, y+180)

    # Draw P and polynomial value
    canvas.create_text(top_frame, x+50, y+30, text = P, font = "Times 20")
    canvas.create_text(top_frame, x+50, y+150, text = str(poly), font = "Times 20")

    if hurdle:
        #top left black square
        canvas.create_rectangle(x-60, y+30, x-50, y+10, fill="black", outline='black')
        #bot left black square
        canvas.create_rectangle(x - 60, y + 190, x - 50, y + 170, fill="black", outline='black')
        #top right black square
        canvas.create_rectangle(x + 150, y + 30, x + 160, y + 10, fill="black", outline='black')
        #bot right black square
        canvas.create_rectangle(x + 150, y + 190, x + 160, y + 170, fill="black", outline='black')


def on_click():
    calc_step()


def draw_board(app):

    label = tk.Label(app, text = "Polynomial Visualizer (x^2 + 2x + 1)")
    label.pack()

    init_coords = [350, 150]
    cont = 0
    for i in COEFFS:
        if i == COEFFS[0] or i == COEFFS[-1]:
            isHurdle = False
        else:
            isHurdle = True

        draw_rectangle(canvas, top_frame, "P"+str(cont),COEFFS[cont], init_coords[0], init_coords[1], hurdle=isHurdle)
        final_coords.append((init_coords[0], init_coords[1]))
        init_coords[0] += 210
        cont += 1

    #Input Text
    canvas.create_text(top_frame, 100, 50, text="Input", font="Times 20")
    #Output Text
    canvas.create_text(top_frame, 1200, 50, text="Output", font="Times 20")

    draw_lists()

    step_button = tk.Button(bot_frame, text="Next Step", command=on_click)

    canvas.pack()
    step_button.pack()


def draw_lists():
    # Input Values
    canvas.create_text(top_frame, 100, 90, text=list_to_string(INPUT_POLY), font="Times 16", tag="DELETEME")
    # Output Values
    canvas.create_text(top_frame, 1100, 90, text=list_to_string(OUTPUT_POLY), font="Times 16", tag="DELETEME")


def start_visual():

    app.geometry("1500x620")
    app.resizable(0, 0)

    draw_board(app)

    app.mainloop()


if __name__ == "__main__":
    start_visual()