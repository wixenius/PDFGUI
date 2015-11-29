# -*- coding: iso-8859-1 -*-

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, TableStyle, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from passwords import EMAIL, INFO, PERMISSION_DATA

from helpFunc import listToCommaSeperatedString



def creatPermissionCompilation(d, year_month, year, month):
    fileName = "Sammanstl-%s_%s.pdf" % (year, month)
    doc = SimpleDocTemplate(fileName, pagesize=letter,
                        rightMargin=72, leftMargin=72,
                        topMargin=18, bottomMargin=18)

    lStory=[]
    styles = getSampleStyleSheet()
    font = "Helvetica"
    styles.add(ParagraphStyle(name='Justify', fontName=font, alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Right', fontName=font, alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Center', fontName=font, alignment=TA_CENTER))
    style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                       ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                       ('VALIGN',(0,0),(0,-1),'TOP'),
                       ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                       ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ])

    lStory = addToCompilationStory(lStory, styles, d, year, month, style)

    doc.build(lStory)

    return fileName

def addToCompilationStory(lStory, styles, d, year, month, tableStyle):
    header = "%s %d" % (month, int(year))
    title = "SAMMANSTÄLLNING AV PARKERINGSTILLSTÅND"

    ptext = '<b size=15>%s</b>' % header
    lStory.append(Paragraph(ptext, styles["Right"]))

    ptext = '<font size=18>%s</font>' % title
    lStory.append(Paragraph(ptext, styles["Justify"]))
    lStory.append(Spacer(1, 40))

    data = [['Lgh nr', 'Antal', 'Tillstånds ID', 'Att betala']]

    agg_nr_of_paid = 0

    for appartmentNumber in sorted(d.keys()):
        nr_of_paid = len(d[appartmentNumber])
        agg_nr_of_paid += nr_of_paid

        data.append([appartmentNumber, str(nr_of_paid), listToCommaSeperatedString(sorted(d[appartmentNumber])), "%d kr" % (nr_of_paid*INFO['PRICE_PER_PERMISSION'])])

    s = getSampleStyleSheet()
    s = s["BodyText"]
    data2 = [[Paragraph(cell, s) for cell in row] for row in data]
    t=Table(data2)
    t.setStyle(tableStyle)

    lStory.append(t)
    lStory.append(Spacer(1, 50))

    summary = "I %s %s betalades %d parkeringstillstånd á %d kr." % (month, year, agg_nr_of_paid, (agg_nr_of_paid*INFO['PRICE_PER_PERMISSION']))
    ptext = '<font size=14>%s</font>' % summary
    lStory.append(Paragraph(ptext, styles["Justify"]))

    return lStory


def addToStory(lStory, styles, serialNumber):
    header = "Lägenhet: %s" % serialNumber

    ptext = '<b size=15>%s</b>' % header
    lStory.append(Paragraph(ptext, styles["Right"]))

    ptext = '<font size=24>%s</font>' % PERMISSION_DATA['TITLE']
    lStory.append(Paragraph(ptext, styles["Justify"]))
    lStory.append(Spacer(1, 40))

    ptext = '<font size=13>%s</font>' % PERMISSION_DATA['VALID']
    lStory.append(Paragraph(ptext, styles["Justify"]))
    lStory.append(Spacer(1, 30))

    ptext = '<font size=12>%s</font>' % PERMISSION_DATA['INFO']
    lStory.append(Paragraph(ptext, styles["Justify"]))
    lStory.append(Spacer(1, 30))

    ptext = '<b size=12>%s</b>' % PERMISSION_DATA['FOOTER']
    lStory.append(Paragraph(ptext, styles["Center"]))

    ptext = '<font size=12>%s<u>%s</u>%s</font>' % (PERMISSION_DATA['FOOTER1'], EMAIL['INFO'], PERMISSION_DATA['FOOTER2'])
    lStory.append(Paragraph(ptext, styles["Justify"]))
    lStory.append(Spacer(1, 38))

    return lStory

def creatPermissionPDF(apartmentNumber, serialNumber, numberOfPermissions):
    fileName = "%s-%s.pdf" % (apartmentNumber, serialNumber)
    doc = SimpleDocTemplate(fileName, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=18, bottomMargin=18)
    lStory=[]
    styles = getSampleStyleSheet()
    font = "Helvetica"
    styles.add(ParagraphStyle(name='Justify', fontName=font, alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Right', fontName=font, alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Center', fontName=font, alignment=TA_CENTER))

    for x in range(0, numberOfPermissions):
        idNumber = "%s-%d" % (apartmentNumber, serialNumber)
        serialNumber+=1
        lStory = addToStory(lStory, styles, idNumber)

    doc.build(lStory)

    return fileName
