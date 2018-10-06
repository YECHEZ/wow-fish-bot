from PIL import ImageGrab
import pyautogui
import time
import numpy as np
import cv2
import keyboard
from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect


if __name__ == '__main__':
    print("Fish bot Vanilla by YECHEZ started !")
    def callback(*arg):
        print(arg)


lastx = 0
lasty = 0
is_block = False
is_stop = False


while True:
    if GetWindowText(GetForegroundWindow()) != 'World of Warcraft':
        print('World of Warcraft no active window !')
        print('-- New check 2 sec')
        time.sleep(2)
    else:
        if keyboard.is_pressed(']'):
            if is_stop == True:
                is_stop = False
            else:
                is_stop = True
            time.sleep(2)

        rect = GetWindowRect(GetForegroundWindow())
        if is_stop == False:
            if is_block == False:
                lastx = 0
                lasty = 0
                pyautogui.press('1')
                print("Fish on !")
                is_block = True
                time.sleep(2)
            else:
                fish_area = (0, rect[3]/2, rect[2], rect[3])

                img = ImageGrab.grab(fish_area)
                img_np = np.array(img)

                frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
                frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                h_min = np.array((0, 0, 253), np.uint8)
                h_max = np.array((255, 0, 255), np.uint8)

                mask = cv2.inRange(frame_hsv, h_min, h_max)

                moments = cv2.moments(mask, 1)
                dM01 = moments['m01']
                dM10 = moments['m10']
                dArea = moments['m00']

                b_x = 0
                b_y = 0

                if dArea > 0:
                    b_x = int(dM10 / dArea)
                    b_y = int(dM01 / dArea)
                if lastx > 0 and lasty > 0:
                    if lastx != b_x and lasty != b_y:
                        is_block = False
                        if b_x < 1: b_x = lastx
                        pyautogui.moveTo(b_x, b_y+fish_area[1], 0.3)
                        pyautogui.keyDown("shiftleft")
                        pyautogui.mouseDown(button='right')
                        pyautogui.mouseUp(button='right')
                        pyautogui.keyUp("shiftleft")
                        print("Catch !")
                        time.sleep(5)
                lastx = b_x
                lasty = b_y

                #cv2.imshow("fish_mask", mask)
                #cv2.imshow("fish_frame", frame)
        else:
            print("Pause")
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
