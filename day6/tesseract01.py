import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\www\Tesseract-OCR\tesseract.exe"
#tesseract.exe 所在的位置

#我们添加了环境变量

img = Image.open('a.png')
text = pytesseract.image_to_string(img,lang='chi_sim')
print(text)