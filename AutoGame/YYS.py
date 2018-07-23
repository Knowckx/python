import pyautogui
import time

#全局
base_loc = (153,90) #基准点

def TestPos():
    # tarPos = (base_loc[0], base_loc[1]-100, 200 ,200)
    tarPos = Repos(325,425,200,200)
    pyautogui.screenshot('photo/looks.png',region=tarPos)  
    

m_size = (1600,900) #窗口大小


#-------------等待XX秒
def WaitBattleEnd():
    pass
    # while True:  
    # try:  
    #     # sleep for the remaining seconds of interval  
    #     time_remaining = interval-time.time()%interval  
    #     print_ts("Sleeping until %s (%s seconds)..."%((time.ctime(time.time()+time_remaining)), time_remaining))  
    #     time.sleep(time_remaining)  
    #     print_ts("Starting command.")  
    #     # execute the command  
    #     status = os.system(command)  
    #     print_ts("-"*100)  
    #     print_ts("Command status = %s."%status)  
    # except Exception, e:  
    #     print e  

#-------------移动到Pos,相对于基准点。
def MoveCur(pos):
    pyautogui.moveTo(base_loc[0] + pos[0],base_loc[1] + pos[1])


def Repos(*args):
    pos = list(args)
    pos[0] = base_loc[0] + args[0]
    pos[1] = base_loc[1] + args[1]
    return pos

#御魂模块
def yuhun():
    # pos_start  = [500,400]  #御魂3层
    # MoveCur(pos_start)
    # pyautogui.click()
    # pos_start1  = [1190,625]  #挑战
    # MoveCur(pos_start1)
    # pyautogui.click()

    time.sleep(3)
    battle_start  = [1470,700]  #战斗
    MoveCur(battle_start)
    pyautogui.click()
    pass


#-------------图像对比





def photo():
    # im = pyautogui.screenshot(region=(0, 0, 300 ,400))
    # print(Repos(840, 850,100 ,50))
    tarPos = Repos(300, 420, 100 ,100)
    pyautogui.screenshot('photo/looks.png',region=tarPos)  
    BattleEndPos = pyautogui.locateOnScreen('photo/battle_end.png',region=tarPos)  
    print(BattleEndPos)
    if BattleEndPos[0] > 0:
        print("战斗结束")
    pass


	# ------------------------定位
	# #  返回(最左x坐标，最顶y坐标，宽度，高度)
	# pyautogui.locateOnScreen('pyautogui/looks.png')  
	# 	.locateCenterOnScreen 返回中心位置
	# ------------圈定区域里找
	# locate(needleImage, haystackImage, grayscale=False)




def TimeFucn():
    gapTime = 3
    T1 = time.time()
    time.sleep(3)
    T2 = time.time()
    print(T1,T2,T2-T1)
    while(True):
        time.sleep(gapTime)
        print("Ones")
        # time
    
    pass




def main():
    pyautogui.PAUSE = 0.3
    # TestPos()
    TimeFucn()
    # photo()
    # yuhun()
__name__ = 'main'
testStr = 'main'
if testStr == 'main':
    main()


    