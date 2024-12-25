import requests
import base64
import os
import json
import threading
import sys
import ctypes
from sentence_transformers import SentenceTransformer, util
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import re
from recordingThread import startRecording, stopRecording
from TextToSpeech import TTS

REC_QUESTION_WAV = "recQuestion.wav"               # The filename for the recorded question

BaiduYuYinResult = ""  # Result of speech recognition
thBaiduYuYin = threading.Thread()  # Speech recognition thread
thBaiduYuYin.start()
thBaiduYuYin.join()

class BaiduYuYinThread(threading.Thread):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        global BaiduYuYinResult
        try:
            RATE = "16000"  # Sampling rate of 16KHz
            FORMAT = "wav"  # wav format
            CUID = "wate_play"
            DEV_PID = "1536"  # Plain Mandarin without punctuation
            TOKEN = "24.8daf91b870cbf45e8f523ee4088edf2f.2592000.1642993060.282335-25410851"
            # Encode the file in byte format after reading
            with open(REC_QUESTION_WAV, "rb") as f:
                speech = base64.b64encode(f.read()).decode("utf8")
            size = os.path.getsize(REC_QUESTION_WAV)
            headers = {"Content-Type": "application/json"}
            url = "https://vop.baidu.com/server_api"
            data = {
                "format": FORMAT,
                "rate": RATE,
                "dev_pid": DEV_PID,
                "speech": speech,
                "cuid": CUID,
                "len": size,
                "channel": 1,
                "token": TOKEN,
            }
            req = requests.post(url, json.dumps(data), headers)
            result = json.loads(req.text)
            BaiduYuYinResult = result["result"][0][:-1]
        except:
            BaiduYuYinResult = "Recognition unclear"
        return BaiduYuYinResult

final_ans = ""
thQA_fun = threading.Thread()
thQA_fun.start()
thQA_fun.join()

class QA_funThread(threading.Thread):
    model=[]
    question_answere=[]
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        model_name = "./roberta-base-squad2"
        self.model = SentenceTransformer('distilbert-base-nli-mean-tokens')
        self.question_answerer = pipeline('question-answering', 
                                          model = model_name, tokenizer = model_name)
    def run(self):
        global final_ans
        question = []
        answer = []
        question.append('')
        answer.append('')
        f = open("./Q&A pair _en.txt", "r")
        lines = f.read().splitlines()  # Read all content and return it as a list
        for line in lines:
            res = re.search('[?]', line)
            if (res):
                q = re.sub("\d+[.]\t", '', line)
                question.append(q)
            elif (len(line) != 0):
                answer.append(line)

        # Translate the input question to English using Youdao translation
        data = {
            'doctype': 'json',
            'type': 'AUTO',
            'i': self.text
        }
        url = "http://fanyi.youdao.com/translate"
        r = requests.get(url, params=data)
        result = r.json()
        qua = result['translateResult'][0][0]['tgt']

        # Encode the question and question bank using word embeddings
        qua_embedding = self.model.encode(qua)
        Q_embeddings = self.model.encode(question)

        res = 0
        res_sen = -1

        # Calculate the most similar data in the question bank to the posed question
        for encod, i in zip(Q_embeddings, range(0, len(question))):
            sim = util.pytorch_cos_sim(Q_embeddings[i], qua_embedding)
            if res < sim:
                res = sim
                res_sen = i
        # Extract the corresponding question and context from the dataset for extractive question answering
        ans = self.question_answerer({
            'question': question[res_sen],
            'context': answer[res_sen]
        })

        final_ans = ans['answer']
        return final_ans
