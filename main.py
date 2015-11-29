# -*- coding: iso-8859-1 -*-
import os

import tkinter as tk

import passwords

from GUI import MainGUI
from backup import backup
from tkinter import Menu

def doNothing():
    toplevel = tk.Toplevel()
    toplevel.wm_title("Generera emaillista")

    checkButtonValA = tk.IntVar()
    check = tk.Checkbutton(toplevel, text="A", variable=checkButtonValA)
    check.toggle()
    check.grid(row=1)

    checkButtonValB = tk.IntVar()
    check = tk.Checkbutton(toplevel, text="B", variable=checkButtonValB)
    check.toggle()
    check.grid(row=1, column=1)

    button = tk.Button(toplevel, text="Go", command=doNothing)
    button.grid(row=1, column=2)


def main():

    for file in os.listdir():
        if file.endswith('.pdf'):
            os.remove('%s' % file)

    backup()

    root = MainGUI.MainGUI()

    #menu = Menu(root)
    #root.config(menu=menu)

    #subMenu = Menu(menu)
    #menu.add_cascade(label="File", menu=subMenu)
    #
    # subMenu.add_command(label="Start", command=doNothing)

    #editMent = Menu(menu)
    #menu.add_cascade(label="Edit", menu=editMent)
    #editMent.add_command(label="Uppdatera lösenord", command=doNothing)

    root.geometry("800x600")
    root.mainloop()


if __name__ == "__main__":
    main()

