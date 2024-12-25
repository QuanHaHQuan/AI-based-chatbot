# -*- coding: utf-8 -*-
import pyaudio
import wave
import threading

CHUNK_SIZE = 1024                    # wav文件是由若干个CHUNK组成的，CHUNK我们就理解成数据包或者数据片段。
FORMAT = pyaudio.paInt16             # 这个参数后面写的pyaudio.paInt16表示我们使用量化位数 16位来进行录音。
CHANNELS = 1                         # 代表的是声道，这里使用的单声道。
SAMPLE_RATE = 16000                  # 采样率16k
REC_QUESTION_WAV = "recQuestion.wav" # 输出文件名

isRecording = False                  # 是否正在录音
pya = pyaudio.PyAudio()
pyaStream = 0
pyaFrames = []
thRec = threading.Thread()           # 录音线程
thRec.start()
thRec.join()


class recordingThread(threading.Thread):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        global isRecording, pya, pyaStream, pyaFrames
        pya = pyaudio.PyAudio()
        pyaStream = pya.open(rate=SAMPLE_RATE,
                             channels=CHANNELS,
                             format=FORMAT,
                             input=True,
                             frames_per_buffer=CHUNK_SIZE)
        pyaFrames = []
        while isRecording:
            data = pyaStream.read(CHUNK_SIZE)
            pyaFrames.append(data)


def startRecording():
    global thRec, isRecording
    isRecording = True
    thRec = recordingThread()
    thRec.start()


def stopRecording():
    global thRec, isRecording, pya
    isRecording = False
    thRec.join()
    pyaStream.stop_stream()
    pyaStream.close()
    pya.terminate()
    wf = wave.open(REC_QUESTION_WAV, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pya.get_sample_size(FORMAT))
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(pyaFrames))
    wf.close()
