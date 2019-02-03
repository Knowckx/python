#自动按键

import keyboard
import time

isLoop = True

cd = 0.25


def StartWait():
    global isLoop

    while True:
        print("we are waiting")
        keyboard.wait("`")
        # keyboard.send("w")
        # keyboard.send("q")
        keyboard.on_press_key('`',StopLoop)
        isLoop =True
        while isLoop:
            LoopContent()
        continue



def LoopContent():
    print("loop ing")



    # keyboard.send("e")
    # time.sleep(0.25) 

    keyboard.send("w")
    keyboard.send("q")
    # keyboard.send("")

    # time.sleep(0.25) 
    # keyboard.send("r")

    # keyboard.send("A")

    # keyboard.send("r")


    keyboard.send("5")
    keyboard.send("6")
    # time.sleep(0.25) 
    # keyboard.send("r")
    time.sleep(cd) 


def StopLoop(msg = None):
    global isLoop
    isLoop = False


StartWait()

keyboard.send()
