import ollama
import cv2
import base64
import numpy as np
import socket
import threading

cap = cv2.VideoCapture('http://192.168.0')
current_frame = None
cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
lock=threading.Lock()
message=""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9999))
server.listen(1)

def encode_frame(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

def ask_rocky(frame, question):
    image_data = encode_frame(frame)
    response = ollama.chat(
        model='llama3.2-vision',
        messages=[{
            'role': 'user',
            'content': question,
            'images': [image_data]
        }]
    )
    print("Rocky:", response['message']['content'])

def listen():
    global message
    with lock:
        conn, addr = server.accept()
        script = conn.recv(1024).decode()
        message=script
        print(f"Received: {message}")

while True:
    thread=threading.Thread(target=listen,daemon=True)
    thread.start()

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        break
    face= cascade.detectMultiScale(frame,1.1)
    for x,y,w,h in face:
        cv2.rectangle(frame, (x,y), (x+w,y+h),(0,0,255),1)
        cv2.circle(frame,(x+w//2,y+h//2),1,(255,0,0),3)
    
    text=message
    if text:
        print(text)

    cv2.putText(frame,text,(50,50),1,2.0,(0,255,255),2,cv2.LINE_4)
    
    cv2.imshow('Rocky Eyes', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()