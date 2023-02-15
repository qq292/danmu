import os
import sys
import threading
import time

import pyautogui as pa


# Point(x=1346, y=840)
# class App: pass


def m():
    while True:
        position = pa.position()
        if pa.onScreen(position):
            print(position)


def d():
    i = 0
    while True:
        i += 1
        time.sleep(1)
        print(i)
        if i == 5:
            pa.click(1346, 840)
            return


# threading.Thread(target=d).start()
import tkinter as tk  # 在代码里面导入库，起一个别名，以后代码里面就用这个别名


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.frameRoot = FrameRoot(self, Frame1, Frame2)
        self.root.attributes("-topmost", True)  # 置顶
        self.root.attributes("-toolwindow", 2)  # 去掉窗口最大化最小化按钮，只保留关闭
        self.root.attributes('-alpha', 0.9)  # 透明度
        self.root['background'] = 'blue'  # 背景色
        self.centre()  # 居中显示
        # self.root.attributes('-transparentcolor', 'red')  # 透明色
        self.root.overrideredirect(True)  # 隐藏标题栏

    def centre(self):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        ww = sw / 2
        wh = sh / 2
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.root.geometry("%dx%d+%d+%d" % (ww, wh, x, y))

    def run(self):
        self.root.mainloop()

    def exit(self):
        time.sleep(0.2)
        os._exit(1)


class FrameRoot:
    def __init__(self, app: App, f1, f2):
        self.app = app
        self.root = tk.Frame(self.app.root)
        self.root.pack(expand=tk.YES)
        self.f1 = f1(self.root, self.app)
        self.f2 = f2(self.root, self.app)
        self.f1.root.pack(side=tk.TOP, expand=tk.YES)
        self.f2.root.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        self.root['background'] = 'purple'  # 背景色


class Frame1:
    def __init__(self, root: FrameRoot, app: App):
        self.app = app
        self.label_width = 5
        self.label_height = 1
        self.root = tk.Frame(root)
        self.d1()
        self.root['background'] = 'red'  # 背景色

    def onMove(self, event):
        new_x = (event.x - self.u_x) + self.app.root.winfo_x()
        new_y = (event.y - self.u_y) + self.app.root.winfo_y()
        self.app.root.geometry(f"+{new_x}+{new_y}")

    def onClick(self, event):
        self.u_x = event.x
        self.u_y = event.y

    def d1(self):
        for x in range(11):
            for y in range(15):

                if not (x == 0 and y == 0):
                    if x == 0:
                        tk.Label(self.root, bd=12, width=self.label_width, height=self.label_height,
                                 text=f'xy:{x},{y}').grid(row=x, column=y)
                    elif y == 0:
                        tk.Label(self.root, bd=12, width=self.label_width, height=self.label_height,
                                 text=f'xy:{x},{y}').grid(row=x, column=y)
                else:
                    t = tk.Label(self.root, bd=12, width=self.label_width, height=self.label_height,
                                 text=f' ', relief="ridge", borderwidth=10)
                    t.grid(row=x, column=y)
                    t.bind("<Button-1>", self.onClick)
                    t.bind("<B1-Motion>", self.onMove)


class Frame2:
    def __init__(self, root: FrameRoot, app: App):
        self.root = tk.Frame(root)
        self.app = app
        self.root['background'] = 'orange'  # 背景色
        self.buttonGroup()

    def buttonGroup(self):
        for i in ['退出', '设置']:
            but = tk.Button(self.root, text=i, width=14)
            but.pack(side=tk.RIGHT)
            but.bind('<Button-1>', self.onClick)

    def onClick(self, e):
        text = e.widget['text']
        if text.__eq__('退出'):
            threading.Thread(target=self.app.exit).start()

        elif text.__eq__('设置'):
            print('setting')


#  14 , 10


r = App()
r.run()
