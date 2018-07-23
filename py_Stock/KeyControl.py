#-*- coding:utf-8 -*-
import win32com.client
import win32gui,win32api,win32con
import time
import random

name = input('11')
print(name)
win32api.keybd_event(81,0,0,0)
win32api.keybd_event(87,0,0,0)
win32api.keybd_event(69,0,0,0)
win32api.keybd_event(82,0,0,0)
time.sleep(2) # waits 2 seconds
win32api.keybd_event(f,0,win32con.KEYEVENTF_KEYUP,0)


##win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0)

# Q 81
# W 87
# E 69
# R 82
