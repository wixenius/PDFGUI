# -*- coding: iso-8859-1 -*-
import os

from GUI import MainGUI

from PDFCreater import PDFCreat
import webbrowser


def main():

    for file in os.listdir():
        if file.endswith('.pdf'):
            os.remove('%s' % file)

    root = MainGUI.MainGUI()
    root.geometry("600x400")
    #root.mainloop()

    d = {"A28": {"unpaid": [], "paid": [], "email": ["levin_malin@hotmail.com"]}, "B21": {"unpaid": [], "paid": [], "email": ["matsring2@hotmail.com"]}, "A22": {"unpaid": [], "paid": [], "email": ["r.svedjestrand@gmail.com"]}, "A44": {"unpaid": [], "paid": [], "email": ["hugo.kreipke@gmail.com"]}, "A52": {"unpaid": [], "paid": [], "email": ["fredrik.lars.strand@gmail.com"]}, "A43": {"unpaid": [], "paid": [], "email": ["josefin.koczy@live.se"]}, "B41": {"unpaid": [], "paid": [], "email": ["jakob.karlsson@gmail.com", "malin.stalbrand@gmail.com"]}, "A47": {"unpaid": [], "paid": [], "email": ["englundfredrik@hotmail.com"]}, "A32": {"unpaid": [], "paid": [], "email": ["hannes.forsman@gmail.com"]}, "A24": {"unpaid": [], "paid": [], "email": ["helen@kalaskommunikation.se"]}, "A42": {"unpaid": [], "paid": [], "email": ["ronnie_koenig@hotmail.com"]}, "B51": {"unpaid": [], "paid": [], "email": ["dino.nikas@euromaint.com"]}, "A46": {"unpaid": [], "paid": [], "email": ["jill.81@hotmail.com"]}, "A36": {"unpaid": [], "paid": [], "email": ["j_bjornaes@hotmail.com"]}, "A57": {"unpaid": [], "paid": [], "email": ["onayjakobov@gmail.com"]}, "A38": {"unpaid": [], "paid": [], "email": ["plojing46@hotmail.com", "johanpl_90@hotmail.com"]}, "A31": {"unpaid": [], "paid": [], "email": ["fredrik.wixenius@gmail.com", "anna_stromblad@hotmail.com"]}, "A37": {"unpaid": [], "paid": [], "email": ["niklas_wigren@hotmail.com"]}, "A33": {"unpaid": [], "paid": [], "email": ["marcus@lomaw.se"]}, "A54": {"unpaid": [], "paid": [], "email": ["susan.ranchber@hotmail.com", "gast@bktv.nu"]}, "A41": {"unpaid": [], "paid": [], "email": ["tuettelmann@gmail.com"]}, "B81": {"unpaid": [], "paid": [], "email": ["stephan.keier@hotmail.com"]}, "A53": {"unpaid": [], "paid": [], "email": ["micke.preston@gmail.com"]}, "B71": {"unpaid": [], "paid": [], "email": ["ewa.uboner@live.se", "uboner43@gmail.com"]}, "A51": {"unpaid": [], "paid": [], "email": ["cyril_gueret@hotmail.com"]}, "A34": {"unpaid": [], "paid": [], "email": ["caroline.engqvist@live.se"]}, "A55": {"unpaid": [], "paid": [], "email": ["sjakobov@gmail.com"]}, "A27": {"unpaid": [], "paid": [], "email": ["lovisasvensson@hotmail.com"]}, "B61": {"unpaid": [], "paid": [], "email": ["soheil.o.shad@gmail.com"]}, "A56": {"unpaid": [], "paid": [], "email": ["nadias@corinneandfriends.se"]}, "A35": {"unpaid": [], "paid": [], "email": ["evelina.holger@gmail.com"]}, "A21": {"unpaid": [], "paid": [], "email": ["per.gustavsson89@gmail.com"]}, "B31": {"unpaid": [], "paid": [], "email": ["kerstin.nordmanolsen@gmail.com"]}, "A26": {"unpaid": [], "paid": [], "email": ["thepringleman@hotmail.com"]}, "A58": {"unpaid": [], "paid": [], "email": ["emilia.kago@hotmail.com"]}, "A45": {"unpaid": [], "paid": [], "email": ["julia.lofkvist@hotmail.com"]}, "A48": {"unpaid": [], "paid": [], "email": ["mikael@bilbo.se"]}, "A25": {"unpaid": [], "paid": [], "email": ["johan.nilsson@storstockholm.brand.se"]}, "A23": {"unpaid": [], "paid": [], "email": ["cinabina2000@yahoo.se"]}}

    PDFC = PDFCreat(sorted(list(d.keys())), 1, 5)
    fileName = PDFC.creat()

    #updateFile_PaidUnpaid(self.apartmentNumber, self.lPaid, self.lUnpaid)

    webbrowser.open_new(r'%s' % fileName)


if __name__ == "__main__":
    main()

