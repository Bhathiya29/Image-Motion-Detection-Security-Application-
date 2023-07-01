# Main.py will be responsible for the front-end part
import cv2
import time
from emailing import send_email

# Starting the webcam of the laptop (can be modified to any camera)
video = cv2.VideoCapture(0)  # 0 to only use the main camera
time.sleep(1)  # to avoid the black frames

first_frame = None
status_list = []


while True:

    status = 0
    check, frame = video.read()  # camera turned on and off
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # converting the pixels to gray scale to make things efficient
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 22), 0)  # 21 22 amount of blurriness standard deviation 0

    if first_frame is None:  # Storing the very first frame so we can compare the next frames
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)  # comparing the difference

    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]  # if the pixel has 30 or more we
    # reassign 255

    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    cv2.imshow('My Video', dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # detecting the
    # contours around the wide areas

    for contour in contours:  # Ignoring Fake detections
        if cv2.contourArea(contour) < 10000:  # detecting any changes
            continue
        x, y, w, h = cv2.boundingRect(contour)  # getting the coordinate for a rectangle detection
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)  # The original color frame
        if rectangle.any():
            status = 1

    status_list.append(status)
    status_list = status_list[-2:]  # only taking the last 2 values

    if status_list[0] ==1 and status_list[1] == 0:  # The moment the object has exited the frame
        send_email()


    cv2.imshow('Video', frame)

    key = cv2.waitKey(1)  # capturing the keyboard press 'q'

    if key == ord('q'):
        break

video.release()

# print(check1)  # True
# print(frame1)  # numpy matrix representing the image captured
