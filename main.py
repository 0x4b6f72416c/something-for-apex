from grabsrcreen import WindowCapture
from pytesseract import pytesseract
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter
import cv2, os ,re, win32gui

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
    currentKills = [0]
    try:
        while squadsLeft > 1 :

            for i in range(8):
                screen = windowCapture.get_sreenshot()
                currentSquadsLeft = getCurrentSqadsLeft(screen)
                tempVal = getCurrentKills(screen)
                if tempVal != None:
                    currentKills.append(tempVal)

                if currentSquadsLeft != None and squadsLeft != None  and  currentSquadsLeft < squadsLeft and currentSquadsLeft >= (squadsLeft - 3):
                    squadsLeft = currentSquadsLeft
                    print(f"Squads Left: {squadsLeft}")
                    cnt = Counter(currentKills).most_common(1)[0][0]
                    killsResult = cnt - squadsKills[currentSquadsLeft + 1]
                    squadsKills[currentSquadsLeft] = killsResult
                    print(f"Kills between [{squadsLeft + 1} <-> {squadsLeft}] : {killsResult}")
            currentKills.clear()

    except KeyboardInterrupt:
        pass

    finally:
        sqds = list(squadsKills.keys())
        kills = list(squadsKills.values())
        plt.bar(range(len(squadsKills)), kills,tick_label = sqds)
        now = datetime.now()
        now =  now.strftime("%d-%m-%Y-[%H.%M]")

        folder = 'Apex-Statistics'

        if not os.path.isdir(folder):
            os.makedirs(folder)

        plt.savefig(f"{folder}\{now}.png")
        plt.show()
        plt.close()