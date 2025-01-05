import pytesseract

def analyze_image(image):
    text = pytesseract.image_to_string(image)
    return text
