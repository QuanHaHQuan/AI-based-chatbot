# -*- coding: utf-8 -*-

import PyQt5.QtGui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
import os
import random
from numpy.core.fromnumeric import argmax
import myresource_rc
import numpy as np


ACTION_SCORE=[
    [69,71,44,35,61,90,5,76,23,45,9,13,19],
    [4,9,34,23,78,8,15,32,51,21,87,6,35],
    [41,70,65,61,32,39,10,68,48,13,54,11,14],
    [12,16,24,29,73,43,54,56,76,84,91,54,32],
    [21,34,55,67,89,40,3,9,12,19,23,22,15],
    [9,14,3,98,16,93,67,95,21,22,47,1,42],
    [40,46,96,88,45,20,99,55,80,26,15,7,24],
    [32,18,71,64,6,94,51,72,85,33,54,82,43],
    [35,76,33,44,53,8,52,36,69,78,25,19,65],
    [84,74,23,97,4,79,86,2,83,60,73,17,77],
    [70,62,59,31,49,28,39,57,29,5,37,68,50],
    [90,11,48,10,12,81,66,75,27,63,61,75,27],
    [63,61,30,41,92,89,58,91,38,56,13,7,89],
]

ACTION_SCORE_array = np.array(ACTION_SCORE).reshape((13, 13))


def group_intelligence():
    a = np.zeros((52, 12))
    
    for i in range (1, 51):
        for j in range(1, 5):
            a[i][j] = np.random.randint(0, 12, 1)
    
    b = np.zeros((52, 12))
    
    for i in range(1, 51):
        for j in range(1, 4):
            
            b[i][j] = ACTION_SCORE_array[int(a[i][j])][int(a[i][j + 1])]
            
    for i in range(5, 11):
        for j in range(1, 51):
            pbest = argmax(b[j][:])
            gbest = argmax(b[:][i - 1])
            v = abs(a[j][i - 1] - a[j][i - 2])
            delta = np.random.randint(-3, 3, 1)
            v =  int(v + delta + random.random() * (pbest - a[j][i - 1]) + random.random() * (gbest - a[j][i - 1])) % 12
            a[j][i] = (a[j][i - 1] + v) % 12
            b[j][i - 1] = ACTION_SCORE[int(a[j][i - 1])][int(a[j][i])]
    
    c = np.zeros((12, 1))
    for i in range(1, 11):
        c[i] = sum(b[i])
    res = a[argmax(c)]
    
    res = res[1 : -1]
    
    return res
    
    
# Configuration file for virtual character settings
class Config():
    ROOT_DIR = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'resources')
    ACTION_DISTRIBUTION = [
        ['1', '2', '3'],
        ['4', '5', '6', '7', '8', '9', '10', '11'],
        ['12', '13', '14'],
        ['15', '16', '17'],
        ['18', '19'],
        ['20', '21'],
        ['22'],
        ['23', '24', '25'],
        ['26',  '27', '28', '29'],
        ['30', '31', '32', '33'],
        ['34', '35', '36', '37'],
        ['38', '39', '40', '41'],
        ['42', '43', '44', '45', '46']
    ]
    PET_ACTIONS_MAP = {'pet_1': ACTION_DISTRIBUTION}
    # for i in range(2, 5): PET_ACTIONS_MAP.update({'pet_%s' % i: ACTION_DISTRIBUTION})

# Window rendering
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 640)
        MainWindow.setMinimumSize(QtCore.QSize(800, 640))
        MainWindow.setMaximumSize(QtCore.QSize(800, 640))
        MainWindow.setStyleSheet("#MainWindow{border-image:url(:/bg/bachground.jpeg);}\n"
                                 "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        '''Render the virtual character'''
        self.cfg = Config()
        # Randomly load a pet
        self.pet_images, iconpath = self.randomLoadPetImages()
        # The currently displayed image, position of the pet
        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(300, 20, 800, 300))
        self.setImage(self.image, self.pet_images[0][0])
        self.image.show()
        # Variables needed for pet animation actions
        self.is_running_action = False
        self.action_images = []
        self.action_pointer = 0
        self.action_max_len = 0
        # Perform an action at intervals
        self.timer = QTimer()
        self.timer.timeout.connect(self.randomAct)
        self.timer.start(800) # Time for performing the action

        '''Render dialog box and buttons'''
        self.output = QtWidgets.QTextBrowser(self.centralwidget)
        self.output.setGeometry(QtCore.QRect(70, 300, 661, 91))
        self.output.setStyleSheet("font: 75 16pt \"微软雅黑\";\n"
"color: rgb(22, 88, 43);")
        self.output.setObjectName("output")
        self.input = QtWidgets.QTextBrowser(self.centralwidget)
        self.input.setGeometry(QtCore.QRect(70, 470, 661, 81))
        self.input.setStyleSheet("font: 75 16pt \"微软雅黑\";\n"
"color: rgb(22, 88, 43);")
        self.input.setObjectName("input")
        self.voice = QtWidgets.QPushButton(self.centralwidget)
        self.voice.setGeometry(QtCore.QRect(70, 570, 70, 41))
        self.voice.setStyleSheet("font: 75 10pt \"微软雅黑\";\n"
"color: rgb(248, 255, 178);\n"
"background-color: rgb(241, 205, 1);")
        self.voice.setObjectName("voice")
        self.voiceEnd = QtWidgets.QPushButton(self.centralwidget)
        self.voiceEnd.setGeometry(QtCore.QRect(160, 570, 70, 41))
        self.voiceEnd.setStyleSheet("font: 75 10pt \"微软雅黑\";\n"
                                 "color: rgb(248, 255, 178);\n"
                                 "background-color: rgb(241, 205, 1);")
        self.voiceEnd.setObjectName("voiceEnd")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit.setGeometry(QtCore.QRect(300, 400, 200, 40))
        self.plainTextEdit.setStyleSheet("font: 75 10pt \"微软雅黑\";\n"
"background-color: rgb(245, 255, 146);\n"
"gridline-color: transparent;\n"
"border-color: transparent;\n"
"selection-color: transparent;")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setEnabled(False)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(280, 560, 451, 61))
        self.plainTextEdit_2.setStyleSheet("font: 10pt \"微软雅黑\";\n"
"background-color: rgb(245, 255, 146);\n"
"gridline-color: transparent;\n"
"border-color: transparent;\n"
"selection-color: transparent;")
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setEnabled(False)
        self.pushButton.setGeometry(QtCore.QRect(160, 0, 500, 50))
        self.pushButton.setStyleSheet("font: 75 16pt \"华文琥珀\";\n"
"color: rgb(89, 54, 37);\n"
"background-color: transparent;\n"
"gridline-color: transparent;\n"
"border-color: transparent;\n"
"selection-color: transparent;")
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        # Signal-slot connection for the recording button; the recorded audio will be named test.wav, with a duration of 5 seconds
        self.voice.clicked.connect(lambda: MainWindow.MakeVoice())
        self.voiceEnd.clicked.connect(lambda: MainWindow.EndVoice())
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Smart AI Pikachu"))
        self.voice.setText(_translate("MainWindow", "Start Speaking"))
        self.voiceEnd.setText(_translate("MainWindow", "Stop Speaking"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "Waiting for a question~"))
        self.plainTextEdit_2.setPlainText(_translate("MainWindow", "Click the button to use your microphone to record audio and chat with Pikachu~"))
        self.pushButton.setText(_translate("MainWindow", "Welcome to start chatting with Smart AI Pikachu!"))

    # Perform a random action
    def randomAct(self):
        if not self.is_running_action:
            self.action_seq = group_intelligence()
            for i in self.action_seq:
                self.is_running_action = True
                self.action_images = self.pet_images[int(i)]
                self.action_max_len = len(self.action_images)
                self.action_pointer = 0
        self.runFrame()

    # Complete each frame of the action
    def runFrame(self):
        if self.action_pointer == self.action_max_len:
            self.is_running_action = False
            self.action_pointer = 0
            self.action_max_len = 0
        self.setImage(self.image, self.action_images[self.action_pointer])
        self.action_pointer += 1

    # Set the currently displayed image
    def setImage(self, label, image):
        label.setPixmap(QPixmap.fromImage(image))

    # Load all images of a desktop pet
    def randomLoadPetImages(self):
        cfg = self.cfg
        pet_name = random.choice(list(cfg.PET_ACTIONS_MAP.keys()))
        actions = cfg.PET_ACTIONS_MAP[pet_name]
        pet_images = []
        for action in actions:
            pet_images.append(
                [self.loadImage(os.path.join(cfg.ROOT_DIR, pet_name, 'shime' + item + '.png')) for item in action])
        iconpath = os.path.join(cfg.ROOT_DIR, pet_name, 'shime1.png')
        return pet_images, iconpath

    # Load an image
    def loadImage(self, imagepath):
        image = QImage()
        image.load(imagepath)
        return image
