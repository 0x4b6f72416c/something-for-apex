from re import X
import win32api
import pyautogui as pg
import time

with open('pos.txt', 'w') as f:
    i = 1
    for j in range(4):
        if win32api.GetKeyState(0x01) < 0:
            x,y = pg.position()
            posString = f" x:{x} y:{y}\n"
            f.write(posString)
            time.sleep(1)