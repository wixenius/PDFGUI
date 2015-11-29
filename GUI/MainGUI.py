# -*- coding: iso-8859-1 -*-

import tkinter as tk
import tkinter.messagebox
import webbrowser
import time

from Emailer.sendEmail import sendEmail
from tkinter import simpledialog, ttk

from FTP.parseInfo import parseInfo, returnCSVEmail, returnData
from FTP.ftpDownAndUpload import downloadFile
from helpFunc import listToCommaSeperatedString, updateFile_PaidUnpaid, updateFile_Email
from PDFCreater.creator import creatPermissionPDF, creatPermissionCompilation
from passwords import FILENAME, EMAIL

lMonths = ['Januari', 'Februari', 'Mars', 'April',
           'Maj', 'Juni', 'Juli', 'Augusti', 'September',
           'Oktober', 'November', 'December']

class MainGUI(tk.Tk):

    def __init__(self, *args, **kwargs):

        self.root = tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        tk.Tk.wm_title(self, "Parkeringstillstånd")

        for F in (StartPage, InfoPage, MarkAsPaidPage, GenerateEmailList):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def returnInstance(self, cont):

        return self.frames[cont]

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, master, controller):
        self.month = ''
        self.controller = controller

        tk.Frame.__init__(self, master)

        label1 = tk.Label(self, text="Lägenhetsnummer")
        self.entry1 = tk.Entry(self)

        label1.grid(row=0, sticky=tk.W)
        self.entry1.grid(row=0, column=1)

        button1 = tk.Button(self, text="Go", command=self.checkApartmentNumber)
        button1.grid(row=0, column=4)

        button2 = tk.Button(self, text="Generera emaillista", command=self.generateEmailList)
        button2.grid(row=1)

        button3 = tk.Button(self, text="Generara sammanställning", command=self.generateCompilation)
        button3.grid(row=2)

    def generateCompilation(self):

        self.toplevel = tk.Toplevel(self)
        self.toplevel.wm_title("Generera sammanställning")

        label1 = tk.Label(self.toplevel, text="År")
        self.entry_year = tk.Entry(self.toplevel)
        self.entry_year.insert(tk.END, time.strftime("%Y"))

        label1.grid(row=0, sticky=tk.W)
        self.entry_year.grid(row=0, column=1)

        label2 = tk.Label(self.toplevel, text="Månad")
        self.box_value_month = tk.StringVar()
        self.box_value_month.set(lMonths[int(time.strftime("%m"))-1])
        comboBox = ttk.Combobox(self.toplevel, values=lMonths, textvariable=self.box_value_month, state='readonly')

        label2.grid(row=1, sticky=tk.W)
        comboBox.grid(row=1, column=1)

        self.checkButton_SendToMediator = tk.IntVar()
        checkBut = tk.Checkbutton(self.toplevel, text="Skicka med email", variable=self.checkButton_SendToMediator)
        checkBut.grid(row=2)

        buttonGenerate = tk.Button(self.toplevel, text="Generara", command=self.generateCompilationPDF)
        buttonGenerate.grid(row=2, column=3)


    def generateCompilationPDF(self):

        year = self.entry_year.get()
        month = self.box_value_month.get()

        if not (year).isdigit():
            tk.messagebox.showinfo('Fel', 'Året måste vara ett nummer!')
            self.generateCompilation()
            return

        year_month = "%d_%s" % (int(year), lMonths.index(month)+1)

        self.toplevel.destroy()

        downloadFile(FILENAME)
        data = returnData()

        d = {}

        for apartmentNumber in data.keys():
            for paidPermission in data[apartmentNumber]['paid']:
                if data[apartmentNumber]['paid'][paidPermission] == year_month:
                    l = d.setdefault(apartmentNumber, [])
                    l.append(int(paidPermission))

        fileName = creatPermissionCompilation(d, year_month, year, month)

        if self.checkButton_SendToMediator.get():
            subject = 'BRF Bällstabacken 4 Parkeringstillstånd sammanställning %s %s' % (month, year)
            sendEmail(fileName, EMAIL['MEDIATOR'], subject, '')
        else:
            webbrowser.open_new(r'%s' % fileName)

    def generateEmailList(self):

        self.toplevel = tk.Toplevel(self)
        self.toplevel.wm_title("Generera emaillista")

        self.checkButtonValA = tk.IntVar()
        check = tk.Checkbutton(self.toplevel, text="A", variable=self.checkButtonValA)
        check.toggle()
        check.grid(row=1)

        self.checkButtonValB = tk.IntVar()
        check = tk.Checkbutton(self.toplevel, text="B", variable=self.checkButtonValB)
        check.toggle()
        check.grid(row=1, column=1)

        button = tk.Button(self.toplevel, text="Go", command=self.appendToClipboard)
        button.grid(row=1, column=2)

    def appendToClipboard(self):

        downloadFile(FILENAME)

        sCSVEmail = ''

        if self.checkButtonValA.get() and self.checkButtonValB.get():
            sCSVEmail = returnCSVEmail()

        elif self.checkButtonValA.get():
            sCSVEmail = returnCSVEmail(specificHouse='A')

        elif self.checkButtonValB.get():
            sCSVEmail = returnCSVEmail(specificHouse='B')

        r = tk.Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(sCSVEmail)

        self.toplevel.destroy()

    def checkApartmentNumber(self):

        downloadFile(FILENAME)

        info = self.entry1.get()

        parsedInfo = parseInfo(info)

        if parsedInfo:

            InfoPageInstance = self.controller.returnInstance(InfoPage)
            InfoPage.generateFirstPage(InfoPageInstance, self.entry1.get(), parsedInfo['paid'], parsedInfo['unpaid'], parsedInfo['email'])

            self.controller.show_frame(InfoPage)

        else:
            tk.messagebox.showinfo('Fel', 'Felaktigt lägenhetsnummer!')

class InfoPage(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        self.list = []
        self.lPaid = []
        self.dPaid_dates = {}
        self.lUnpaid = []
        self.lEmail = []

        tk.Frame.__init__(self, parent)
        self.apartmentNumber = tk.StringVar()
        self.label = tk.Label(self, text=self.apartmentNumber.get())
        self.label.grid(row=0, column=0)

        label1 = tk.Label(self, text="Betalade:")
        label2 = tk.Label(self, text="Obetalade:")
        label3 = tk.Label(self, text="Email1:")
        label4 = tk.Label(self, text="Email2:")

        label1.grid(row=1)
        label2.grid(row=2)
        label3.grid(row=3)
        label4.grid(row=4)

        button1 = tk.Button(self, text="Tillbaka", command=self.returnToHomePage)
        button1.grid(row=6, column=20)

        button2 = tk.Button(self, text="Utfärda nya tillstånd", command=self.generatePDF)
        button2.grid(row=6, column=0)

        button3 = tk.Button(self, text="Ändra", command=lambda: self.updateEmail(0))
        button3.grid(row=3, column=2)

        button4 = tk.Button(self, text="Ändra", command=lambda: self.updateEmail(1))
        button4.grid(row=4, column=2)

        self.checkButtonVal = tk.IntVar()

        check = tk.Checkbutton(self, text="Skicka med email", variable=self.checkButtonVal)
        check.grid(row=7)

    def generatePDF(self):
        try:
            i = max(self.lPaid + self.lUnpaid)
        except:
            i = 0

        downloadFile(FILENAME)

        numberOfPermissions = simpledialog.askinteger('Antal', 'Hur många tillstånd?')

        while numberOfPermissions != None and numberOfPermissions % 3 != 0:
            tk.messagebox.showinfo('Fel', 'Måste vara jämt delbart med tre!')
            numberOfPermissions = simpledialog.askinteger('Antal', 'Hur många tillstånd?')

        if numberOfPermissions:
            self.updateListOfUnpaid(i, numberOfPermissions)
            fileName = creatPermissionPDF(self.apartmentNumber, i+1, numberOfPermissions)

            updateFile_PaidUnpaid(self.apartmentNumber, self.dPaid_dates, self.lUnpaid)

            if self.checkButtonVal.get():
                sendEmail(fileName, self.lEmail, 'Parkeringstillstånd', 'Här kommer dina parkeringstillstånd!')

            else:
                webbrowser.open_new(r'%s' % fileName)

    def updateEmail(self, idx):

        downloadFile(FILENAME)

        updatedEmail = simpledialog.askstring('Email', 'Email')

        if updatedEmail:

            try:
                self.lEmail[idx] = updatedEmail
            except:
                self.lEmail.append(updatedEmail)

            if idx == 0:
                self.email1.config(text=self.lEmail[idx])

            if idx == 1:
                self.email2.config(text=self.lEmail[idx])

            updateFile_Email(self.apartmentNumber, self.lEmail)


    def updateListOfUnpaid(self, i, numberOfPermissions):
        i += 1

        for x in range(i,i+numberOfPermissions):
            self.lUnpaid.append(x)

        self.list.clear()
        self.lPaid.sort()
        self.lUnpaid.sort()

        self.labelPaid.config(text=listToCommaSeperatedString(self.lPaid))
        self.list.append(self.labelPaid)
        self.labelUnpaid.config(text=listToCommaSeperatedString(self.lUnpaid))
        self.list.append(self.labelUnpaid)

    def returnToHomePage(self):
        self.email1.grid_remove()
        self.email2.grid_remove()

        for x in self.list:
            x.grid_remove()
        self.list.clear()
        self.controller.show_frame(StartPage)

    def generateFirstPage(self, apartmentNumber, dPaid, lUnpaid, lEmail):
        self.apartmentNumber = apartmentNumber
        self.lPaid = [int(x) for x in dPaid.keys()]
        self.dPaid_dates = dPaid
        self.lUnpaid = lUnpaid
        self.lEmail = lEmail

        self.lPaid.sort()

        self.label.config(text=apartmentNumber)

        stringPaid = listToCommaSeperatedString(self.lPaid[-10:])
        self.labelPaid = tk.Label(self, text=stringPaid)
        self.labelPaid.grid(row=1, column=1)
        self.list.append(self.labelPaid)

        stringUnpaid = listToCommaSeperatedString(lUnpaid)
        self.labelUnpaid = tk.Label(self, text=stringUnpaid)
        self.labelUnpaid.grid(row=2, column=1)
        self.list.append(self.labelUnpaid)

        self.lEmail = lEmail

        try:
            self.email1 = tk.Label(self, text=lEmail[0])
            self.email1.grid(row=3, column=1)
            self.list.append(self.email1)
        except:
            self.email1 = tk.Label(self, text='')
            self.email1.grid(row=3, column=1)
            self.list.append(self.email1)

        try:
            self.email2 = tk.Label(self, text=lEmail[1])
            self.email2.grid(row=4, column=1)
            self.list.append(self.email2)
        except:
            self.email2 = tk.Label(self, text='')
            self.email2.grid(row=4, column=1)
            self.list.append(self.email2)

        button3 = tk.Button(self, text="Markera betalade", command=self.markAsPaid)
        button3.grid(row=2, column=2)
        self.list.append(button3)

    def markAsPaid(self):

        downloadFile(FILENAME)

        markAsPaidPageInstance = self.controller.returnInstance(MarkAsPaidPage)
        MarkAsPaidPage.spawnGridnet(markAsPaidPageInstance, self.lUnpaid)

        self.controller.show_frame(MarkAsPaidPage)

    def updateValues(self, lMarkedAsPaid):
        self.lPaid += lMarkedAsPaid
        self.lUnpaid = [x for x in self.lUnpaid if x not in lMarkedAsPaid]
        self.list.clear()
        self.lPaid.sort()
        self.lUnpaid.sort()

        for idnbr in lMarkedAsPaid:
            self.dPaid_dates[idnbr] = time.strftime("%Y_%m")

        self.labelPaid.config(text=listToCommaSeperatedString(self.lPaid))
        self.labelUnpaid.config(text=listToCommaSeperatedString(self.lUnpaid))
        self.list.append(self.labelPaid)
        self.list.append(self.labelUnpaid)

        updateFile_PaidUnpaid(self.apartmentNumber, self.dPaid_dates, self.lUnpaid)

class MarkAsPaidPage(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        self.list = []
        self.lMarkedAsPaid = []
        tk.Frame.__init__(self, parent)

        button1 = tk.Button(self, text="Utför", command=self.markAsPaidAndReturnToInfoPage)
        button1.grid(row=5, column=20)

        button1 = tk.Button(self, text="Tillbaka", command=self.returnToInfoPage)
        button1.grid(row=6, column=20)

    def returnToInfoPage(self):
        for x in self.list:
            x.grid_remove()
        self.list.clear()
        self.controller.show_frame(InfoPage)

    def markAsPaidAndReturnToInfoPage(self):
        for x in self.list:
            x.grid_remove()
        self.list.clear()

        if self.lMarkedAsPaid:
            InfoPageInstance = self.controller.returnInstance(InfoPage)
            InfoPage.updateValues(InfoPageInstance, self.lMarkedAsPaid)
            self.lMarkedAsPaid.clear()

        self.controller.show_frame(InfoPage)

    def spawnGridnet(self, lUnpaid):
        for idx, item in enumerate(lUnpaid):
            button = tk.Button(self, text=item, command=lambda idx=idx, item=item: self.markAsPaid(idx, item))
            button.grid(row=0, column=idx)
            self.list.append(button)

    def markAsPaid(self, idx, item):

        button = self.list[idx]
        if button.cget('bg') != 'green':
            button.config(bg="green")
            self.lMarkedAsPaid.append(item)
        else:
            button.config(bg="red")
            self.lMarkedAsPaid.remove(item)

class GenerateEmailList(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.checkButtonVal = tk.IntVar()
        check = tk.Checkbutton(self, text="A", variable=self.checkButtonVal)
        check.grid(row=1)

        self.checkButtonVal2 = tk.IntVar()
        check = tk.Checkbutton(self, text="B", variable=self.checkButtonVal2)
        check.grid(row=1, column=1)
