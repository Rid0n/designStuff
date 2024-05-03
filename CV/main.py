import cv2
import time

cap = cv2.VideoCapture("sample.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    ret, thresh = cv2.threshold(gray, 105, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

        cv2.line(frame, (x+ int(w/2),0), (x+int(w/2),y+int(h/2)), (0, 0, 255), 2)
        cv2.line(frame, (0, y + int(h / 2)), (x + int(w / 2), y + int(h / 2)), (255, 0, 0), 2)

        frH, frW, _ = frame.shape

        distance = ( (int(frH/2) - (y+ int(h/2)))**2 + (int(frW/2) - (x + int(w / 2)))**2)**0.5

        cv2.putText(frame, "Distance from center: " + str(distance), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                    1, cv2.LINE_AA)




    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.1)

cap.release()


