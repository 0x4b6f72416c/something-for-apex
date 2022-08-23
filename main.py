from grabsrcreen import WindowCapture
import cv2
import time 
import win32gui
import numpy as np 

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        print (hex(hwnd), win32gui.GetWindowText( hwnd ))

def matchTemplates(cropedImgDict,screen):

    resultOfMatching = {}

    for place, img in cropedImgDict.items():
        result = cv2.matchTemplate(screen,img,cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        resultOfMatching.update({place:max_val})
    maxResult = max(resultOfMatching,key=resultOfMatching.get)
    if  maxResult > 0.95:
        return maxResult
    
if __name__ == "__main__":

    windowName = "Apex Legends"
    windowCapture = WindowCapture(windowName)
    cropedImgDict2to10 = {i:cv2.cvtColor(cv2.imread(f"cropedImg/{i}.png"),cv2.COLOR_BGR2GRAY) for i in range(2,11)}
    cropedImgDict11to20 = {i:cv2.cvtColor(cv2.imread(f"cropedImg/{i}.png"),cv2.COLOR_BGR2GRAY) for i in range(11,21)}
    x,y,h,w = 1631,50,40,60

    currentSquadsLeft = 20
    tempArray = [20 for _ in range(8)]

    while True:

        for i in range(8):
            screen = windowCapture.get_sreenshot()
            grayScreen = cv2.cvtColor(screen,cv2.COLOR_BGR2GRAY)
            canny2 = cv2.Canny(grayScreen[y:y+h,x:x+w],50,100)
            if currentSquadsLeft > 10:
                squadsLeft = matchTemplates(cropedImgDict2to10,canny2)
            else:
                squadsLeft = matchTemplates(cropedImgDict11to20,canny2)

            tempArray[i] = squadsLeft
            print(squadsLeft)
        tempSqdsLeft = sum(tempArray)
        if tempSqdsLeft % 10 == 0 and tempSqdsLeft // 10 < currentSquadsLeft:
            currentSquadsLeft = tempSqdsLeft // 10
            print(f"Current squads left : {currentSquadsLeft}")
        if cv2.waitKey(1) == ord('q'):
            break