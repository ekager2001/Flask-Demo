import pdfplumber

#Original work to create this
class PDFconverter:
    #ICreate PDFconverter    
    def __init__(self):
        self.PATH =""
    
    #Set path of converter
    def setPATH(self, PATH):
        self.PATH = PATH

    #Extract words or text
    def extract(self, PATH, words=False):
        self.setPATH(PATH)
        with pdfplumber.open(PATH) as pdf:
            pages = self.pdfToText(pdf)
            if(words):     
                words = self.extractWords(pages)
                return pages
            text = self.extractText(pages)
            return text

    #Convert pdf to text
    def pdfToText(self, pdf):   
        pages = pdf.pages
        return pages

    #Extract words in each page
    def extractWords(self, pages):
        extractedWords = []
        for p in pages:
            pageWords = p.extract_words(x_tolerance=2, y_tolerance=3, keep_blank_chars=False, use_text_flow=False, horizontal_ltr=True, vertical_ttb=True)
            for w in pageWords:
                extractedWords.append(w['text'])
        return extractedWords

    #Extract all text on each page
    def extractText(self, pages):
        text = ""
        for p in pages:
            extractedText = p.extract_text(x_tolerance=2, y_tolerance=3, keep_blank_chars=False, use_text_flow=False, horizontal_ltr=True, vertical_ttb=True)
            text = text + extractedText
        return text