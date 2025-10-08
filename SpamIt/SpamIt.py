#Libraries
import time
import pyautogui
from tkinter import *
import threading
import os
import sys

# Root window setup
root = Tk()
root.geometry("320x360")
root.title("Spammer")
root.resizable(False, False)

try:
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    logo_png_path = os.path.join(application_path, "logo.png")
    logo_ico_path = os.path.join(application_path, "logo.ico")

    if os.path.exists(logo_ico_path):
        root.iconbitmap(logo_ico_path)
    elif os.path.exists(logo_png_path):
        logo_img = PhotoImage(file=logo_png_path)
        root.iconphoto(False, logo_img)
except:
    pass

#Object
stop_flag = False

# Functions
def start_thread():
    global stop_flag
    stop_flag = False
    threading.Thread(target=start_spam).start()

def stop_spam():
    global stop_flag
    stop_flag = True
    debugger_label.config(text="Stopping...")

def start_spam():
    global stop_flag

    try:
        sleep_time = int(sleep_entry.get())
        spam_count = int(count_entry.get())
        delay_ms = float(delay_entry.get())
        
        if spam_count < 0:
            raise ValueError
        if delay_ms < 100:
            debugger_label.config(text="Delay must be >= 100 ms")
            return
            
    except ValueError:
        debugger_label.config(text="Please enter valid numbers")
        return

    spam_text = spam_text_entry.get().strip()
    if not spam_text:
        debugger_label.config(text="Please enter spam text")
        return

    debugger_label.config(text=f"Waiting {sleep_time}s before start...")
    root.update()
    for _ in range(sleep_time):
        if stop_flag:
            debugger_label.config(text="Stopped before start")
            return
        time.sleep(1)

    delay_sec = delay_ms / 1000
    surround_enter = surround_var.get()

    i = 0
    while not stop_flag and (spam_count == 0 or i < spam_count):
        debugger_label.config(text=f"Spamming ({i+1 if spam_count!=0 else '∞'}/{spam_count if spam_count!=0 else '∞'})")
        root.update()

        if surround_enter:
            pyautogui.press('enter')
        pyautogui.typewrite(spam_text)
        pyautogui.press('enter')

        end_time = time.time() + delay_sec
        while time.time() < end_time and not stop_flag:
            time.sleep(0.01)

        i += 1

    debugger_label.config(text="Stopped" if stop_flag else "Done")

def apply_dark_theme(widget):
    widget.config(bg="#2f2f2f")
    for child in widget.winfo_children():
        cls = child.winfo_class()
        try:
            if cls == "Label":
                child.config(bg="#2f2f2f", fg="#ffffff")
            elif cls == "Button":
                child.config(bg="#3a3a3a", fg="#ffffff", activebackground="#505050")
            elif cls == "Entry":
                child.config(bg="#4a4a4a", fg="#ffffff", insertbackground="#ffffff")
            elif cls == "Checkbutton":
                child.config(bg="#2f2f2f", fg="#ffffff", selectcolor="#2f2f2f")
        except:
            pass
        apply_dark_theme(child)

# Widgets
start_button = Button(root, text="Start", command=start_thread)
start_button.pack(pady=5)
stop_button = Button(root, text="Stop", command=stop_spam)
stop_button.pack(pady=5)
spam_text_label = Label(root, text="Enter spam text:")
spam_text_label.pack()
spam_text_entry = Entry(root)
spam_text_entry.pack(pady=5)
count_label = Label(root, text="Enter spam count (0 for infinite):")
count_label.pack()
count_entry = Entry(root)
count_entry.pack(pady=5)
delay_label = Label(root, text="Enter delay (ms, >=100):")
delay_label.pack()
delay_entry = Entry(root)
delay_entry.pack(pady=5)
sleep_label = Label(root, text="Enter sleep time before start (s):")
sleep_label.pack()
sleep_entry = Entry(root)
sleep_entry.pack(pady=5)
surround_var = IntVar()
surround_checkbox = Checkbutton(root, text="Surround Enter (Enter, spam, Enter)", variable=surround_var)
surround_checkbox.pack(pady=5)
debugger_label = Label(root, text="Debugger")
debugger_label.pack(pady=5)

#Start Application
apply_dark_theme(root)
root.mainloop()