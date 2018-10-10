from PIL import ImageGrab
import pyautogui
import time
import numpy as np
import cv2
import sys
from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect
from PyQt5 import QtGui, QtCore, QtWidgets


class FishBotTray(QtCore.QThread):

    def __init__(self, icon):
        QtCore.QThread.__init__(self)
        self.icon = icon
        # vars
        self.flag_exit = True
        self.lastx = 0
        self.lasty = 0
        self.is_block = False
        self.is_stop = False
        self.new_cast_time = 0
        self.recast_time = 40

    def run(self):
        self.icon.showMessage('wow-fish-bot by YECHEZ', 'BOT is READY!\ngithub.com/YECHEZ/wow-fish-bot')
        while self.flag_exit:
            if GetWindowText(GetForegroundWindow()) != 'World of Warcraft':
                self.icon.setToolTip('World of Warcraft no active window !')
                #print('World of Warcraft no active window !')
                #print('-- New check 2 sec')
                time.sleep(2)
            else:
                rect = GetWindowRect(GetForegroundWindow())
                if self.is_stop == False:
                    if self.is_block == False:
                        self.lastx = 0
                        self.lasty = 0
                        pyautogui.press('1')
                        #print("Fish on !")
                        self.icon.setToolTip("Fish on !")
                        self.new_cast_time = time.time()
                        self.is_block = True
                        time.sleep(2)
                    else:
                        fish_area = (0, rect[3] / 2, rect[2], rect[3])

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
                        if self.lastx > 0 and self.lasty > 0:
                            if self.lastx != b_x and self.lasty != b_y:
                                self.is_block = False
                                if b_x < 1: b_x = self.lastx
                                if b_y < 1: b_y = self.lasty
                                pyautogui.moveTo(b_x, b_y + fish_area[1], 0.3)
                                pyautogui.keyDown("shiftleft")
                                pyautogui.mouseDown(button='right')
                                pyautogui.mouseUp(button='right')
                                pyautogui.keyUp("shiftleft")
                                #print("Catch !")
                                self.icon.setToolTip("Catch !")
                                time.sleep(5)
                        self.lastx = b_x
                        self.lasty = b_y

                        # cv2.imshow("fish_mask", mask)
                        # cv2.imshow("fish_frame", frame)

                        if time.time() - self.new_cast_time > self.recast_time:
                            #print(time.time(), self.new_cast_time)
                            #print("New cast if something wrong")
                            self.icon.setToolTip("New cast if something wrong")
                            self.is_block = False
                else:
                    #print("Pause")
                    self.icon.setToolTip("Pause")
            if cv2.waitKey(1) == 27:
                break
        QtWidgets.QApplication.quit()

    def stop(self):
        self.flag_exit = False


if __name__ == '__main__':
    #print("Fish bot Vanilla by YECHEZ started !")

    app = QtWidgets.QApplication(sys.argv)
    tray = QtWidgets.QSystemTrayIcon(
        QtGui.QIcon("wow-fish-bot.png")
    )
    fish_bot = FishBotTray(tray)
    menu = QtWidgets.QMenu()
    quit_action = menu.addAction('Quit')
    quit_action.triggered.connect(fish_bot.stop)
    tray.setContextMenu(menu)
    tray.show()
    tray.setToolTip("Fish bot Vanilla by YECHEZ started !")
    fish_bot.start()
    cv2.destroyAllWindows()
    app.exec_()
