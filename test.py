from tkinter import *

root = Tk()

def key(event):
    print("pressed", repr(event.char))

root.bind('<Key>', key)

root.mainloop()