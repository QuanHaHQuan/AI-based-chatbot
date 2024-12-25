# -*- coding: utf-8 -*-
import pyaudio
import wave
import threading

CHUNK_SIZE = 1024                    # The wav file is composed of several CHUNKS, which can be understood as data packets or data fragments.
FORMAT = pyaudio.paInt16             # This parameter pyaudio.paInt16 means we use 16-bit quantization for recording.
CHANNELS = 1                         # Represents the audio channel, here using mono.
SAMPLE_RATE = 16000                  # Sampling rate 16k
REC_QUESTION_WAV = "recQuestion.wav" # Output file name

isRecording = False                  # Whether recording is in progress
pya = pyaudio.PyAudio()
pyaStream = 0
pyaFrames = []
thRec = threading.Thread()           # Recording thread
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
