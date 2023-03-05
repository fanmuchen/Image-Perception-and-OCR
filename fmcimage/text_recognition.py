"""
这个模块提供了一些用于OCR（Optical Character Recognition）的方法，包括选择图像文件、准备图像、执行OCR识别等。
"""
import sys
import cv2
import pytesseract

def prepare_img(image):
    """
    准备图像以供OCR处理。

    Args:
        image: 要处理的原始图像。

    Returns:
        processing_img: 已转换为灰度图像并进行了二值化处理的图像。
    """
    # 将图像从 BGR 格式转换为灰度格式
    processing_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 对图像进行二值化处理，将文字变为白色，背景变为黑色
    processing_img = cv2.threshold( processing_img, cv2.mean(processing_img)[0]+25, 255, cv2.THRESH_BINARY)[1]

    return processing_img

def perform_ocr(image, psm = 6, lang = None):
    """
    使用Tesseract OCR引擎对图像进行识别，返回识别出的文本。

    Args:
        image: 要识别的图像。
        psm: OCR引擎的页面分段模式（page segmentation mode）。
        lang: 要用于识别的语言。

    Returns:
        text: 从图像中识别出的文本。
    """
    if lang: lang = f" -l {lang}"
    config = f"--psm {psm} --oem 1{lang}"
    text = pytesseract.image_to_string(processing_img, config = config)
    return text

def perform_ocr_with_data(image, psm = 6, lang = None):
    """
    使用Tesseract OCR引擎对图像进行识别，返回识别数据。

    Args:
        image: 要识别的图像。
        psm: OCR引擎的页面分段模式（page segmentation mode）。
        lang: 要用于识别的语言。

    Returns:
        data: 识别数据。
    """
    if lang: lang = f" -l {lang}"
    config = f"--psm {psm} --oem 1{lang}"
    data = pytesseract.image_to_data(processing_img, config = config)
    return data



if __name__ == "__main__":

    import ui
    import subprocess

    # 配置 pytesseract 库
    # 该路径是在Python应用程序中的全局变量。
    # 在Python应用程序的任何位置，只要设置了Tesseract OCR引擎的可执行文件路径，就可以在整个应用程序中使用它，不需要再重新设置一次。
    try:
        subprocess.run(['tesseract', '-v'], check=True)
        print("Tesseract found.")
    except:
        print("Tesseract not found. Using hardcoded path.")
        pytesseract.pytesseract.tesseract_cmd = r"C:\Users\FMC\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"  # 修改为您的 tesseract.exe 路径
    # 最好还是在系统变量中设置好tesseract路径。

    image_files = ui.select_image_files(insist = False)
    if not image_files: sys.exit()

    # Ask the user whether they want to save the processed images
    save_processed = ui.yes_or_no("保存处理后的图片", "你想要保存处理后的图片吗？")
    save_results = ui.yes_or_no("保存识别结果", "你想要保存识别结果吗？")
    
    for image_file in image_files:

        image = cv2.imread(image_file)
        processing_img = prepare_img(image)
        cv2.imshow("Image", processing_img)
        cv2.waitKey(0)
        if save_processed:
            cv2.imwrite(f"{image_file}_processed.png", processing_img)
        if save_results:
            results_file = open(f"{image_file}_ocr_results.txt", "w", encoding="utf-8")
        # 使用 Tesseract 进行 OCR 识别
        for i in range(1, 16):
            try:
                text = perform_ocr(processing_img, i, "chi_sim")
                text = text.replace("\n", "")
                # 打印识别结果
                print(f"{text} (psm: {i})")
                if save_results:
                    # 将识别结果写入文本文件中
                    data = perform_ocr_with_data(processing_img, i, "chi_sim")
                    results_file.write(f"{image_file} (psm: {i}): {text}\n")
                    results_file.write(f"{data}\n")
            except Exception as e:
                print(f"扫描中出错: {e}", file=sys.stderr)
                if save_results:
                    results_file.write(f"{image_file} (psm: {i}): {e}\n\n")
                pass
        if save_results:
            results_file.close()

