import keyboard
import time

isLoop = True
cd = 0.25

def StartWait():
    global isLoop
    while True:
        print("waiting for start")
        keyboard.wait("`")
        keyboard.on_press_key('`',StopLoop)
        isLoop = True
        while isLoop:
            LoopContent()
        continue


def LoopContent():
    print("looping")
    keyboard.send("q") # 滚键盘流
    keyboard.send("w") 
    keyboard.send("e")
    # keyboard.send("alt+w") # 释放目标自己（护盾）
    keyboard.send("4") # 道具  比如科技刀
    time.sleep(cd) 

def StopLoop(msg = None):
    global isLoop
    isLoop = False

StartWait()
