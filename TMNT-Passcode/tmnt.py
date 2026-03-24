import tkinter as tk

from PIL import Image, ImageTk
import cv2

root = tk.Tk()

mode = "sewer"

cursor_visible = True

import tkinter.font as tkFont
pixel_font = tkFont.Font(family="Pixel Operator SC", size=16, weight="bold")

import tkinter.font as tkFont
button_font = tkFont.Font(family="Early Gameboy", size=20)

root.title('TMNT')
root.geometry("540x720")
root.resizable(width=False, height=False)

cap = cv2.VideoCapture("assets/sewer.mp4")

bg_label = tk.Label(root)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

password = "16926261"

def update_video():
    global cap, mode

    ret, frame = cap.read()

    if not ret:
        if mode == "sewer":
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        elif mode == "unlocked":
            cap.release()
            cap = cv2.VideoCapture("assets/unlocked.mp4")
            mode = "unlocked"
        elif mode == "unlocked":
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return update_video()

    frame = cv2.resize(frame, (540, 720), interpolation=cv2.INTER_NEAREST)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    img = ImageTk.PhotoImage(Image.fromarray(frame))
    bg_label.configure(image=img)
    bg_label.image = img

    root.after(30, update_video)

def open_keypad():
    print("opening keypad")
    keypad_popup.place(relx=0.5, rely=0.5, anchor="center")

def quit_keypad():
    print("closing keypad")
    keypad_popup.place_forget()
    keypad_popup.update()

entered_code = ""
is_showing_message = False

def check_password():
    global entered_code, is_showing_message
    global cap
    global mode

    if entered_code == password:
        display.configure(text="Turtle Power!")

        cap.release()
        cap = cv2.VideoCapture("assets/open2.mp4")
        mode = "unlocked"


        keypad_popup.place_forget()
        button_label.place_forget()

    else:
        is_showing_message = True
        display.configure(text="Skill Issue lol")
        print("skill issue lol")
        root.after(1500, reset_code)

def press (num):
    global entered_code
    if len(entered_code) <8:
     entered_code += str(num)
    print("entered code: ", entered_code)

def reset_code():
    global entered_code, is_showing_message
    entered_code = ""
    display.config(text="")
    is_showing_message = False

def delete_last():
    global entered_code

    entered_code = entered_code[:-1]
    display.config(text="  ".join(entered_code))

def blink_cursor():
    global cursor_visible

    if is_showing_message:
        root.after(500, blink_cursor)
        return

    if len(entered_code) >= 8:
        display.config(text="  ".join(entered_code))
    else:
        if cursor_visible:
            display.config(text="  ".join(entered_code) + " _")
        else:
            display.config(text="  ".join(entered_code) + "  ")

        cursor_visible = not cursor_visible

    root.after(500, blink_cursor)

img = Image.open("assets/button.png")
img = img.resize((40,70))

button_img = ImageTk.PhotoImage(img)

button_label = tk.Button(root, image=button_img, bd=0, highlightthickness=0, command=open_keypad)
button_label.place(x=422, y=252)

keypad_popup = tk.Frame(root, bg="black", width=300, height=420, relief="flat")

pad = Image.open("assets/pad.png")
pad = pad.resize((300,420))

pad_img = ImageTk.PhotoImage(pad)
pad_label = tk.Label(keypad_popup, image=pad_img, bd=0, highlightthickness=0)
pad_label.place(x=0, y=0)

keys = Image.open("assets/pad key.png")
keys_img = ImageTk.PhotoImage(keys)

red = Image.open("assets/red.png")
red_img = ImageTk.PhotoImage(red)

display = tk.Label(
    keypad_popup,
    text="",
    font=pixel_font,
    fg="dark green",
    bg="lime",

)
display.place(x=68, y=87)
blink_cursor()

positions = {
    1: (56,190), 2: (126,190), 3: (197,190),
    4: (56,240), 5: (126,240), 6: (197,240),
    7: (56,288), 8: (126,288), 9: (197,288),
    0: (126,335)
}

for num, (x,y) in positions.items():
    btn = tk.Button(
        keypad_popup,
        command=lambda n=num: press(n),
        bd=0,
        highlightthickness=0,
        relief="flat",
        borderwidth=0,
        activebackground = "light green",
        image=keys_img,
        text=str(num),
        compound="center",
        font=button_font,
        fg="lightgoldenrodyellow",
        bg="olivedrab",

    )
    btn.place(x=x, y=y, width=51, height=38)
    btn.image = keys_img

quit_button = tk.Button(keypad_popup, text="QUIT", command=quit_keypad, bg="maroon", fg="white", activebackground="indianred", relief="flat", font=(pixel_font), image=red_img, bd=0, highlightthickness=0, compound="center", width=52)
quit_button.place(x=54, y=335)
quit_button.image = red_img

enter_button = tk.Button(keypad_popup, text="---->", command=check_password,bg="olivedrab", fg="white", relief="flat", font=(pixel_font), image=keys_img, bd=0, highlightthickness=0, compound="center", activebackground="light green")
enter_button.place(x=197, y=335)
enter_button.image = keys_img

delete_button = tk.Button(keypad_popup, text="DEL", command=delete_last, font=pixel_font, bg="dimgray")
delete_button.place(x=197, y=160, width=51, height=22)













update_video()
root.mainloop()
