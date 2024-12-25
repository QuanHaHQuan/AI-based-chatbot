# AI-based-chatbot (Madrain Version)
## Introduction
This project is a virtual chatbot for Beijing Institute of Technology, implemented using artificial intelligence techniques such as artificial neural networks, machine learning, swarm intelligence, and symbolic intelligence. The key features of the system are as follows:

* It can recognize the presence of a person in front of the camera and greet them actively.
* It can engage in natural voice communication with people about the situation at Beijing Institute of Technology, understanding what the person says and responding appropriately with corresponding voice output.
* It has a virtual image and animated actions.

The core Q&A part of this project is built using a close-domain extraction-based question answering system based on Transformer and BERT models. The database contains 135 manually constructed Q&A entries related to Beijing Institute of Technology. The facial recognition part of the project uses the deep learning model Face Recognition, which captures facial images at specific times, encodes and compares feature values to determine the best matching identity. The virtual image is made up of frame-by-frame animation sequences, combining swarm intelligence and symbolic intelligence algorithms, using a score-based connection between actions to determine the optimal action sequence for display.

## Installation Guide
Before running the project, please install the required libraries according to the information in the code and configure the necessary environment. This project is developed using Python 3.7.

You need to download:

roberta-base-squad2 model

distilbert-base-nli-mean-tokens model

The required models for the question-answering system are stored in ./distilbert-base-nli-mean-tokens and ./roberta-base-squad2. The whl file for PyAudio compatible with Python 3.7 is ./PyAudio-0.2.11-cp37-cp37m-win_amd64.whl. Other library files can be directly downloaded via pip install.

This project requires access to the computer's microphone and camera, so please ensure that these peripherals are functioning correctly.

## Usage Instructions
To run the main program, enter python main.py in the command line. Ensure that your face is directly in front of the camera. If a clear face is not detected, the system will display a message indicating that no face was found. The program's window will appear once a clear face is captured.

Facial data is stored in the facial_info folder. If a face is not in the dataset, it will be recognized as an unknown person. After recognizing the face, the main program will start, and the virtual character will greet you.

Click the "Start Talking" button below to activate the microphone for recording. 

You can ask the AI questions related to Beijing Institute of Technology in Madrain, such as "Who is the president of Beijing Institute of Technology?", "How many academicians does Beijing Institute of Technology have?", "How many students does Beijing Institute of Technology have?", and "What is the ranking of Beijing Institute of Technology?" 

For a complete list of questions, refer to the question set in Q&A pair_en.txt. After finishing the question, click the "Stop Talking" button. Wait a moment, and the AI will respond vocally.
