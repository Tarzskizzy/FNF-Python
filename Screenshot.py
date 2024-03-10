#Biblioteca importada da internet de forma livre , não sei o autor, mas estou deixando claro que não é de minha autoria.
import numpy as np
import win32gui
import win32api
import win32con
import win32ui
from ctypes import windll
from contextlib import contextmanager

# https://github.com/asweigart/pyscreeze/blob/0446e87235e0079f591f0c49ece7d487dedc2f9a/pyscreeze/__init__.py#L101
@contextmanager
def __win32_openDC(hWnd):
        hDC = windll.user32.GetDC(hWnd)
        if hDC == 0: #NULL
            raise WindowsError("windll.user32.GetDC failed : return NULL")
        try:
            yield hDC
        finally:
            if windll.user32.ReleaseDC(hWnd, hDC) == 0:
                print('error: ', hDC) # print hDC when we fail to release
            else:
                pass
                #print 'normal' hDC
                #raise WindowsError("windll.user32.ReleaseDC failed : return 0")

def pixel(x, y):
    """
    TODO
    """
    with __win32_openDC(0) as hdc: # handle will be released automatically
        color = windll.gdi32.GetPixel(hdc, x, y)
        if color < 0:
            raise WindowsError("windll.gdi32.GetPixel failed : return {}".format(color))
        bbggrr = "{:0>6x}".format(color) # bbggrr => 'bbggrr' (hex)
        b, g, r = (int(bbggrr[i:i+2], 16) for i in range(0, 6, 2))
        return (r, g, b)


def _screenshot_win32_2(imageFilename=None, region=None):
    """
    function from: https://www.programmersought.com/article/49766989757/
    region: tuple (left, top, right, down)
    """
    hwin = win32gui.GetDesktopWindow()
    if region:
        left, top, x2, y2 = region
        width = x2 - left
        height = y2 - top
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    signedIntsArray = bmp.GetBitmapBits(True)

    im = np.frombuffer(signedIntsArray, dtype='uint8')
    im.shape = (height, width, 4)

    if imageFilename is not None:
        im.save(imageFilename)

    # clean up
    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())
    return im

