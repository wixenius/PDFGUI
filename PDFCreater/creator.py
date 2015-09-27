# -*- coding: iso-8859-1 -*-

from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from passwords import INFO_MAIL


class PDFCreat():

    def __init__(self, apartmentNumber, serialNumber, numberOfPermissions):
        self.apartmentNumber = apartmentNumber
        self.serialNumber = serialNumber
        self.numberOfPermissions = numberOfPermissions


    def addToStory(self, lStory, styles, serialNumber):
        header = "Lägenhet: %s" % serialNumber
        title = "TILLFÄLLIGT PARKERINGSTILLSTÅND"
        valid = "GÄLLER 24 TIMMAR FRÅN OCH MED DATUM:__________ KL:__________"
        info = "AVGIFTEN 40 KR PER PÅBÖRJAD 24-TIMMARSPERIOD LÄGGS EFTER AVSLUTAD PARKERING \
                    I FÖRENINGENS BREVLÅDA TILLSAMMANS MED PARKERINGSTILLSTÅNDET."
        footer = "BÖRJAR DINA PARKERINGSTILLSTÅND TA SLUT?"
        footer1 = "Skicka ett mail till "
        mail = INFO_MAIL
        footer2 = " eller lägg en lapp i föreningens brevlåda så utfärdar vi nya."

        ptext = '<b size=15>%s</b>' % header
        lStory.append(Paragraph(ptext, styles["Right"]))

        ptext = '<font size=24>%s</font>' % title
        lStory.append(Paragraph(ptext, styles["Justify"]))
        lStory.append(Spacer(1, 40))

        ptext = '<font size=13>%s</font>' % valid
        lStory.append(Paragraph(ptext, styles["Justify"]))
        lStory.append(Spacer(1, 30))

        ptext = '<font size=12>%s</font>' % info
        lStory.append(Paragraph(ptext, styles["Justify"]))
        lStory.append(Spacer(1, 30))

        ptext = '<b size=12>%s</b>' % footer
        lStory.append(Paragraph(ptext, styles["Center"]))

        ptext = '<font size=12>%s<u>%s</u>%s</font>' % (footer1, mail, footer2)
        lStory.append(Paragraph(ptext, styles["Justify"]))
        lStory.append(Spacer(1, 38))

        return lStory

    def creat(self):
        fileName = "%s-%s.pdf" % (self.apartmentNumber, self.serialNumber)

        fileName = "fem.pdf"

        doc = SimpleDocTemplate(fileName, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=18, bottomMargin=18)
        lStory=[]
        styles=getSampleStyleSheet()
        font = "Helvetica"
        styles.add(ParagraphStyle(name='Justify', fontName=font, alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Right', fontName=font, alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='Center', fontName=font, alignment=TA_CENTER))

        for apNr in self.apartmentNumber:

            for x in range(0, self.numberOfPermissions):
                idNumber = "%s-%d" % (apNr, self.serialNumber)
                self.serialNumber += 1
                lStory = self.addToStory(lStory, styles, idNumber)

            self.serialNumber = 1

        doc.build(lStory)



        return fileName