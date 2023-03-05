"""
这是一个测试OCR处理图像能力的模块

此程序使用了 OpenCV 和 Tesseract 库，可以处理 JPEG 和 PNG 格式的图像文件。
它会首先弹出一个文件对话框，让用户选择一个或多个图像文件，然后逐一读取图像并进行处理。
处理后的图像会显示在屏幕上，并进行 OCR 识别，最终输出识别结果。
用户可以选择是否保存处理后的图像。
"""

import os
import sys
import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Use file dialog to allow user to select one or more image files
image_files = filedialog.askopenfilenames(filetypes=[('Image Files', ('*.jpg', '*.png'))])
if not image_files: sys.exit()

# 配置 pytesseract 库
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\FMC\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"  # 修改为您的 tesseract.exe 路径

# Ask the user whether they want to save the processed images
save_processed = messagebox.askyesno("保存处理后的图片", "你想要保存处理后的图片吗？")

# 逐一读取图像文件，并进行 OCR 识别
for image_file in image_files:
    # image_path = os.path.join(image_directory, image_file)

    # 使用 OpenCV 库读取图像
    image = cv2.imread(image_file)

    # 将图像从 BGR 格式转换为灰度格式
    processing_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 对图像进行二值化处理，将文字变为白色，背景变为黑色
    processing_img = cv2.threshold( processing_img, cv2.mean(processing_img)[0]+25, 255, cv2.THRESH_BINARY)[1]
    
    cv2.imshow("Image", processing_img)
    cv2.waitKey(0)
    if save_processed:
        cv2.imwrite(f"{image_file}_processed.png", processing_img)

    # 使用 Tesseract 进行 OCR 识别
    i = 0
    while i < 15:
        try:
            i += 1
            config = f"--psm {i} --oem 1 -l chi_sim"
            text = pytesseract.image_to_string(processing_img, config = config)
            text = text.replace("\n", "")
            # 打印识别结果
            print(f"{text} ({i})")
        except:
            pass


    # config = '--psm 6 --oem 1 -l chi_sim'
    # text = pytesseract.image_to_string(processing_img, config = config)
    # text = text.replace("\n", "")
    # # 打印识别结果
    # print(f"{image_file}: {text}")
