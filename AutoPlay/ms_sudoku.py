from SudokuSolver import SudokuGrid
import win32gui
import win32con
import win32api
import os

from PIL import ImageGrab

__window_title__ = 'Microsoft Sudoku' 
__wnd__ = []

def screenGrab(box):
    im = ImageGrab.grab(box)
    #im.save(os.getcwd() + '\\full_snap__' + 'test1' + '.png', 'PNG')
    

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


def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)


win32gui.EnumWindows(enumHandler, None)
click(__wnd__[0]+500,__wnd__[1]+550)#hard

#odczekanie na zaladowanie poziomu

#siatka x179 y127 485x485

#rozpoznanie cyfr na siatce (komorka 51x52; odstepy 3px szerokie, 2px wysokie)

#parsowanie do SudokuGrid

#rozwiazanie sudoku

#ustawienie myszki
#klik myszy/klawiatury