import json
import os
import threading
import time
import tkinter.font as tkFont
import tkinter as tk


# 适用于连连看游戏的辅助工具


class Settings:
    settings: dict

    def __init__(self):
        self.settings_read()

    @staticmethod
    def settings_save():
        json.dump(Settings.settings, open('settings.json', 'w'))

    @staticmethod
    def settings_read():
        Settings.settings = json.load(open('settings.json', 'r'))


class AppBase(Settings):
    isDrag = True
    root: tk.Tk
    __isDrag = False
    setting: str or dict

    def __init__(self):
        super(AppBase, self).__init__()
        self.inin()

    @classmethod
    def inin(cls):
        cls.setting = Settings.settings[cls.__name__]

    def centre(self, w=0.5, h=0.5):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        ww = sw * w
        wh = sh * h
        self.root.geometry(
            "%dx%d+%d+%d" % (
                ww, wh, self.setting['position']['x'], self.setting['position']['y']))

    #  让窗口可以拖拽移动
    def setDrag(self):
        self.root.bind("<Button-1>", self.__onClick)
        self.root.bind("<B1-Motion>", self.__onMove)
        self.root.bind("<ButtonRelease-1>", self.__onButtonRelease)

    def __onButtonRelease(self, event):
        if self.__isDrag:
            self.__isDrag = False
            self.onMoveEnd()

    # 窗口移动结束事件
    def onMoveEnd(self):
        self.setting['position']['x'] = self.root.winfo_rootx()
        self.setting['position']['y'] = self.root.winfo_rooty()
        self.settings_save()

    def __onMove(self, event):
        if self.isDrag:
            self.__isDrag = True
            new_x = (event.x - self.u_x) + self.root.winfo_x()
            new_y = (event.y - self.u_y) + self.root.winfo_y()
            self.root.geometry(f"+{new_x}+{new_y}")

    def __onClick(self, event):
        self.u_x = event.x
        self.u_y = event.y

    def run(self):
        self.root.mainloop()

    @classmethod
    def __exit(cls):
        time.sleep(0.2)
        os._exit(10)

    @classmethod
    def exit(cls):
        threading.Thread(target=cls.__exit).start()


class SettingWindows(AppBase):
    def __init__(self):
        super(SettingWindows, self).__init__()
        self.root = tk.Tk()
        self.root.attributes("-toolwindow", 2)  # 去掉窗口最大化最小化按钮，只保留关闭
        self.root.title('Settings')
        self.root.attributes("-topmost", True)  # 置顶
        self.centre(0.25, 0.4)
        self.setDrag()
        self.layout = tk.Frame(self.root)
        self.layout.pack(fill=tk.Y, expand=tk.YES)
        self.grid_setting(self.layout)
        self.labels(self.layout)
        self.but = tk.Button(self.layout, text='应用')
        self.but.bind('<Button-1>', self.ui_update)
        self.but.pack(side=tk.BOTTOM, fill=tk.X)

    def labels(self, root):
        frm = tk.Frame(root)
        self.label_width_spi = self.label_spinbox(frm, '宽度', Settings.settings['Label']['width'])
        self.label_height_spi = self.label_spinbox(frm, '高度', Settings.settings['Label']['height'])
        frm.pack(side=tk.TOP)

    def onMoveEnd(self):
        super(SettingWindows, self).onMoveEnd()

    def ui_update(self, event):
        Settings.settings['Grid']['row'] = int(self.row_spi.get())
        Settings.settings['Grid']['col'] = int(self.col_spi.get())
        Settings.settings['Label']['width'] = int(self.label_width_spi.get())
        Settings.settings['Label']['height'] = int(self.label_height_spi.get())
        Frame1.rot.grid()
        Settings.settings_save()

    def grid_setting(self, root):
        frm = tk.Frame(root)
        frm.config(pady="20")
        frm.pack(side=tk.TOP)
        frm2 = tk.Frame(frm)
        frm2.config(pady="10")
        frm2.pack(side=tk.TOP, fill=tk.X)
        lab = tk.Label(frm2, text='网格设置:')
        lab.pack(side=tk.LEFT)
        self.row_spi = self.label_spinbox(frm, '行数', Settings.settings['Grid']['row'])
        self.col_spi = self.label_spinbox(frm, '列数', Settings.settings['Grid']['col'])

    def label_spinbox(self, root, text, b):
        frm = tk.Frame(root, bg='red')
        lab = tk.Label(frm, text=text)
        spi = tk.Spinbox(frm, value=b)
        lab.pack(side=tk.LEFT)
        spi.pack(side=tk.LEFT)
        frm.pack(side=tk.RIGHT, expand=tk.YES)
        return spi


class App(AppBase):
    def __init__(self):
        super(App, self).__init__()
        self.root = tk.Tk()
        self.frameRoot = FrameRoot(self, Frame1, Frame2)
        self.root.attributes("-topmost", True)  # 置顶
        self.root.attributes('-alpha', 0.9)  # 透明度
        self.root['background'] = 'blue'  # 背景色
        self.centre(h=1, w=1)  # 居中显示
        self.root.attributes('-transparentcolor', 'blue')  # 透明色
        self.root.overrideredirect(True)  # 隐藏标题栏
        self.setDrag()

    def onMoveEnd(self):
        super(App, self).onMoveEnd()


class FrameRoot:
    def __init__(self, app: App, f1, f2):
        self.app = app
        self.root = tk.Frame(self.app.root)
        self.root.pack(expand=tk.YES)  # ,fill=tk.Y
        self.f1 = f1(self.root, self.app)
        self.f2 = f2(self.app.root, self.app)
        self.f1.root.pack(side=tk.TOP, expand=tk.YES)
        self.f2.root.place(anchor=tk.N, relx=0.5, rely=1, in_=self.root)  # in_=
        # self.f2.root.place(anchor=tk.S,relx=0.5,rely = 0,in_=self.root)
        self.root['background'] = 'blue'  # 背景色


class Frame1:
    data_position = {}
    isHide = False
    rot = None

    def __init__(self, root: FrameRoot, app: App):
        self.app = app
        self.root = tk.Frame(root)
        Frame1.rot = self
        self.px1 = tk.PhotoImage(file="./Images/px1.png")
        self.root['background'] = 'blue'  # 背景色
        self.fontStyle = tkFont.Font(family="Lucida Grande", size=15, weight="bold")
        self.grid()

    def Label(self, x, y, key_name):
        lab = tk.Label(self.root,
                       height=Settings.settings['Label']['height'],
                       image=self.px1, borderwidth=1,
                       relief="sunken", bg='blue', )
        lab['width'] = Settings.settings['Label']['width']
        lab.grid(row=x, column=y)
        Frame1.data_position[key_name] = lab
        t = tk.Label(lab, text=key_name, font=self.fontStyle, cursor='cross', relief=tk.RIDGE, fg='red', bg='yellow')
        t.place(x=0, y=0)

        return lab

    def grid(self):
        row = Settings.settings['Grid']['row'] or 1
        col = Settings.settings['Grid']['col'] or 1
        abc = 'CDEFGHIKLMGOPQRSTUVWXYZ'  # 有的字母加数字组合会被屏蔽 比如j8,a13
        le = len(abc)
        key_names = []
        for x in range(row):
            s = x // le
            p = x % le
            q = abc[s - 1] if s and s <= le else ''
            t = q + abc[p]
            for y in range(1, col):
                key_name = t + str(y + 1)
                if key_name in Frame1.data_position:
                    widget = Frame1.data_position[key_name]
                    if widget['width'] != Settings.settings['Label']['width']:
                        widget['width'] = Settings.settings['Label']['width']
                    if widget['height'] != Settings.settings['Label']['height']:
                        widget['height'] = Settings.settings['Label']['height']
                    widget.grid()

                else:
                    self.Label(x, y, key_name)
                key_names.append(key_name)

        if len(Frame1.data_position) > len(key_names):
            for k, v in Frame1.data_position.items():
                if k not in key_names:
                    Frame1.data_position[k].grid_forget()


class Frame2:
    def __init__(self, root: FrameRoot, app: App):
        self.root = tk.Frame(root)
        self.app = app
        self.root['background'] = 'blue'  # 背景色
        self.root.place()
        self.buttonGroup()
        self.closed = True
        self.win: SettingWindows

    def buttonGroup(self):
        for i in ['退出', '设置', '锁定', '隐藏']:
            but = tk.Button(self.root, text=i, width=14)
            but.pack(side=tk.RIGHT)
            but.bind('<Button-1>', self.onClick)

    def onClick(self, e):
        widget = e.widget
        text = widget['text']
        if text.__eq__('退出'):
            self.app.exit()

        elif text.__eq__('设置'):
            if self.closed:
                self.closed = False
                self.win = SettingWindows()
                self.win.root.protocol('WM_DELETE_WINDOW',
                                       lambda: (self.win.root.destroy(), setattr(self, 'closed', True)))
            else:
                self.closed = True
                self.win.root.destroy()

        elif text in ['锁定', '解锁']:
            self.app.isDrag = not self.app.isDrag
            widget['text'] = '锁定' if self.app.isDrag else '解锁'

        elif text in ['隐藏', '显示']:
            if Frame1.isHide is False:
                Frame1.rot.root.pack_forget()
                Frame1.isHide = True
                widget['text'] = '显示'
            else:
                Frame1.rot.root.pack()
                Frame1.isHide = False
                widget['text'] = '隐藏'


if __name__ == '__main__':
    r = App()
    r.run()
