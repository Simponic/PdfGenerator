import fpdf
from lorem import lipsum
from fpdf import FPDF
from datetime import date

leftStart = 20
rightEnd = 200
topStart = 20
bottomEnd = 287

class Header:
    def __init__(self, name="Logan Hunt", professor="Dr. Doctor", title="A Title", size=12):
        self.size = size
        self.name = name
        self.professor = professor
        self.title = title
        self.today = date.today().strftime("%B %d, %Y")

    def place(self, pdf):
        self.headtext = self.name + "\n" + self.professor + "\n" + self.today
        if (pdf.get_x() == 0 and pdf.get_y() == 0):
            # If the header isn't the first entry in the pdf
            pdf.set_xy(leftStart, topStart)
        startX = pdf.get_x()
        pdf.set_font("roboto", size=self.size)
        # The height of the text is the number of lines by the line spacing
        hh = (self.headtext.count("\n")+1)*1.5
        pdf.multi_cell(w=rightEnd-startX, h=hh, txt=self.headtext)

        pdf.set_font("roboto", size=20) # Size of title will always be 20
        tw = pdf.get_string_width(self.title)
        tx = (210 - tw)/2
        ty = pdf.get_y() + 5
        pdf.set_xy(tx, ty + 6)
        pdf.cell(w=tw, h=0, txt=self.title)

        # Set coordinates for next object
        pdf.set_xy(startX, pdf.get_y() + 12)

class Paragraph:
    def __init__(self, text=lipsum, size=12, indent=False, align="J"):
        if (indent):
            self.text = " " * 4 + text
        else:
            self.text = text
        self.size = size
        self.align = align

    def place(self, pdf):
        startX = pdf.get_x()
        pdf.set_font("roboto", size=self.size)
        pdf.multi_cell(w=rightEnd - startX,h=5, align=self.align, txt=self.text)
        pdf.set_xy(startX, pdf.get_y() + 6)

class SubItem:
    def __init__(self, heading="Lorem ipsum", text=lipsum, size=12, link=""):
        self.heading = heading
        self.text = text
        self.size = size
        self.link = link

    def place(self, pdf):
        startX = pdf.get_x()
        pdf.set_font("roboto", size=self.size+5)
        pdf.cell(w=pdf.get_string_width(self.heading), h=1, txt=self.heading, align="C", link=self.link)
        # Set indentation width for item
        pdf.set_xy(startX + 10, pdf.get_y() + self.size/2)
        pdf.set_font("roboto", size=self.size)
        pdf.multi_cell(w=rightEnd-pdf.get_x(), h=5, txt=" "*4+self.text, align="J")
        # Set coordinates for next object so we don't have weird formatting issues
        pdf.set_xy(startX, pdf.get_y() + 6)

class Image:
    def __init__(self, file):
        self.file = file

    def place(self, pdf, width=None, height=None, align="C", caption=None):
        startX = pdf.get_x()
        if (align == "C"):
            ix = (rightEnd - pdf.get_x() - width) / 2 + pdf.get_x()
        elif (align == "L"):
            ix = pdf.get_x()
        elif (align == "R"):
            ix = rightEnd - width

        if (width and height):
            pdf.image(self.file, x=ix, w=width, h=height)
        else:
            pdf.image(self.file, x=ix)


        if (caption):
            pdf.set_font("roboto", style="I", size=12)
            pdf.set_xy(ix, pdf.get_y() + 3)
            pdf.cell(w=pdf.get_string_width(caption), txt=caption)

        pdf.set_xy(startX, pdf.get_y() + 6)

def main():
    pdf = FPDF()
    pdf.add_font("roboto", fname="./RobotoMono-Regular.ttf", uni=True)
    pdf.add_font("roboto", style='I', fname='./RobotoMono-Italic.ttf', uni=True)
    pdf.add_page()

    header = Header()
    header.place(pdf)

    subItem = SubItem(link=1)
    subItem.place(pdf)
    to_page_2 = pdf.add_link()

    paragraph = Paragraph()
    paragraph.place(pdf)

    image = Image("./img.jpg")
    image.place(pdf, 100, 50, align="C", caption="Fig 1.1: A fox")

    pdf.add_page()
    paragraph.place(pdf)
    pdf.set_link(to_page_2, page=2)

    pdf.output("test.pdf","F")

if __name__ == "__main__":
    main()
