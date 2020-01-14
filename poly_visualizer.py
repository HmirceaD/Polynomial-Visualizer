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


class Step:

    def __init__(self, coef):
        self.xin = None
        self.xout = None
        self.pin = None
        self.pout = None
        self.coef = coef

    def __str__(self):
        return str(self.xin) + " " + str(self.xout) + " " + str(self.pin) + " " + str(self.pout)


for i in range(len(COEFFS)):
    current_steps.append(Step(COEFFS[i]))


def calc_step():

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

        i = i - 1

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

    canvas.delete("tag")

    draw_nums(canvas, app, 350, 150, current_steps[0].pin, current_steps[0].pout,
              current_steps[0].xin, current_steps[0].xout)
    draw_nums(canvas, app, 560, 150, current_steps[1].pin, current_steps[1].pout,
              current_steps[1].xin, current_steps[1].xout)
    draw_nums(canvas, app, 770, 150, current_steps[2].pin, current_steps[2].pout,
              current_steps[2].xin, current_steps[2].xout)
    draw_lists()


def list_to_string(list1):

    string_list = ""

    for elem in list1:

        string_list += str(elem) + " "

    return string_list


def draw_nums(canvas, root, x, y, pin, pout, xin, xout):

    # top left
    if pin is not None:
        canvas.create_text((x - 15, y + 10), tag="tag", text=str(pin), font="Times 16")
    else:
        canvas.create_text((x - 15, y + 10), tag="tag", text="", font="Times 16")

    # top right
    if pout is not None:
        canvas.create_text((x + 115, y + 10), tag="tag", text=str(pout), font="Times 16")
    else:
        canvas.create_text((x + 115, y + 10), tag="tag", text="", font="Times 16")

    # bot left
    if xin is not None:
        canvas.create_text((x - 15, y + 170), tag="tag", text=str(xin), font="Times 16")
    else:
        canvas.create_text((x - 15, y + 170), tag="tag", text="", font="Times 16")

    # bot right
    if xout is not None:
        canvas.create_text((x + 115, y + 170), tag="tag", text=str(xout), font="Times 16")
    else:
        canvas.create_text((x + 115, y + 170), tag="tag", text="", font="Times 16")


def draw_rectangle(canvas, top_frame, P, poly, x, y, hurdle = False):

    canvas.create_rectangle(x, y, x+100, y+200, fill="white", outline='black')

    #ingoing lines
    canvas.create_line(top_frame, x-50, y+20, x, y+20)
    canvas.create_line(top_frame, x-50, y+180, x, y+180)

    #outgoint lines
    canvas.create_line(top_frame, x+100, y+20, x+150, y+20)
    canvas.create_line(top_frame, x+100, y+180, x+150, y+180)

    canvas.create_text(top_frame, x+50, y+30, text = P, font = "Times 20")
    canvas.create_text(top_frame, x+50, y+150, text = str(poly), font = "Times 20")

    if hurdle:
        #top left
        canvas.create_rectangle(x-60, y+30, x-50, y+10, fill="black", outline='black')
        #bot left
        canvas.create_rectangle(x - 60, y + 190, x - 50, y + 170, fill="black", outline='black')
        #top right
        canvas.create_rectangle(x + 150, y + 30, x + 160, y + 10, fill="black", outline='black')
        #bot right
        canvas.create_rectangle(x + 150, y + 190, x + 160, y + 170, fill="black", outline='black')


def on_click():
    calc_step()


def draw_board(app):

    label = tk.Label(app, text = "Polynomial Visualizer (x^2 + 2x + 1)")
    label.pack()

    draw_rectangle(canvas, top_frame, "P0", 1, 350, 150)

    draw_rectangle(canvas, top_frame, "P1", 2, 560, 150, hurdle = True)

    draw_rectangle(canvas, top_frame, "P2", 1, 770, 150)

    #Input Text
    canvas.create_text(top_frame, 100, 50, text="Input", font="Times 20")
    #Output Text
    canvas.create_text(top_frame, 1200, 50, text="Output", font="Times 20")

    draw_lists()

    step_button = tk.Button(bot_frame, text="Advance Algorithm", command=on_click)

    canvas.pack()
    step_button.pack()


def draw_lists():
    # Input Poly
    canvas.create_text(top_frame, 100, 90, text=list_to_string(INPUT_POLY), font="Times 16", tag="tag")
    # Output Poly
    canvas.create_text(top_frame, 1100, 90, text=list_to_string(OUTPUT_POLY), font="Times 16", tag="tag")


def start_visual():

    app.geometry("1500x620")
    app.resizable(0, 0)

    draw_board(app)

    app.mainloop()


if __name__ == "__main__":
    start_visual()