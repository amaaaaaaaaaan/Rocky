# client.py
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9999))
a=input("Message: ")
client.send(a.encode())
client.close()

#

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9999))
server.listen(1)

recognizer = sr.Recognizer()
model = whisper.load_model("tiny")

print("Waiting for message...")

conn, addr = server.accept()
message = conn.recv(1024).decode()
print(f"Received: {message}")
conn.close()