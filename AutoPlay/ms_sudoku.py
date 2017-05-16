from SudokuSolver import SudokuGrid
import numpy as np
import win32gui
import win32con
import win32api
import os,time
from PIL import ImageGrab,Image, ImageEnhance, ImageFilter, ImageOps
from pytesseract import *
import pytesseract

tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

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
#m_click(__wnd__[0]+500,__wnd__[1]+550)#hard

time.sleep(2)#temp #odczekanie na zaladowanie poziomu

#rozpoznanie cyfr na siatce (komorka 51x52; odstepy 3px szerokie, 2px wysokie; co 3 komorki +1px)
#siatka x179 y127 485x485


numbers = list()

v_1 = np.mean([15583,14519])
v_2 = np.mean([17260 ,17419 ,16649 ,17473])
v_3 = np.mean([19211 ,18248 ,20182])
v_4 = np.mean([15978 ,16824])
v_5 = np.mean([17158 ,17015])
v_6 = np.mean([20940 ,20215 ,20013])
v_7 = np.mean([15934 ,16025 ,15253])
v_8 = np.mean([20658 ,21204])
v_9 = np.mean([19272 ,20116])
v_0 = 1977

v = [v_0, v_1, v_2, v_3 ,v_4 ,v_5 , v_6 , v_7, v_8 , v_9]
matrix = np.zeros((9, 9))

pad = [179, 127]
x = __wnd__[0]+pad[0]
y = __wnd__[1]+pad[1]
im = screenGrab((x, y, x+500, y+550))

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
        win32gui.EnumWindows(enumHandler, None)
        im = screenGrab((x+int(row*53.5)+padx+5, y+int(col*53)+pady+5, x+int(row*53.5)+51+padx-5,  y+int(col*53)+52+pady-5))
        #im.show()
        string = image_to_string(im, config='-psm 10 digits')
        try:
            matrix[col][row] = int(string)
        except:
            matrix[col][row] = 0


print(matrix)

#parsowanie do SudokuGrid
grid = SudokuGrid(np.array(matrix, copy=True)  )
#rozwiazanie sudoku
print(grid.trySolve())
print(grid.grid)

#ustawienie myszki
#klik myszy/klawiatury

for row in range(9):
    for col in range(9):
        if matrix[row][col] == 0:
            m_click(x+int(col*53.5+25.5), y+int(row*53+26))
            if grid.grid[row][col] == 1:
                k_click(49)
            elif grid.grid[row][col] == 2:
                k_click(50)
            elif grid.grid[row][col] == 3:
                k_click(51)
            elif grid.grid[row][col] == 4:
                k_click(52)
            elif grid.grid[row][col] == 5:
                k_click(53)
            elif grid.grid[row][col] == 6:
                k_click(54)
            elif grid.grid[row][col] == 7:
                k_click(55)
            elif grid.grid[row][col] == 8:
                k_click(56)
            elif grid.grid[row][col] == 9:
                k_click(57)
            


