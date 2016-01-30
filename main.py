# -*- coding: iso-8859-1 -*-
import os

import tkinter as tk
import tkinter.font

from Logger import Logger

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

    logger = Logger.Logger()

    for file in os.listdir():
        if file.endswith('.pdf'):
            try:
                os.remove('%s' % file)
            except:
                logger.log("Couldn't remove %s, file is already in use." % (file))

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

    default_font = tkinter.font.nametofont("TkDefaultFont")
    default_font.configure(size=15)
    root.option_add("*Font", default_font)

    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    #root.overrideredirect(1)
    #root.geometry("%dx%d+0+0" % (w, h))

    root.geometry("%dx%d" % (w, h-100))
    root.mainloop()


if __name__ == "__main__":
    main()

