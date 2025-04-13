from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QAction
from random import *
from time import *
import threading

from options_win import *
import welcomee
import json
import os

class StatsManager:
    def __init__(self, filename="stats.json"):
        self.filename = filename
        self.stats = {"games_played": 0, "games_won": 0, "games_lost": 0, "best_time": None}
        self.load_stats()

    def load_stats(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                self.stats = json.load(file)

    def save_stats(self):
        with open(self.filename, "w") as file:
            json.dump(self.stats, file, indent=4)

    def update_stats(self, won, time=None):
        self.stats["games_played"] += 1
        if won:
            self.stats["games_won"] += 1
            if self.stats["best_time"] is None or (time is not None and time < self.stats["best_time"]):
                self.stats["best_time"] = time
        else:
            self.stats["games_lost"] += 1
        self.save_stats()
        print(f"Updating stats: won={won}, time={time}, current_best_time={self.stats['best_time']}")

def nums(n: int):
    style = ''
    if n == 1:
        style = "color: blue;"
    elif n == 2:
        style = "color: green;"
    elif n == 3:
        style = "color: red;"
    elif n == 4:
        style = "color: violet;"
    elif n == 5:
        style = "color: black;"
    elif n == 6:
        style = "color: yellow;"
    elif n == 7:
        style = "color: pink;"
    elif n == 8:
        style = "color: brown;"

    return "font-weight: bold;" + style

class ResetButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(QIcon('./icons/characters/Tech.png'))
        self.setIconSize(QtCore.QSize(60, 26))
        self.clicked.connect( self.Reset)

    def Reset(self):
        for y in range(window.sizeY):
            for x in range(window.sizeX):
                window.items[y][x].SetVal(None)
                window.items[y][x].setText(" ")
                window.items[y][x].setEnabled(True)
                window.items[y][x].Flag(0)

        window.FirstMove = 1
        window.ingame = 1
        window.BombRest = window.sizeY*window.sizeX-window.sizeBomb
        window.FlagRest = window.sizeBomb
        window.DispBomb.display(window.FlagRest)
        window.ClearBombs()
        window.DispTime.reset()
        self.setIcon(QIcon('./icons/characters/Tech.png'))

    def win(self):
        self.setIcon(QIcon('./icons/win/win5.png'))
    def lose(self):
        self.setIcon(QIcon('./icons/characters/techk.png'))

class Timer(QLCDNumber):
    def __init__(self):
        super().__init__()
        self.__counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.increment)

    def reset(self):
        self.display(0)
        self.__counter = 0
        self.timer.stop()

    def start(self):
        self.timer.start(1000)

    def stop(self):
        self.timer.stop()

    def increment(self):
        self.__counter += 1
        self.display(self.__counter)

    def GetScore(self):
        return self.__counter

class btn(QPushButton):
    def __init__(self,x,y):
        super().__init__()
        self.__value=None
        self.__flag=0
        self.x,self.y=x,y
        self.setText(" ")
        self.setEnabled(True)
        self.setFixedSize(25,25)

    def mousePressEvent(self, event):
        if window.ingame:
            if event.button() == Qt.MouseButton.LeftButton:
                window.rec_reveal(self.x,self.y,1)

            elif event.button() == Qt.MouseButton.RightButton:
                if not self.__flag:
                    window.FlagRest-=1
                    window.DispBomb.display(window.FlagRest)
                    self.Flag(1)
                else:
                    window.FlagRest+=1
                    window.DispBomb.display(window.FlagRest)
                    self.Flag(0)

    def Flag(self,b):
        if b:
            self.__flag=1
            self.setText("")
            self.setIcon(QIcon('./icons/flags/flag1.png'))
            self.setIconSize(QtCore.QSize(20, 20))
        else:
            self.__flag=0
            self.setText(" ")
            self.setIcon(QIcon(''))

    def GetFlag(self):
        return self.__flag

    def SetVal(self,val):
        self.__value=val
        self.setStyleSheet(nums(val))

    def GetVal(self):
        return self.__value



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.FirstMove=1
        self.ingame=1
        self.option_window=0

        self.sizeX,self.sizeY=9,9
        self.sizeBomb = 10
        self.BombRest = self.sizeX*self.sizeX-self.sizeBomb
        self.FlagRest = self.sizeBomb
        self.stats_manager = StatsManager()

        self.items=[[btn(x,y) for x in range(self.sizeX)] for y in range(self.sizeY)]
        self.__bombs=[]
        self.setFixedSize(QSize())
        self.setWindowTitle("Сапёр")
        self.setWindowIcon(QIcon("./icons/bombs/mine1.png"))
        with open("./style.css","r") as fh:
            self.setStyleSheet(fh.read())

        self.toolbar = QToolBar("My main toolbar")
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)
        self.settings = QAction("Настройки",self)
        self.settings.triggered.connect(self.optins_win)
        self.toolbar.addAction(self.settings)
        self.stats = QAction("Статистика", self)
        self.stats.triggered.connect(self.show_stats)
        self.toolbar.addAction(self.stats)
        self.about = QAction("Информация",self)
        self.about.triggered.connect(self.about_win)
        self.toolbar.addAction(self.about)

        self.DispTime = Timer()
        self.MButton= ResetButton()

        self.DispBomb = QLCDNumber()
        self.DispBomb.display(str(self.FlagRest))

        self.spacer1 = QSpacerItem(20, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.spacer2 = QSpacerItem(20, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        layout1 = QGridLayout()
        layout1.addWidget(self.DispTime,0,0)
        layout1.addWidget(self.MButton,0,2)
        layout1.addWidget(self.DispBomb,0,4)
        layout1.setObjectName("l1")

        layout1.addItem(self.spacer1,0,1)
        layout1.addItem(self.spacer2,0,3)

        self.layout2 = QGridLayout()
        self.layout2.setSpacing(0)
        self.layout2.setContentsMargins(0,0,0,0)
        self.layout2.setObjectName("l2")

        for x in range(self.sizeX):
            for y in range(self.sizeY):
                self.layout2.addWidget(self.items[y][x], y+1, x+1)

        self.MainLayout = QVBoxLayout()
        self.MainLayout.addLayout(layout1)
        self.MainLayout.addLayout(self.layout2)
        self.MainLayout.setObjectName("l3")

        widget = QWidget()
        widget.setLayout(self.MainLayout)
        self.setCentralWidget(widget)

    def show_stats(self):
        stats_dialog = StatsDialog(self.stats_manager.stats, self)
        stats_dialog.exec()

    def NewSettings(self,NewX,NewY,NewB) :
        if (NewB==self.sizeBomb and NewX==self.sizeX and NewY==self.sizeY ):
            self.MButton.Reset()
            return

        for x in range(self.sizeX):
            for y in range(self.sizeY):
                self.layout2.removeWidget(self.items[y][x])
                self.items[y][x].deleteLater()
        self.items.clear()
        self.sizeX,self.sizeY,self.sizeBomb=NewX,NewY,NewB
        self.items=[[btn(x,y) for x in range(self.sizeX)] for y in range(self.sizeY)]
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                self.layout2.addWidget(self.items[y][x], y+1, x+1)
        self.MButton.Reset()
        self.setFixedSize(QSize())
        self.move(QPoint())

    def optins_win(self):
        self.option_window=1
        self.OptWin = opt()
        self.OptWin.apply.clicked.connect(lambda : self.NewSettings(self.OptWin.pos_x,self.OptWin.pos_y, self.OptWin.bombs))
        self.OptWin.GoBack.clicked.connect(lambda: self.NewSettings(self.OptWin.pos_x, self.OptWin.pos_y, self.OptWin.bombs))
        self.OptWin.exec()
        self.option_window = 0

    def about_win(self):
        self.option_window=1
        self.AboutWin = about()
        self.AboutWin.exec()
        self.option_window = 0

    def rec_reveal(self,x=0,y=0,first_call=0):
        if self.FirstMove:
            self.FirstMove=0
            self.MakeBombs(x,y)
            self.SetValues()
            self.DispTime.start()

        if self.items[y][x].GetFlag() :
            return

        if self.items[y][x].GetVal()=="*":
            if first_call: self.lose()
            return

        if self.items[y][x].text()!=" " :
            return

        elif int(self.items[y][x].GetVal())>0:
            self.items[y][x].setText( str(self.items[y][x].GetVal()) )
            self.items[y][x].setEnabled(False)
            window.BombRest-=1
            if not window.BombRest: self.win()
            return

        elif self.items[y][x].GetVal()==0 :
            self.items[y][x].setText( "  " )
            self.items[y][x].setEnabled(False)
            window.BombRest-=1
            if not window.BombRest: self.win()

            if (x+1<self.sizeX): self.rec_reveal(x+1,y)
            if (x-1>=0): self.rec_reveal(x-1,y)
            if (y+1<self.sizeY): self.rec_reveal(x,y+1)
            if (y-1>=0): self.rec_reveal(x,y-1)

            if (x-1>=0 and y-1>=0): self.rec_reveal(x-1,y-1)
            if (x+1<self.sizeX and y+1<self.sizeY): self.rec_reveal(x+1,y+1)
            if (x-1>=0 and y+1<self.sizeY): self.rec_reveal(x-1,y+1)
            if (x+1<self.sizeX and y-1>=0): self.rec_reveal(x+1,y-1)


    def SetValues(self):
        for y in range(self.sizeY):
            for x in range(self.sizeX):

                if( self.items[y][x].GetVal()=="*"):continue
                count=0

                if( y>=1 and x>=1 and self.items[y-1][x-1].GetVal()=="*"): count+=1

                if( y>=1 and self.items[y-1][x].GetVal()=="*"): count+=1

                if( y>=1 and (x+1)<self.sizeX and self.items[y-1][x+1].GetVal()=="*"): count+=1

                # =================================================

                if( (y+1)<self.sizeY and x>=1 and self.items[y+1][x-1].GetVal()=="*"): count+=1

                if( (y+1)<self.sizeY and self.items[y+1][x].GetVal()=="*"): count+=1

                if( (y+1)<self.sizeY and (x+1)<self.sizeX and self.items[y+1][x+1].GetVal()=="*"): count+=1


                if( x>=1 and self.items[y][x-1].GetVal()=="*"): count+=1

                if( (x+1)<self.sizeX and self.items[y][x+1].GetVal()=="*"): count+=1

                self.items[y][x].SetVal(count)


    def MakeBombs(self,x,y):
        c = self.sizeBomb
        while c:
            tempx,tempy=randint(0,self.sizeX-1),randint(0,self.sizeY-1)

            if(abs(tempy-y)<=1 and abs(tempx-x)<=1): continue
            if self.items[tempy][tempx].GetVal()!="*":
                # print(f"bomeb[{c}] ({tempy};{tempx})")
                self.items[tempy][tempx].SetVal("*")
                self.__bombs.append([tempy,tempx])
                c-=1
    def ClearBombs(self):
        window.__bombs.clear()

    def win(self):
        self.ingame = 0
        self.DispTime.stop()
        self.DispBomb.display(0)
        self.stats_manager.update_stats(won=True, time=self.DispTime.GetScore())
        for x in self.__bombs:
            self.items[x[0]][x[1]].setText("")
            self.items[x[0]][x[1]].setIcon(QIcon('./icons/flags/flag1.png'))
            self.items[x[0]][x[1]].setIconSize(QtCore.QSize(20, 20))
        self.MButton.win()
        print(f"Winning time: {self.DispTime.GetScore()}")

    def lose(self):
        self.ingame = 0
        self.DispTime.stop()
        self.stats_manager.update_stats(won=False)
        for x in self.__bombs:
            self.items[x[0]][x[1]].setText("")
            self.items[x[0]][x[1]].setIcon(QIcon('./icons/bombs/mine1.png'))
            self.items[x[0]][x[1]].setIconSize(QtCore.QSize(16, 16))
        self.MButton.lose()


class StatsDialog(QDialog):
    def __init__(self, stats, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Статистика")
        layout = QVBoxLayout()

        games_played = QLabel(f"Игр сыграно: {stats['games_played']}")
        games_won = QLabel(f"Игр выиграно: {stats['games_won']}")
        games_lost = QLabel(f"Игр проиграно: {stats['games_lost']}")
        best_time = QLabel(f"Лучшее время: {stats['best_time']} сек" if stats['best_time'] else "Лучшее время: N/A")

        layout.addWidget(games_played)
        layout.addWidget(games_won)
        layout.addWidget(games_lost)
        layout.addWidget(best_time)

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class WelcomeWindow(QDialog, welcomee.Ui_dialog):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window
        self.playButton.clicked.connect(self.start_game)

    def start_game(self):
        self.close()
        self.main_window.show()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    welcome = WelcomeWindow(window)
    welcome.show()
    app.exec()