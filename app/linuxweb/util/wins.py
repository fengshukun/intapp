import time
import win32con,win32api  #安装 pip3 install pypiwin32   当前模块在windows系统上运行
class wins:
    __code=None
    def GetCursorPos(self):
        "获取鼠标位置"
        return win32api.GetCursorPos()
    def set_CursorPos(self,x,y):
        "设置鼠标位置"
        win32api.SetCursorPos((x, y))
    def left_press_down(self):
        "鼠标左键按下"
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    def left_bounce_up(self):
        "鼠标左键弹起"
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    def left_click(self):
        "鼠标左点击"
        self.left_press_down()
        time.sleep(0.1)
        self.left_bounce_up()
        time.sleep(0.1)
    def right_press_down(self):
        "鼠标右按下"
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    def right_bounce_up(self):
        "鼠标右键弹起"
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    def right_click(self):
        "鼠标右点击"
        self.right_press_down()
        time.sleep(0.1)
        self.right_bounce_up()
        time.sleep(0.1)
    def key_code(self,code):
        """键盘码按键
        
        参数 code按键码  比如a是65  键盘对应数字，查表
        """
        win32api.keybd_event(code, 0, 0, 0)  # 键盘按下
        win32api.keybd_event(code, 0, win32con.KEYEVENTF_KEYUP, 0) #键盘弹起
    def key_down(self,key):
        "键盘按下"
        self.__key_code(key)
        win32api.keybd_event(self.__code, 0, 0, 0)  # 键盘按下
    def key_up(self,key):
        "键盘弹起"
        self.__key_code(key)
        win32api.keybd_event(self.__code, 0, win32con.KEYEVENTF_KEYUP, 0) #键盘弹起
    def __key_code(self,key):
        "按键转按键码"
        if key=='a':
            self.__code=65
        