from os import listdir
from PIL import Image
import pytesseract
 
imgdirectory = "images/"
croppeddirectory = "cropped/"
questiondirectory = "questions/"
filename = "mozilla"
offsetpxsize = 70
questioncounter = 0
 
 
def extractIMG():
    from pdf2image import convert_from_path
    convert_from_path(filename + '.pdf', dpi=300, fmt="JPEG", output_file="output", grayscale=True,
                      output_folder=imgdirectory)
 
 
def halfCrop():
    for index, name in enumerate(sorted(listdir(imgdirectory))):
        im = Image.open(imgdirectory + name)
        width, height = im.size
 
        if index == 0:
            im = im.crop((0, height / 4, width / 2, height))
        else:
            im = im.crop((0, 0, width / 2, height))
        im.save(croppeddirectory + name)
 
 
def exportQuestions():
    for index, name in enumerate(sorted(listdir(croppeddirectory))):
        im = Image.open(croppeddirectory + name)
        pix = pytesseract.image_to_boxes(im).split()
        symbols = []
        identified = []
        for y in range(0, len(pix), 6):
            if pix[y] in "1 2 3 4 5 6 7 8 9 0 .":
                symbols.append(pix[y:y + 5])
                symbols.append(pix[y + 6:y + 11])
                symbols.append(pix[y + 12:y + 16])
        while len(symbols) > 0:
            try:
                if symbols[0][0] in "1 2 3 4 5 6 7 8 9 0" and symbols[1][0] == "." and symbols[2][0].isalpha():
                    identified.append(symbols[0])
                    symbols.pop(0)
                    symbols.pop(1)
                    symbols.pop(2)
                else:
                    symbols.pop(0)
            except:
                symbols.pop(0)
 
        def saveQuestion(im, box, identified, index, questiondirectory):
            question = im.crop(box)
            question.save(questiondirectory + str(int(identified[0][0]) + index * 10) + ".jpg")
            identified.pop(0)
 
        width, height = im.size
        while len(identified) > 0:
            try:
                box = (
                    0, height - int(identified[0][2]) - offsetpxsize, width,
                    height - int(identified[1][2]) - offsetpxsize)
                saveQuestion(im, box, identified, index, questiondirectory)
            except:
                box = (0, height - int(identified[0][2]) - offsetpxsize, width, height)
                saveQuestion(im, box, identified, index, questiondirectory)
                break
 
 
def exportTranscript():
    for index, name in enumerate(sorted(listdir(questiondirectory))):
        with open(questiondirectory + name.replace(".jpg", ".txt"), "w") as f:
            f.write(pytesseract.image_to_string(Image.open(questiondirectory + name)))

extractIMG()
halfCrop()
exportQuestions()
exportTranscript()
