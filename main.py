# -*- coding: iso-8859-1 -*-
import os

from GUI import MainGUI


def main():

    for file in os.listdir():
        if file.endswith('.pdf'):
            os.remove('%s' % file)

    root = MainGUI.MainGUI()
    root.geometry("600x400")
    root.mainloop()


if __name__ == "__main__":
    main()

