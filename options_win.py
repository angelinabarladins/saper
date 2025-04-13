from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from PyQt6.uic import loadUi

class about(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("about.ui",self)
        self.setWindowIcon(QIcon("./icons/info/information.png"))
        self.setWindowTitle("Информация")
        self.ok.clicked.connect(lambda : self.close())

class opt(QDialog):
    def __init__(self):
        super().__init__()
        
        self.pos_x = 0
        self.pos_y = 0
        self.bombs = 0
         
        loadUi("option.ui",self)
        self.setFixedSize(QSize(365,197))
        self.setWindowIcon(QIcon("./icons/settings.png"))
        self.setWindowTitle("Настройки")
        
        self.GoBack.clicked.connect(lambda : self.close())
        
        self.rb1.toggled.connect(lambda : self.radio(1))
        self.rb2.toggled.connect(lambda : self.radio(2))
        self.rb3.toggled.connect(lambda : self.radio(3))
        self.rb4.toggled.connect(lambda : self.radio(5))
        
        self.s1.valueChanged.connect(lambda : self.slider_ch(1))
        self.s2.valueChanged.connect(lambda : self.slider_ch(2))
        self.s3.valueChanged.connect(lambda : self.slider_ch(3))
        
        self.s1.setMinimum(5)
        self.s2.setMinimum(5)
        self.s3.setMinimum(9)
        
        self.s2.setMaximum(27)
        self.s3.setMaximum(50)
        
        self.s2.setValue(9)
        self.s3.setValue(9)
        self.s1.setMinimum(10)
        self.rb1.setChecked(1)

    def slider_ch(self,s):
        if s==1:
            self.bombs = self.s1.value()
            self.lcd1.display(self.bombs)
            
        elif s==2:
            self.pos_y = self.s2.value()
            self.slider1_update()
            self.update_lcd()
        elif s==3:
            self.pos_x = self.s3.value()
            self.slider1_update()
            self.update_lcd()

    def slider1_update(self):
        max = (self.pos_x*self.pos_y)//3
        self.s1.setMinimum(5)
        self.s1.setMaximum(max)
        if max <self.bombs:
            self.bombs =max
            self.s1.setValue(max)
        
    def update_lcd(self):
        self.lcd1.display(self.bombs)
        self.lcd2.display(self.pos_y)
        self.lcd3.display(self.pos_x)
        
    def update_slider(self,b,x,y):
        self.s2.setValue(y)
        self.s3.setValue(x)
        self.s1.setMinimum(5)
        self.s1.setMaximum((x*y)//3)
        self.s1.setValue(b)
        
    def radio(self,n:int):
        if n in [1,2,3,4]:
            if n == 1 :
                self.pos_x,self.pos_y,self.bombs = 9,9,10          
            elif n == 2 :
                self.pos_x,self.pos_y,self.bombs = 16,16,40
            elif n == 3 :
                self.pos_x,self.pos_y,self.bombs = 30,16,99
            elif n == 4 :
                self.pos_x,self.pos_y,self.bombs = 36,25,150
            self.update_slider(self.bombs,self.pos_x,self.pos_y)
            self.slider_state(0)
            self.update_lcd()
            
        else:
            self.slider_state(1)
            self.slider1_update()
            self.update_slider(self.bombs,self.pos_x,self.pos_y)

    def slider_state(self,n):
        if n:
            self.s1.setEnabled(True) 
            self.s2.setEnabled(True) 
            self.s3.setEnabled(True)
            
            self.l1.setEnabled(True) 
            self.l2.setEnabled(True) 
            self.l3.setEnabled(True) 
        else:
            self.s1.setEnabled(False) 
            self.s2.setEnabled(False) 
            self.s3.setEnabled(False)
            
            self.l1.setEnabled(False) 
            self.l2.setEnabled(False) 
            self.l3.setEnabled(False)