import win32gui
import win32ui
import win32con
import numpy as np

class WindowCapture:

    def __init__(self, windowName): 
        self.hwnd = win32gui.FindWindow(None, windowName)
        if not self.hwnd:
            raise Exception(f"Window not found{windowName}")
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1] 

    def get_sreenshot(self):
        """Fast grab screen """

        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (0,0), win32con.SRCCOPY)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray,dtype='uint8')
        img.shape = (self.h,self.w,4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        return img
