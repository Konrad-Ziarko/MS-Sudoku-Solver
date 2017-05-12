from __future__ import print_function
import numpy as np
import os,sys
import time
from colorama import init, Fore, Back, Style
import threading
from msvcrt import getch
init(autoreset=False)
from ctypes import *



STD_OUTPUT_HANDLE = -11
 
class COORD(Structure):
    pass
 
COORD._fields_ = [("X", c_short), ("Y", c_short)]
debug = False
isRunning = True

def printColoredSudoku(before, testData):
    for i in range (0,9):
        for j in range (0,9):
            if before[i][j] == testData[i][j] and before[i][j] != 0:
                print(Fore.GREEN + str(testData[i][j]), end="")
            elif testData[i][j] == 0:
                print(Fore.RED + str(testData[i][j]), end="")
            else:
                print(Fore.LIGHTCYAN_EX + str(testData[i][j]), end="")
            
            if (j+1) % 3 == 0:
                print("|", end="")
        if (i+1) % 3 == 0:
                print()
                print("--"*6, end="")
        print ("")


def print_at(r, c, s):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
 
    c = s.encode("windows-1252")
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)


class SingleCell:
    def __init__(self, x, y, houseNumber, row, col, house, missingInRow, missingInColumn, missingInHouse):
        self.me = 0
        self.x = x
        self.y = y
        self.houseNumber = houseNumber
        self.row = row
        self.column = col
        self.house = house
        self.missingInRow = missingInRow
        self.missingInColumn = missingInColumn
        self.missingInHouse = missingInHouse
        self.potencialNumbers = []
        self.clearLists()

    def simpleCheck(self):
        if len(self.missingInColumn) == 1:
            self.me = self.missingInColumn[0]
        elif len(self.missingInHouse) == 1:
            self.me = self.missingInHouse[0]
        elif len(self.missingInRow) == 1:
            self.me = self.missingInRow[0]
        else:
            return False
        return True

    def clearLists(self):
        for removeValue in self.column:
            try:
                self.missingInRow.remove(removeValue)
            except ValueError:
                pass
            try:
                self.missingInHouse.remove(removeValue)
            except ValueError:
                pass
        for removeValue in self.row:
            try:
                self.missingInColumn.remove(removeValue)
            except ValueError:
                pass
            try:
                self.missingInHouse.remove(removeValue)
            except ValueError:
                pass
        for removeValue in self.house:
            for removeValue2 in removeValue:
                try:
                    self.missingInRow.remove(removeValue2)
                except ValueError:
                    pass    
                try:
                    self.missingInColumn.remove(removeValue2)
                except ValueError:
                    pass


class SudokuGrid:
    def __init__(self, grid):
        self.grid = grid
        self.cells = []
        for i in range (0,9):
            for j in range (0,9):
                if self.grid[i, j] == 0:
                    missingInRow = [1,2,3,4,5,6,7,8,9]
                    row = self.grid[i, :]
                    for removeValue in row:
                        try:
                            missingInRow.remove(removeValue)
                        except ValueError:
                            pass
                    if len(missingInRow) == 1:
                        self.grid[i,j] = missingInRow[0]
                    else:
                        missingInColumn = [1,2,3,4,5,6,7,8,9]
                        column = self.grid[:, j]
                        for removeValue in column:
                            try:
                                missingInColumn.remove(removeValue)
                            except ValueError:
                                    pass
                        if len(missingInColumn) == 1:
                            self.grid[i,j] = missingInColumn[0]
                        else:
                            houseNumber = [0, 0]
                            if i > 2:
                                if i > 5:
                                    houseNumber[0]=2
                                else:
                                    houseNumber[0]=1
                            if j > 2:
                                if j > 5:
                                    houseNumber[1]=2
                                else:
                                    houseNumber[1]=1
                            house = self.grid[houseNumber[0]*3:3+houseNumber[0]*3, houseNumber[1]*3:3+houseNumber[1]*3]
                            missingInHouse = [1,2,3,4,5,6,7,8,9]
                            for i2 in range (0+houseNumber[0]*3,3+houseNumber[0]*3):
                                for j2 in range (0+houseNumber[1]*3,3+houseNumber[1]*3):
                                    try:
                                        missingInHouse.remove(self.grid[i2, j2])
                                    except ValueError:
                                        pass
                            if len(missingInHouse) == 1:
                                self.grid[i,j] = missingInHouse[0]
                            else:
                                self.cells.append(SingleCell(i, j, houseNumber, row, column, house, missingInRow, missingInColumn, missingInHouse))
    def trySolve(self):
        breakNextLoop = False
        for loops in range(0,90):
            if breakNextLoop:
                break
            breakNextLoop = True
            breakLoop = False
            for i in range(0, 20):
                if breakLoop:
                    if debug:
                        print("simple", i)
                    break
                breakLoop = True
                for obj in self.cells:
                    obj.clearLists()
                    if obj.simpleCheck():
                        breakLoop = False
                        self.grid[obj.x, obj.y] = obj.me
                        self.cells.remove(obj)

            breakLoop = False
            for i in range(0, 20):
                if breakLoop:
                    if debug:
                        print("missing", i)
                    break
                breakLoop = True
                for obj in self.cells:
                    obj.clearLists()
                    if obj.simpleCheck():
                        self.grid[obj.x, obj.y] = obj.me
                        self.cells.remove(obj)
                        continue
                    obj.potencialNumbers = list(set(obj.missingInHouse).intersection(set(obj.missingInColumn).intersection(obj.missingInRow)))
                    for obj2 in self.cells:
                        if obj2.houseNumber == obj.houseNumber and obj2!=obj:
                            
                            """obj.potencialNumbers = list(set(obj.potencialNumbers).intersection(set(obj.missingInHouse).intersection(set(obj.missingInColumn).intersection(obj.missingInRow))))"""
                            obj2.potencialNumbers = list(set(obj2.missingInHouse).intersection(set(obj2.missingInColumn).intersection(obj2.missingInRow)))
                            obj.potencialNumbers = list(set(obj.potencialNumbers).difference(obj2.potencialNumbers))
                            if len(obj.potencialNumbers) == 0:
                                break
                    if len(obj.potencialNumbers)==1:
                        obj.potencialNumbers = list(set(obj.potencialNumbers).intersection(set(obj.missingInHouse).intersection(set(obj.missingInColumn).intersection(obj.missingInRow))))
                        if len(obj.potencialNumbers)==1:
                            breakLoop = False
                            self.grid[obj.x, obj.y] = obj.me = obj.potencialNumbers[0]
                            self.cells.remove(obj)
            
            
            for i in range (0,9):
                for j in range (0,9):
                    if self.grid[i,j] == 0:
                        breakNextLoop=False;
                        break
                if not breakNextLoop:
                    break

        if debug:
            print("loops", loops)
        for i in range (0,9):
            test = set(self.grid[i, :])
            if len(test) != 9:
                return False
        for i in range (0,9):
            test = set(self.grid[:, i])
            if len(test) != 9:
                return False
        return True;

    def animatedSolve(self):
        breakNextLoop = False
        for loops in range(0,10):
            if breakNextLoop:
                break
            if not isRunning:
                return "Interrupted"
            breakNextLoop = True
            breakLoop = False
            for i in range(0, 20):
                if breakLoop:
                    """print("simple", i)"""
                    break
                breakLoop = True
                for obj in self.cells:
                    obj.clearLists()
                    if obj.simpleCheck():
                        breakLoop = False
                        self.grid[obj.x, obj.y] = obj.me
                        if abortable_sleep(1):
                            pass
                        if not isRunning:
                            return "Interrupted"
                        print_at(obj.x+obj.houseNumber[0], obj.y+obj.houseNumber[1], str(obj.me))
                        self.cells.remove(obj)

            breakLoop = False
            for i in range(0, 20):
                if breakLoop:
                    """print("missing", i)"""
                    break
                if not isRunning:
                    return "Interrupted"
                breakLoop = True
                for obj in self.cells:
                    obj.clearLists()
                    if obj.simpleCheck():
                        self.grid[obj.x, obj.y] = obj.me
                        if abortable_sleep(1):
                            pass
                        print_at(obj.x+obj.houseNumber[0], obj.y+obj.houseNumber[1], str(obj.me))
                        self.cells.remove(obj)
                        continue
                    obj.potencialNumbers = list(set(obj.missingInHouse).intersection(set(obj.missingInColumn).intersection(obj.missingInRow)))
                    for obj2 in self.cells:
                        if obj2.houseNumber == obj.houseNumber and obj2!=obj:
                            """obj.potencialNumbers = list(set(obj.potencialNumbers).intersection(set(obj.missingInHouse).intersection(set(obj.missingInColumn).intersection(obj.missingInRow))))"""
                            obj2.potencialNumbers = list(set(obj2.missingInHouse).intersection(set(obj2.missingInColumn).intersection(obj2.missingInRow)))
                            obj.potencialNumbers = list(set(obj.potencialNumbers).difference(obj2.potencialNumbers))
                            if len(obj.potencialNumbers) == 0:
                                        break
                    if len(obj.potencialNumbers)==1:
                        obj.potencialNumbers = list(set(obj.potencialNumbers).intersection(set(obj.missingInHouse).intersection(set(obj.missingInColumn).intersection(obj.missingInRow))))
                        if len(obj.potencialNumbers)==1:
                            breakLoop = False
                            self.grid[obj.x, obj.y] = obj.me = obj.potencialNumbers[0]
                            if abortable_sleep(1):
                                pass
                            print_at(obj.x+obj.houseNumber[0], obj.y+obj.houseNumber[1], str(obj.me))
                            self.cells.remove(obj)
            
            
            for i in range (0,9):
                for j in range (0,9):
                    if self.grid[i,j] == 0:
                        breakNextLoop=False;
                        break
                if not breakNextLoop:
                    break

        print_at(15,0, "ESC to exit\n")
        """print("loops", loops)"""
        for i in range (0,9):
            test = set(self.grid[i, :])
            if len(test) != 9:
                return False
        for i in range (0,9):
            test = set(self.grid[:, i])
            if len(test) != 9:
                return False
        return True;
            


if __name__ == '__main__':
    testData5 = np.array([[1,4,0,2,0,8,5,0,7],[9,0,8,0,0,0,0,0,0],[0,5,6,1,0,3,9,2,8],[3,6,1,0,5,4,2,8,0],[8,7,0,0,2,0,0,5,0],[5,9,2,0,0,0,0,0,0],[0,3,0,9,0,2,7,0,4],[2,8,0,0,3,1,6,9,0],[4,1,0,0,6,7,8,0,2]])

    testData4 = np.array([[0,0,0,5,0,0,0,0,0],[7,5,4,3,6,1,2,0,0],[3,0,0,0,0,0,0,7,6],[8,0,9,4,1,0,6,0,3],[6,3,0,7,0,9,1,0,0],[0,4,0,0,8,0,9,5,0],[5,1,0,9,0,8,0,0,2],[0,0,0,0,0,0,0,0,0],[2,9,0,0,4,7,8,6,0]])

    testData3 = np.array([[7,0,0,8,4,0,9,0,0],[0,0,1,0,0,0,0,0,0],[9,3,0,0,0,0,8,6,4],[0,0,0,0,7,0,3,0,8],[0,0,6,9,1,0,4,7,0],[0,8,0,0,3,0,0,0,6],[0,5,0,1,0,0,0,0,9],[4,0,9,0,0,3,0,0,1],[0,0,0,0,0,6,0,0,7]])

    testData2 = np.array([[5,0,0,0,0,0,0,0,1],[2,6,0,0,0,0,0,0,3],[0,0,0,0,0,0,9,0,0],[0,4,0,5,0,0,0,7,0],[7,1,0,0,0,4,0,0,0],[6,2,0,0,1,9,0,5,4],[0,7,4,0,9,5,0,0,2],[0,0,0,8,0,0,0,0,7],[0,0,0,0,0,2,3,0,8]])

    #testData = np.array([[9,0,0,0,0,0,0,0,1],[0,5,0,0,7,0,6,0,0],[1,0,0,0,0,0,7,0,5],[0,0,4,7,2,0,0,0,0],[0,0,0,5,4,6,1,3,0],[6,2,0,9,0,8,0,0,0],[0,7,0,3,0,0,2,0,4],[2,1,0,6,0,0,0,7,0],[0,0,6,0,0,0,5,1,3]])

    testData = np.array([[9,0,0,0,0,0,0,0,1],[0,5,0,0,7,0,6,0,0],[1,0,0,0,0,0,7,0,5],[0,0,4,7,2,0,0,0,0],[0,0,0,5,4,6,1,3,0],[6,2,0,9,0,8,0,0,0],[0,7,0,3,0,0,2,0,4],[2,1,0,6,0,0,0,7,0],[0,0,6,0,0,0,5,1,3]])
    

    fromFile = testData
    obj = SudokuGrid(fromFile)



    """
    delimiterChar = input('Insert delimiter char and press Enter\n')
    os.system('cls')
    fileName = input('Insert file name\n');
    os.system('cls')
    try:
        fromFile = np.genfromtxt(fileName, dtype=(int), delimiter=delimiterChar)
    except:
        sys.exit()

    print_at(0,15, "Press any button and hop to next step")
    print_at(1,15, "Press ESC to exit")
    print_at(0,0,"")
    if len(fromFile) != 9:
        sys.exit()
    for i in range (0,9):
        try:
            if len(fromFile[i]) != 9:
                sys.exit()
        except:
            sys.exit()

    for i in range (0,9):
        for j in range (0,9):
            if fromFile[i][j] == 0:
                print(Fore.WHITE, end="")
            else:
                print(Fore.GREEN, end="")
            print(fromFile[i][j], end="")
            if (j+1) % 3 == 0:
                print(Fore.MAGENTA, end="")
                print("|", end="")
        if (i+1) % 3 == 0:
                print()
                print(Fore.MAGENTA, end="")
                print("--"*6, end="")
        print ("")

    print(Fore.LIGHTCYAN_EX)
    before = np.array(fromFile)


    obj = SudokuGrid(fromFile)
    class AbortableSleep():
        def __init__(self):
            self.isRunning = True
            self._condition = threading.Condition()

        def __call__(self, secs):
            with self._condition:
                self._aborted = False
                self._condition.wait(timeout=secs)
                return not self._aborted

        def abort(self):
            with self._condition:
                self._condition.notify()
                self._aborted = True

    
    abortable_sleep = AbortableSleep()
    th = threading.Thread(target=obj.animatedSolve)
    th.start()
    while True:
        key = ord(getch())
        abortable_sleep.abort()
        if key == 27: #ESC
            isRunning = False
            print_at(15,0, "")
            break

    """
    start_time = time.time()
    print(obj.trySolve())
    print(time.time() - start_time, "\n")
    #"""


