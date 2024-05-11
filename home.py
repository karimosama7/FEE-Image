import customtkinter as ctk
import subprocess


def run_program1():
    subprocess.Popen(["python", "first.py"])


def run_program2():
    subprocess.Popen(["python", "second.py"])


def run_program3():
    subprocess.Popen(["python", "third.py"])


def run_program4():
    subprocess.Popen(["python", "fourth.py"])


app = ctk.CTk()
frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill="both", expand=True)
ctk.set_appearance_mode("system")

ctk.set_default_color_theme("green")

button1 = ctk.CTkButton(master=frame, text="Program 1", command=run_program1)
button1.pack(pady=12, padx=10)
button2 = ctk.CTkButton(master=frame, text="Program 2", command=run_program2)
button2.pack(pady=12, padx=10)
button3 = ctk.CTkButton(master=frame, text="Program 3", command=run_program3)
button3.pack(pady=12, padx=10)
button4 = ctk.CTkButton(master=frame, text="Program 4", command=run_program4)
button4.pack(pady=12, padx=10)

app.geometry("400x300")
app.title("FEE IMAGE")
app.resizable(width=False, height=False)
app.mainloop()
