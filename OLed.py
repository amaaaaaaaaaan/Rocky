import cv2
import numpy as np
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

esp_ip="192.168.1.107"
port=12345

capture=cv2.VideoCapture("YTDown.com_YouTube_The-Odyssey-Official-New-Trailer_Media_f_bKjZeJBBI_001_1080p.mp4")

while True:
    ret,frame=capture.read()
    flip=cv2.flip(frame,1)
    bw=cv2.cvtColor(flip,cv2.COLOR_BGR2GRAY)
    _,threshold=cv2.threshold(bw,127,255,cv2.THRESH_BINARY)
    #frame=frame.flatten()
    resize=cv2.resize(threshold,(128,64),interpolation=cv2.INTER_AREA)
    packing=np.packbits(resize>0)

    if len(packing)==1024:
        sock.sendto(packing.tobytes(),(esp_ip,port))
    if not ret:
        break
    cv2.imshow("aaaaa",threshold)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()
