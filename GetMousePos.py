from pynput.mouse import Controller
import threading
import json
import keyboard
import time
ARROWS = ('q','w','e','r')

Mouse = Controller()

with open("FNF BOT/ArrowPos.json", 'r') as arquivo:
    file = json.load(arquivo)


def get_cord():
    a = Mouse.position
    b = list(a)
    return b


def MousePos(key,name):
    while True:
        if keyboard.is_pressed(key):
            file["arrows"][name] = get_cord()
            with open("FNF BOT/ArrowPos.json", 'w') as arquivo:
                json.dump(file, arquivo,indent=1)
            print("{} foi salva no {}".format(get_cord(), name))
            time.sleep(1)


left = threading.Thread(target=MousePos, args=(ARROWS[0],"left"))
down = threading.Thread(target=MousePos, args=(ARROWS[1],"down"))
up = threading.Thread(target=MousePos, args=(ARROWS[2],"up"))
right = threading.Thread(target=MousePos, args=(ARROWS[3],"right"))
left.start()
down.start()
up.start()
right.start()

