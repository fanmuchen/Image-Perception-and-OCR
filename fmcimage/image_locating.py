import cv2
import numpy as np

def template_matching(image, template, threshold = 0.90, mask_black = False, thresholding = True):
    """
    在图像中搜索模板图像的位置。

    参数:
        image (ndarray): 原始图像的 NumPy 数组。
        template (ndarray): 模板图像的 NumPy 数组。
        threshold (float): 匹配误差阈值，默认为0.90。
        mask_black (bool): 是否使用黑色像素掩膜，默认为False。
        thresholding (bool): 是否对图像进行二值化处理，默认为True。

    返回值:
        match_locations (list of tuple of tuple): 匹配位置的列表。列表中每个元素为一个元组，包含匹配位置的左上角和右下角坐标。

    该方法使用了 OpenCV 中的模板匹配算法，在原始图像中搜索模板图像的位置。其中，参数image是原始图像的 NumPy 数组，参数template是模板图像的 NumPy 数组，参数threshold是匹配误差阈值，默认为0.90。可选的参数mask_black指定是否使用黑色像素掩膜，默认为False。可选的参数thresholding指定是否对图像进行二值化处理，默认为True。匹配结果以列表形式返回，列表中每个元素为一个元组，包含匹配位置的左上角和右下角坐标。``` 

    该方法使用了 OpenCV 中的模板匹配算法来搜索模板图像在原始图像中的位置，并返回一个元组列表，每个元组包含匹配位置的左上角和右下角坐标。可选的参数threshold、mask_black和thresholding可以分别指定匹配误差阈值、是否使用黑色像素掩膜和是否对图像进行二值化处理。该方法返回匹配位置的列表。
    """
    # 获得模板图像的高度和宽度
    h, w = template.shape[:-1]
    mask = None
    # 用于存储匹配位置的列表
    match_locations = []

    if mask_black:
        # 将所有纯黑色像素设置为255，其他像素设置为0
        _, thresh = cv2.threshold(template, 1, 255, cv2.THRESH_BINARY)
        # 将掩膜应用于模板图像
        mask = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)

    if thresholding:
        # 将图像从 BGR 格式转换为灰度格式
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 对图像进行二值化处理，将文字变为白色，背景变为黑色
        image = cv2.threshold( image, cv2.mean(image)[0]+25, 255, cv2.THRESH_BINARY)[1]
        # 将图像从 BGR 格式转换为灰度格式
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        # 对图像进行二值化处理，将文字变为白色，背景变为黑色
        template = cv2.threshold( template, cv2.mean(image)[0]+25, 255, cv2.THRESH_BINARY)[1]

    # 搜索模板图像在原始图像中的匹配位置
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED, mask=mask)

    # cv2.imshow('Result', res)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 在匹配结果中查找位置
    while True:
        # 查找匹配程度最高的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val >= threshold:
            # 找到了匹配位置
            # 在原始图像中找到模板图像的位置
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            match_locations.append((top_left, bottom_right))
            # 设置下一次搜索的区域为已找到的区域
            res[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = -1
            # print(f"Found match at ({top_left[0]}, {top_left[1]})")
        else:
            # 没有找到更多的匹配位置
            break

    # 返回匹配位置列表
    return match_locations


def show_matches(image, match_locations):
    """
    在图像上绘制匹配位置的矩形并显示结果图像。

    参数:
        image (ndarray): 原始图像的 NumPy 数组。
        match_locations (list of tuple of tuple): 匹配位置的列表。列表中每个元素为一个元组，包含匹配位置的左上角和右下角坐标。

    返回值:
        无返回值。

    该方法在原始图像中绘制匹配位置的矩形，并在新的窗口中显示结果图像。其中，参数image是原始图像的 NumPy 数组，参数match_locations是模板匹配算法返回的匹配位置列表。``` 

    该方法在原始图像中绘制模板匹配算法返回的匹配位置矩形，并在新的窗口中显示结果图像。该方法没有返回值，而是直接修改原始图像的 NumPy 数组并显示结果图像。
    """
    for match in match_locations:
        top_left, bottom_right = match
        # 画出匹配矩形
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    # 显示结果图像
    cv2.imshow('Result', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import ui
    # 加载原始图像和模板图像
    image_files = ui.select_image_files("原始图像", False)
    template_files = ui.select_image_files("模板图像", False)

    for image_file in image_files:
        image = cv2.imread(image_file)
        for template_file in template_files:
            template = cv2.imread(template_file)
            # template_matching(image, template)
            matches = template_matching(image, template)
            show_matches(image, matches)


