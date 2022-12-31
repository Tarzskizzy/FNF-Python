import PIL
import time
import keyboard
import threading
import Screenshot
import json

with open("FNF BOT/ArrowPos.json", 'r') as arquivo:
    file = json.load(arquivo)


cores = [(194,75,153), (0,255,255), (18,250,5), (249,57,63)]
gray = Screenshot.pixel(1030, 233)
def set(x, y , keynum,):
    while True:
        color = Screenshot.pixel(x,y)
        if color != gray:
            keyboard.press(keynum)
            time.sleep(0.025)
            keyboard.release(keynum)
        if keyboard.is_pressed('q'):
            break

def main():
    left = threading.Thread(target=set, args=(file["ARROWS"]["Left"][0], file["ARROWS"]["Left"][1],  'left',))
    down = threading.Thread(target=set, args=(file["ARROWS"]["Down"][0], file["ARROWS"]["Down"][1], 'down',))
    up = threading.Thread(target=set, args=(file["ARROWS"]["Up"][0], file["ARROWS"]["Up"][1], 'up',))
    right = threading.Thread(target=set, args=(file["ARROWS"]["Right"][0], file["ARROWS"]["Right"][1],'right',))
    left.start()
    print("pronto")
    down.start()
    print("pronto")
    up.start()
    print("pronto")
    right.start()
    print("pronto")

if __name__ == '__main__':
    main()