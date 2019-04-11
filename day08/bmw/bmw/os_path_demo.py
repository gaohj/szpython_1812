import os
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'images')
if not os.path.exists(img_path):
    os.mkdir(img_path)
else:
    print("image文件夹已经存在")