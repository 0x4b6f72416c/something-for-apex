from grabsrcreen import WindowCapture
from pytesseract import pytesseract
import matplotlib.pyplot as plt
from datetime import datetime
import cv2
import win32gui
import re

_PATH_TO_TESSERACT = r"D:\teserract\tesseract.exe"

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        print (hex(hwnd), win32gui.GetWindowText( hwnd ))

def getCurrentSqadsLeft(screen):
    x,y,h,w = 1644,40,40,100
    string = pytesseract.image_to_string(screen[y:y+h,x:x+w])
    string = re.split(' ',string)

    try:
        stringToInt = int(string[0])
        return stringToInt
    except:
        pass 

def getCurrentKills(screen):
    x,y,h,w = 1535,85,40,200  
    string =pytesseract.image_to_string(screen[y:y+h,x:x+w])
    string = re.split(' ',string)
    try:
        stringToInt = int(string[0])
        return stringToInt
    except:
        pass 


if __name__ == "__main__":

    pytesseract.tesseract_cmd = _PATH_TO_TESSERACT
    windowName = "Apex Legends"
    windowCapture = WindowCapture(windowName)
    squadsKills = {a:0 for a in range(2,22)}
    squadsLeft = 20
    currentKills = 0
    try:
        while squadsLeft > 1 :

            for i in range(8):
                screen = windowCapture.get_sreenshot()
                currentSquadsLeft = getCurrentSqadsLeft(screen)
                tempVal = getCurrentKills(screen)
                if tempVal != None:
                    currentKills = tempVal

                if currentSquadsLeft < squadsLeft:
                    squadsLeft = currentSquadsLeft
                    print(f"Squads Left: {squadsLeft}")
                    k0  =  currentKills - squadsKills[currentSquadsLeft + 1]
                    squadsKills[currentSquadsLeft] = k0 
                    print(f"Kills between [{squadsLeft + 1} <-> {squadsLeft}] : {k0}")

    except KeyboardInterrupt:
        sqds = list(squadsKills.keys())
        kills = list(squadsKills.values())
        plt.bar(range(len(squadsKills)), kills,tick_label = sqds)
        now = datetime.now()
        now =  str(now.strftime("%d-%m-%Y-%H:%M"))
        plt.savefig('test',format='png')
        plt.show()
        