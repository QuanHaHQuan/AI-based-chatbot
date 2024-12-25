# -*- coding: utf-8 -*-
import win32com.client as win


def TTS(text: str = ""):
    speak = win.Dispatch("SAPI.SpVoice")
    speak.Speak(text)
