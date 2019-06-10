# -*- coding: utf-8 -*-
import webbrowser
import sys
import os
import struct
import time
#
import pyautogui
import numpy as np
import cv2
#
from win10toast import ToastNotifier
from PIL import ImageGrab
from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect
from threading import Thread
from infi.systray import SysTrayIcon


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
  
def app_pause(systray):
    global is_stop
    is_stop = False if is_stop is True else True
    # print ("Is Pause: " + str(is_stop))
    if is_stop is True:
        systray.update(
            hover_text=app + " - On Pause") 
    else:
        systray.update(
            hover_text=app)         

def app_destroy(systray):
    # print("Exit app")
    sys.exit()
    
def app_about(systray):
    # print("github.com/YECHEZ/wow-fish-bot")
    webbrowser.open('https://github.com/YECHEZ/wow-fish-bot')

if __name__ == "__main__":
    is_stop = True
    flag_exit = False
    lastx = 0
    lasty = 0
    is_block = False
    new_cast_time = 0
    recast_time = 40
    wait_mes = 0    
    app = "WoW Fish BOT by YECHEZ"
    link = "github.com/YECHEZ/wow-fish-bot"
    app_ico = resource_path('wow-fish-bot.ico')
    menu_options = (("Start/Stop", None, app_pause),
                    (link, None, app_about),)
    systray = SysTrayIcon(app_ico, app, 
                          menu_options, on_quit=app_destroy)
    systray.start()
    toaster = ToastNotifier()
    toaster.show_toast(app,
                       link,
                       icon_path=app_ico,
                       duration=5)    
    while flag_exit is False:
        if is_stop == False:
            if GetWindowText(GetForegroundWindow()) != "World of Warcraft":
                if wait_mes == 5:
                    wait_mes = 0
                    toaster.show_toast(app,
                                       "Waiting for World of Warcraft"
                                       + " as active window",
                                       icon_path='wow-fish-bot.ico',
                                       duration=5)                  
                # print("Waiting for World of Warcraft as active window")
                systray.update(
                    hover_text=app
                    + " - Waiting for World of Warcraft as active window")
                wait_mes += 1
                time.sleep(2)
            else:
                systray.update(hover_text=app)
                rect = GetWindowRect(GetForegroundWindow())
                
                if is_block == False:
                    lastx = 0
                    lasty = 0
                    pyautogui.press('1')
                    # print("Fish on !")
                    new_cast_time = time.time()
                    is_block = True
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
                    if lastx > 0 and lasty > 0:
                        if lastx != b_x and lasty != b_y:
                            is_block = False
                            if b_x < 1: b_x = lastx
                            if b_y < 1: b_y = lasty
                            pyautogui.moveTo(b_x, b_y + fish_area[1], 0.3)
                            pyautogui.keyDown('shiftleft')
                            pyautogui.mouseDown(button='right')
                            pyautogui.mouseUp(button='right')
                            pyautogui.keyUp('shiftleft')
                            # print("Catch !")
                            time.sleep(5)
                    lastx = b_x
                    lasty = b_y
                    
                    # show windows with mask
                    # cv2.imshow("fish_mask", mask)
                    # cv2.imshow("fish_frame", frame)
    
                    if time.time() - new_cast_time > recast_time:
                        # print("New cast if something wrong")
                        is_block = False               
            if cv2.waitKey(1) == 27:
                break
        else:
            # print("Pause")
            systray.update(hover_text=app + " - On Pause")   
            time.sleep(2)