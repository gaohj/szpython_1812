import pytesseract
from PIL import Image
from urllib import request
import time
def texts():
    pytesseract.pytesseract.tesseract_cmd = r"C:\www\Tesseract-OCR\tesseract.exe"
    url = 'https://passport.lagou.com/vcode/create?from=register&refresh=1513081451891'
    while True:
        request.urlretrieve(url,'captcha.png')
        img = Image.open('captcha.png')
        text = pytesseract.image_to_string(img)
        print(text)
        time.sleep(2)


if __name__ == "__main__":
    texts()