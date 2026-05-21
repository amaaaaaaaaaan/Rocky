import cv2

stream="http://192.168.1.55/stream"

cap=cv2.VideoCapture(stream)

while True:
    ret,frame=cap.read()
    if not ret:
        print("oops")
        break
    cv2.imshow('stream',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()