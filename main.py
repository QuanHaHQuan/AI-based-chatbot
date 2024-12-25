from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import time
import threading
from page import *
import QA
from recordingThread import startRecording, stopRecording
from TextToSpeech import TTS
import facerecognition
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import face_recognition
import cv2
import numpy as np
import time
import matplotlib as plt
#初始化窗口
class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        name = facerecognition.recognition()
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.output.append("hello "+name)
        TTS("hello"+name)
    
    #录音
    def MakeVoice(self):
        startRecording()
    
    #停止录音
    def EndVoice(self):
        self.plainTextEdit.setPlainText("正在回答~")
        stopRecording()
        # 转文本
        thBaiduYuYin = QA.BaiduYuYinThread()
        thBaiduYuYin.start()
        Question=thBaiduYuYin.run()
        #self.input.clear()
        self.input.append(Question)
        thBaiduYuYin.join()
        # 回答
        thQA_fun = QA.QA_funThread(Question)
        thQA_fun.start()
        Answer=thQA_fun.run()
        #self.output.clear()
        self.output.append(Answer)
        TTS(Answer)
        thQA_fun.join()
        self.plainTextEdit.setPlainText("等待问题中~")

if __name__ == '__main__':
    # 创建窗口实例
    
    app = QtWidgets.QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())