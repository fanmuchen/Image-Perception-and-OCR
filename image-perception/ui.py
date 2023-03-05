"""
这个模块提供了最简略限度的UI，用来方便地调用项目中的其他模块，快速测试它们的可用性。
"""

import tkinter as tk
from tkinter import filedialog, messagebox

def select_image_files(label = "选择图片", insist = True):
    """
    选择图片文件的方法。

    参数:
        label (str): 文件选择对话框的标题，默认为“选择图片”。
        insist (bool): 是否坚持要求用户选择文件，默认为True。

    返回值:
        image_files (tuple of str): 用户选择的图片文件路径元组。
    """
    image_files = ()
    # Create a Tkinter root window
    root = tk.Tk()
    root.title(label)
    # 一句话奇妙地解决tkinter窗口启动不置顶的问题
    root.attributes("-topmost", True) # 来自 -> https://stackoverflow.com/questions/8691655/how-to-put-a-tkinter-window-on-top-of-the-others
    root.withdraw()

    while not image_files:
        # Use file dialog to allow user to select one or more image files
        image_files = filedialog.askopenfilenames(filetypes=[(label, ('*.jpg', '*.png'))])
        if not insist:
            break
        
    return image_files

def yes_or_no(title = "等待用户输入", message = "程序需要你选择是或否"):
    """
    显示一个包含标题和消息的对话框，询问用户是或否。

    :param title: 对话框标题，默认为“等待用户输入”。
    :param message: 对话框消息，默认为“程序需要你选择是或否”。
    :return: 如果用户选择“是”，则返回True；如果用户选择“否”，则返回False。
    """
    return messagebox.askyesno(title, message)

def pop(title = "提示", message = "确认继续吗？"):
    """弹出提示框并等待用户响应。

    参数:
        title (str): 提示框的标题，默认为“提示”。
        message (str): 提示框的提示信息，默认为“确认继续吗？”。

    返回值:
        无返回值。
    """
    import tkinter as tk
    from tkinter import messagebox

    # 创建主窗口
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()

    # 显示提示框
    messagebox.showinfo(title, message)

    # 运行主循环
    root.mainloop()
