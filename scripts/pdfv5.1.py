import img2pdf
import os
import gc

maxsize = 500
# change above value to change final file size (Megabytes)
# script will try to reach maxsize without erroring out...

foldername = os.path.basename(os.getcwd())
filelist = []
filelists = {}
fulllist = []


def calculatefilelists(maxsize, zflag):
    global filelist, filelists, fulllist
    filelist = []
    filelists = {}
    filesize = 0
    x = 1
    y = 1
    a = 1
    while x == 1:
        filename = str(y) + ".jpg"
        try:
            with open(filename) as file:
                if zflag == 1:
                    fulllist.append(filename)
                filelist.append(filename)
                filesize += os.path.getsize(os.getcwd()+'/'+filename)
                y += 1
                if filesize >= maxsize * 1000000:
                    filelists[a] = filelist
                    filelist = []
                    filesize = 0
                    gc.collect()
                    a += 1
                file.close()
        except FileNotFoundError:
            filelists[a] = filelist
            x = 0
            gc.collect()


def pdfmultiple():
    global filelists, foldername, errors, maxsize
    a = 1
    filescreated = []
    try:
        for _ in filelists:
            name = foldername + " - " + str(a) + ".pdf"
            filescreated.append(name)
            with open(name, "wb") as f:
                print("Writing " + name)
                gc.collect()
                f.write(img2pdf.convert(filelists.get(a)))
            a += 1
        errors = 100
    except MemoryError:
        print("MemoryError - Rolling Back Changes \n")
        for x in filescreated:
            os.remove(x)
        maxsize -= 5
        print("Errors Caught in Total: " + str(errors) + "\n Using MaxSize of " + str(maxsize))
        errors += 1


def pdfcreation():
    global fulllist, foldername
    print(calculatefilelists(maxsize, 1))
    try:
        name = foldername + ".pdf"
        print("Trying to Compress Whole...")
        with open(name, "wb") as f:
            f.write(img2pdf.convert(fulllist))
            print(fulllist)
    except MemoryError:
        os.remove(name)
        del name
        del fulllist
        print("Failed, Reverting to Multiple... Using MaxSize of " + str(maxsize))


pdfcreation()
errors = 1
while errors < 25:
    calculatefilelists(maxsize, 0)
    pdfmultiple()
if errors == 100:
    print("Success!")
else:
    print("Error: Ranout of Retries")
