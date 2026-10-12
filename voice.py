import pyttsx3

speak= pyttsx3.init()

speak.setProperty('voice',"en-US-GuyNeural")
speak.setProperty('rate',130)

speak.say("Hi Amori!, This is rocky")
speak.runAndWait()

