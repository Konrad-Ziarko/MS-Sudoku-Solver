from SudokuSolver import SudokuGrid
import win32gui
import win32con
import win32api
import os,time
from PIL import ImageGrab,Image, ImageEnhance, ImageFilter
import pytesseract

__window_title__ = 'Microsoft Sudoku' 
__wnd__ = []

__idx__ = 0

def screenGrab(box):
    im = ImageGrab.grab(box)
    global __idx__
    #im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + str(__idx__) + '.png', 'PNG')
    __idx__+=1
    return im
    

def isRealWindow(hwnd):
    if not win32gui.IsWindowVisible(hwnd):
        return False
    if win32gui.GetParent(hwnd) != 0:
        return False
    hasNoOwner = win32gui.GetWindow(hwnd, win32con.GW_OWNER) == 0
    lExStyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
      or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
        if win32gui.GetWindowText(hwnd):
            return True
    return False

def enumHandler(hwnd, lParam):
    if win32gui.IsWindowVisible(hwnd):
        if __window_title__ in win32gui.GetWindowText(hwnd):
            #win32gui.MoveWindow(hwnd, 0, 0, 760, 500, True)
            if isRealWindow(hwnd):
                wnd = []
                box = win32gui.GetWindowRect(hwnd)
                wnd.append(box[0])
                wnd.append(box[1])
                wnd.append(box[2])
                wnd.append(box[3])
                box = win32gui.GetClientRect(hwnd)
                wnd[2]=wnd[0]+box[2]
                wnd[3]=wnd[1]+box[3]
                wnd[0]+=10
                win32gui.SetForegroundWindow(hwnd)
                screenGrab(tuple(wnd))
                __wnd__.append(wnd[0])
                __wnd__.append(wnd[1])
                __wnd__.append(wnd[2])
                __wnd__.append(wnd[3])
                return


def m_click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
def k_click(code):#1 = 0x31; 9 = 0x39
    win32api.keybd_event(code,0,0,0)
    time.sleep(.1)#delete
    win32api.keybd_event(code,0,win32con.KEYEVENTF_KEYUP,0)



win32gui.EnumWindows(enumHandler, None)
time.sleep(2)
m_click(__wnd__[0]+500,__wnd__[1]+550)#hard

time.sleep(2)#temp #odczekanie na zaladowanie poziomu

#rozpoznanie cyfr na siatce (komorka 51x52; odstepy 3px szerokie, 2px wysokie; co 3 komorki +1px)
#siatka x179 y127 485x485
numbers = list()

pad = [179, 127]
x = __wnd__[0]+pad[0]
y = __wnd__[1]+pad[1]
for col in range(9):
    for row in range(9):
        padx = 0
        pady = 0
        if row > 2:
            padx += 1
            if row > 5:
                padx += 1
        if col > 2:
            pady+=2
            if col > 5:
                pady +=2
        numbers.append(screenGrab((x+int(row*53.5)+padx, y+int(col*53)+pady, x+int(row*53.5)+51+padx,  y+int(col*53)+52+pady)))


from pytesser3 import *
from io import StringIO


im = numbers[4]
#im = im.filter(ImageFilter.MedianFilter())
#enhancer = ImageEnhance.Contrast(im)
#im = enhancer.enhance(2)
#im = im.convert('1')
im.save('temp2.png')

text = pytesseract.image_to_string(im)
print(text)


matrix = []


#parsowanie do SudokuGrid
#grid = SudokuGrid(matrix)
#rozwiazanie sudoku





#ustawienie myszki
#klik myszy/klawiatury
for row in range(9):
    for col in range(9):
        m_click(x+int(col*53.5+25.5), y+int(row*53+26))
        time.sleep(0.2)
        

