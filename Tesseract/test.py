import pytesseract as tes

tes.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
print(tes.image_to_string('',lang='kor'))