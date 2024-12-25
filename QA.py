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

REC_QUESTION_WAV = "recQuestion.wav"               # 提问生成的录音文件的文件名

BaiduYuYinResult = ""  # 语音识别的结果
thBaiduYuYin = threading.Thread()  # 语音识别线程
thBaiduYuYin.start()
thBaiduYuYin.join()

class BaiduYuYinThread(threading.Thread):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        global BaiduYuYinResult
        try:
            RATE = "16000"  # 采样率16KHz
            FORMAT = "wav"  # wav格式
            CUID = "wate_play"
            DEV_PID = "1536"  # 无标点普通话
            TOKEN = "24.8daf91b870cbf45e8f523ee4088edf2f.2592000.1642993060.282335-25410851"
            # 以字节格式读取文件之后进行编码
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
            BaiduYuYinResult = "识别不清"
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
        lines = f.read().splitlines()  # 读取全部内容 ，并以列表方式返回
        for line in lines:
            res = re.search('[?]', line)
            if (res):
                q = re.sub("\d+[.]\t", '', line)
                question.append(q)
            elif (len(line) != 0):
                answer.append(line)

        # 通过有道翻译将输入的问题转换为英文
        data = {
            'doctype': 'json',
            'type': 'AUTO',
            'i': self.text
        }
        url = "http://fanyi.youdao.com/translate"
        r = requests.get(url, params=data)
        result = r.json()
        qua = result['translateResult'][0][0]['tgt']

        # 将问题和问题库通过词向量进行编码转换
        qua_embedding = self.model.encode(qua)
        Q_embeddings = self.model.encode(question)

        res = 0
        res_sen = -1

        # 计算问题库中和提出问题最为相似的数据
        for encod, i in zip(Q_embeddings, range(0, len(question))):
            sim = util.pytorch_cos_sim(Q_embeddings[i], qua_embedding)
            if res < sim:
                res = sim
                res_sen = i
        # 从数据集中抽取对应的question和context, 进行抽取式的问答
        ans = self.question_answerer({
            'question': question[res_sen],
            'context': answer[res_sen]
        })

        final_ans = ans['answer']
        return final_ans
