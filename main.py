from PIL import Image, ImageEnhance
import fitz
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import sys
from copy import copy

def addWatermark(inputFile, img, outFile, alpha: int=20):
    imgPath = '{}/AppData/Local/Temp/watermark.png'.format(os.path.expanduser('~').replace('\\', '/'))

    img = Image.open(img).copy()

    # opacity = int(alpha)/255
    opacity = int(alpha)*255/100
    print(opacity)
    assert opacity >= 0 and opacity <= 1
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    else:
        img = img.copy()
    alpha = img.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    img.putalpha(alpha)

    # img.save(imgPath, 'png')
    img.resize(PdfFileReader(inputFile).pages[0].mediabox[2:]).save(imgPath, 'png')
    # img.rotate(45)
    handle = fitz.open(inputFile)
    [page.wrap_contents() for page in handle  if not page.is_wrapped]
    rect = fitz.Rect(PdfFileReader(inputFile).pages[0].mediabox)
    for page in handle:
        page.insert_image(rect, stream=open(imgPath, 'rb').read())
    handle.save(outFile)
    print(imgPath)
    # os.remove(imgPath)

# addWatermark(sys.argv)
addWatermark(*sys.argv[1:])