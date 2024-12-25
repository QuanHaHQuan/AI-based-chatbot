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

# Initialize the window
class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        name = facerecognition.recognition()
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.output.append("hello " + name)
        TTS("hello" + name)
    
    # Start recording
    def MakeVoice(self):
        startRecording()
    
    # Stop recording
    def EndVoice(self):
        self.plainTextEdit.setPlainText("Answering~")
        stopRecording()
        # Convert to text
        thBaiduYuYin = QA.BaiduYuYinThread()
        thBaiduYuYin.start()
        Question = thBaiduYuYin.run()
        #self.input.clear()
        self.input.append(Question)
        thBaiduYuYin.join()
        # Respond
        thQA_fun = QA.QA_funThread(Question)
        thQA_fun.start()
        Answer = thQA_fun.run()
        #self.output.clear()
        self.output.append(Answer)
        TTS(Answer)
        thQA_fun.join()
        self.plainTextEdit.setPlainText("Waiting for the question~")

if __name__ == '__main__':
    # Create window instance
    app = QtWidgets.QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
