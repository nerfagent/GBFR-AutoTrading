import cv2
import concurrent.futures
from datetime import datetime
import easyocr
import keyboard
import numpy as np
import pyautogui
from pynput.keyboard import Controller as Controllerk
from pynput.mouse import Button, Controller as Controllerm
import re
import time

# Get the size of the primary screen
screen_size = pyautogui.size()
print("Primary screen size:", screen_size)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# pynput controller
kb = Controllerk()
mouse = Controllerm()

# global variables
cur_time = 0
stop_flag = False
# selectedItem = 0

# Banning list of sigils
banList = ["Attack Down Resistance", "Attack Power", "Blight Resistance", "Break Assassin", "Burn Resistance", "Cascade", "Combo Finisher", "Crabby Resonance", "Darkflame Resistance", "Defense Down Resistance",
            "Dizzy Resistance", "Dragonslayer", "Ebony", "Eternal Rage", "Fast Learner", "Fearless", "Firm Stance", "Garrison", "Glaciate Resistance", "Guard Payback", "Health", "Held Under Resistance", 
            "Improved Guard", "Improved Healing", "Injury to Insult", "Lucky Charge", "Paralysis Resistance", "Path to Mastery", "Precise Resilience", "Precise Wrath", "Quick Cooldown", "Regen", "Rupie Tycoon", 
            "Sandtomb Resistance", "Slow Resistance", "Steel Nerves", "Throw"]

conditional_ban = ["Aegis", "Autorevive", "Charged Attack", "Combo Booster", "Concentrated Fire", "Critical Damage", "Critical Hit Rate", "Damage Cap", "Drain", "Dodge Payback", "Enmity", "Exploiter", "Guts", "Improved Dodge", "Life on the Line", 
                   "Linked Together", "Low Profile", "Nimble Defense", "Nimble Onslaught", "Overdrive Assassin", "Potion Hoarder", "Provoke", "Quick Charge", "Skilled Assault", "Stamina", "Steady Focus", "Stun Power", "Tyranny", 
                   "Uplift"]

banList_trait = ["Resistance", "ATK", "Cascade", "Combo Finisher", "Crabby Resonance", "Fast Learner", "Fearless", "Firm Stance", "Garrison", "Guard Payback", "HP", "Improved Guard", "Improved Healing", "Injury to Insult",
                 "Lucky Charge", "Path to Mastery", "Precise Resilience", "Precise Wrath", "Quick Cooldown", "Regen", "Rupie Tycoon", "Steel Nerves", "Throw"]

# Define the regions for different text recognition tasks
transmarvel = lv3trans = { 'x0': 572, 'y0': 731, 'x1': 692, 'y1': 139 }
w30 = s30 = { 'x0': 209, 'y0': 810, 'x1': 55, 'y1': 80 }
wv800 = sv800 = { 'x0': 548, 'y0': 850, 'x1': 478, 'y1': 50 }
exrate = { 'x0': 501, 'y0': 683, 'x1': 102, 'y1': 32 }
rarityRange = { 'x0': 1590, 'y0': 165, 'x1': 210, 'y1': 45 }
sigilBan = conditionalSigilBan = { 'x0': 724, 'y0': 167, 'x1': 554, 'y1': 45 }
addTrait = { 'x0': 724, 'y0': 774, 'x1': 1088, 'y1': 155 }
trait1Range = { 'x0': 1347, 'y0': 286, 'x1': 308, 'y1': 30 }
trait2Range = { 'x0': 1347, 'y0': 328, 'x1': 308, 'y1': 30 }

def cvr(range, name):
    text0 = False
    text1 = False
    text2 = False
    targetNumber = 0

    screenshot = pyautogui.screenshot(region=(range['x0'], range['y0'], range['x1'], range['y1']))
    screenshot_np = np.array(screenshot)
    screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
    results = reader.readtext(screenshot_rgb)

    for (bbox, text, prob) in results:
        print(f'{datetime.now()}>>> {text}')
        if name == "lv3trans" or name == "transmarvel":
            if 'Executions' in text:
                text0 = True
            if 'enough' not in text:
                text1 = True
            if 'vouchers' not in text:
                text2 = True
        elif name == "w30" or name == "s30":
            match = re.search(r'\d+', text)
            if match:
                temp = int(match.group(0))
                if 0 <= temp <= 30:
                    targetNumber = temp
        elif name == "wv800" or name == "sv800":
            match = re.search(r'\d+', text)
            if match:
                temp = int(match.group(0))
                if 0 <= temp <= 999:
                    targetNumber = temp
        elif name == "exrate":
            match = re.search(r'\d+', text)
            if match:
                temp = int(match.group(0))
                if 0 <= temp <= 65:
                    targetNumber = temp
        elif name == "rarityRange":
            if 'LEGENDARY' in text:
                text0 = text1 = text2 = True
        elif name == "addTrait":
            if 'sigils' in text:
                text0 = True
            if 'additional' in text:
                text1 = True
            if 'trait' in text:
                text2 = True
        elif name == "sigilBan":
            for ban in banList:
                if ban in text:
                    return True
        elif name == "conditionalSigilBan":
            for ban in conditional_ban:
                if ban in text:
                    return True
        elif name == "traitxRange":
            for ban in banList_trait:
                if ban in text:
                    return True

    if name == "lv3trans" or name == "transmarvel" or name == "rarityRange" or name == "addTrait":
        return text0 and text1 and text2
    
    if name == "sigilBan" or name == "conditionalSigilBan" or name == "traitxRange":
        return text0 and text1 and text2
    
    if name == "w30" or name == "s30" or name == "wv800" or name == "sv800" or name == "exrate":
        return targetNumber
    
def buyTransmarvel():
    kb.press('s')
    time.sleep(0.1)
    kb.release('s')
    time.sleep(0.5)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(1)

    if cvr(transmarvel, "transmarvel"):
        mouse.press(Button.left)
        time.sleep(0.1)
        mouse.release(Button.left)
        time.sleep(1)
        kb.press('s')
        time.sleep(0.1)
        kb.release('s')
        time.sleep(0.5)
        mouse.press(Button.left)
        time.sleep(0.1)
        mouse.release(Button.left)
        time.sleep(0.5)
        mouse.press(Button.left)
        time.sleep(0.1)
        mouse.release(Button.left)
        time.sleep(6)
        mouse.press(Button.left)
        time.sleep(0.1)
        mouse.release(Button.left)
        time.sleep(1)
    # mouse.press(Button.left)
    # time.sleep(0.1)
    # mouse.release(Button.left)
    # time.sleep(0.5)
    # for i in range(4):
    #     kb.press('s')
    #     time.sleep(0.1)
    #     kb.release('s')
    #     time.sleep(0.5)
    # mouse.press(Button.left)
    # time.sleep(0.1)
    # mouse.release(Button.left)
    # time.sleep(0.5)
    # mouse.press(Button.left)
    # time.sleep(0.1)
    # mouse.release(Button.left)
    # time.sleep(4)
    # mouse.press(Button.left)
    # time.sleep(0.1)
    # mouse.release(Button.left)
    # time.sleep(1)

    kb.press('w')
    time.sleep(0.1)
    kb.release('w')
    time.sleep(0.5)

def sellVoucher():
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(1)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(2)

    if cvr(lv3trans, "lv3trans"):
        mouse.press(Button.left)
        time.sleep(0.1)
        mouse.release(Button.left)
        time.sleep(0.5)
        kb.press('s')
        time.sleep(0.1)
        kb.release('s')
        time.sleep(0.5)
        mouse.press(Button.left)
        time.sleep(0.1)
        mouse.release(Button.left)
        time.sleep(0.5)
        mouse.press(Button.left)
        time.sleep(0.1)
        mouse.release(Button.left)
        time.sleep(4)
        mouse.press(Button.left)
        time.sleep(0.1)
        mouse.release(Button.left)
        time.sleep(1)
    else:
        mouse.press(Button.left)
        time.sleep(0.1)
        mouse.release(Button.left)
        time.sleep(1)

    # buyTransmarvel()

    mouse.press(Button.right)
    time.sleep(0.1)
    mouse.release(Button.right)
    time.sleep(1)

def buyVoucher():
    kb.press('3')
    time.sleep(0.1)
    kb.release('3')
    time.sleep(0.5)
    kb.press('w')
    time.sleep(0.1)
    kb.release('w')
    time.sleep(0.5)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(0.5)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(0.5)
    kb.press('s')
    time.sleep(0.1)
    kb.release('s')
    time.sleep(0.5)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(0.5)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(0.5)

    mouse.press(Button.right)
    time.sleep(0.1)
    mouse.release(Button.right)
    time.sleep(1)
    mouse.press(Button.right)
    time.sleep(0.1)
    mouse.release(Button.right)
    time.sleep(1)
    kb.press('s')
    time.sleep(0.1)
    kb.release('s')
    time.sleep(0.5)
    sellVoucher() # sellVoucher() 
    kb.press('w')
    time.sleep(0.1)
    kb.release('w')
    time.sleep(0.5)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(1)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(2)

def initialVoucher():
    for i in range(3):
        kb.press('s')
        time.sleep(0.1)
        kb.release('s')
        time.sleep(0.5)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(1)
    for i in range(2):
        kb.press('s')
        time.sleep(0.1)
        kb.release('s')
        time.sleep(0.5)
    mouse.press(Button.right)
    time.sleep(0.1)
    mouse.release(Button.right)
    time.sleep(0.5)

    sellVoucher()

def tradeWrightstones(selectedItem):
    # global cur_time
    # time_diff = datetime.now() - cur_time
    # if time_diff.total_seconds() > 60 or stop_flag:
    #     return
 
    # # if cvr(w30, "w30") < 30 and cvr(wv800, "wv800") < 800:
    # if selectedItem < 20 and time_diff.total_seconds() < 30 and not stop_flag:
    if selectedItem < 20 and not stop_flag:
        temp = cvr(exrate, "exrate")
        print(temp)
        if temp < 65:
            mouse.press(Button.left)
            time.sleep(0.1)
            mouse.release(Button.left)
            time.sleep(0.5)
            # cur_time = datetime.now()
            selectedItem += 1
        kb.press('s')
        time.sleep(0.1)
        kb.release('s')
        time.sleep(0.5)
    elif not stop_flag:
        selectedItem = 0
        buyVoucher()
        for i in range(5):
            kb.press('s')
            time.sleep(0.1)
            kb.release('s')
            time.sleep(0.5)
    else:
        return
    tradeWrightstones(selectedItem)

def enterTradeWrightstones():
    kb.press('w')
    time.sleep(0.1)
    kb.release('w')
    time.sleep(0.5)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(1)
    for i in range(2):
        kb.press('s')
        time.sleep(0.1)
        kb.release('s')
        time.sleep(0.5)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(1)

    for i in range(6):
        kb.press('s')
        time.sleep(0.1)
        kb.release('s')
        time.sleep(0.5)

    global cur_time
    cur_time = datetime.now()
    time.sleep(2)
    tradeWrightstones(0)
    if stop_flag:
        return

    mouse.press(Button.right)
    time.sleep(0.1)
    mouse.release(Button.right)
    time.sleep(1)
    kb.press('s')
    time.sleep(0.1)
    kb.release('s')
    time.sleep(0.5)
    mouse.press(Button.right)
    time.sleep(0.1)
    mouse.release(Button.right)
    time.sleep(1)
    kb.press('s')
    time.sleep(0.1)
    kb.release('s')
    time.sleep(0.5)

def tradeSigils(selectedItem):
    # global cur_time
    # time_diff = datetime.now() - cur_time
    # if time_diff.total_seconds() > 60 or stop_flag:
    #     return
        
    # if selectedItem < 20 and time_diff.total_seconds() < 30 and not stop_flag:
    if selectedItem < 20 and not stop_flag:
    # if cvr(s30, "s30") < 30 and cvr(sv800, "sv800") < 800:
        rarity = cvr(rarityRange, "rarityRange")
        sigilName = cvr(sigilBan, "sigilBan")
        addtrait = cvr(addTrait, "addTrait")
        conditionalSigilName = cvr(conditionalSigilBan, "conditionalSigilBan")
        trait1 = cvr(trait1Range, "traitxRange")
        trait2 = cvr(trait2Range, "traitxRange")
        if conditionalSigilName and not addtrait:
            trait1 = True
        if addtrait:
            trait1 = trait1 or trait2
        
        if not rarity or sigilName or trait1:
            mouse.press(Button.left)
            time.sleep(0.1)
            mouse.release(Button.left)
            time.sleep(0.1)
            # cur_time = datetime.now()
            selectedItem += 1
        kb.press('s')
        time.sleep(0.1)
        kb.release('s')
        time.sleep(0.5)
    elif not stop_flag:
        selectedItem = 0
        buyVoucher()
    else:
        return
    tradeSigils(selectedItem)

def enterTradeSigils():
    kb.press('w')
    time.sleep(0.1)
    kb.release('w')
    time.sleep(0.5)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(1)
    for i in range(2):
        kb.press('w')
        time.sleep(0.1)
        kb.release('w')
        time.sleep(0.5)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(1)

    global cur_time
    cur_time = datetime.now()
    time.sleep(2)
    tradeSigils(0)
    if stop_flag:
        return
    print("Trade sigils done.")

    mouse.press(Button.right)
    time.sleep(0.1)
    mouse.release(Button.right)
    time.sleep(1)
    kb.press('w')
    time.sleep(0.1)
    kb.release('w')
    time.sleep(0.5)
    mouse.press(Button.right)
    time.sleep(0.1)
    mouse.release(Button.right)
    time.sleep(1)
    kb.press('s')
    time.sleep(0.1)
    kb.release('s')
    time.sleep(0.5)

def leftAndEnterSiero():
    mouse.press(Button.right)
    time.sleep(0.1)
    mouse.release(Button.right)
    time.sleep(2)
    kb.press('f')
    time.sleep(0.1)
    kb.release('f')
    time.sleep(3)

def main(mode):
    leftAndEnterSiero()
    initialVoucher()
    while not stop_flag:
        if mode == "Wrightstones":
            enterTradeWrightstones()
        elif mode == "Sigils":
            enterTradeSigils()
        else:
            print("Invalid mode selected. Please choose 'Wrightstones' or 'Sigils'.")
            return

def stop():
    global stop_flag
    keyboard.wait('p')
    stop_flag = True
    print("Stopping the script...")

if __name__ == "__main__":
    time.sleep(3)  # Allow time to switch to the game window
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(main, "Wrightstones") # "Wrightstones" or "Sigils"
        executor.submit(stop)