# Main.py will be responsible for the front-end part
import cv2
import time
from emailing import send_email
import glob
import os
from threading import Thread

# Starting the webcam of the laptop (can be modified to any camera)
video = cv2.VideoCapture(0)  # 0 to only use the main camera
time.sleep(1)  # to avoid the black frames

first_frame = None
status_list = []
count = 1


def clean_folder():
    images = glob.glob('Images/*.png')  # getting the list of images into a list
    for image in images:
        os.remove(image)


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
            cv2.imwrite(f'Images/{count}.png', frame)  # capturing images
            count += count
            all_images = glob.glob('Images/*.png')  # List of the images
            index = int(len(all_images) / 2)  # Selecting the image in the middle
            selected_image = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]  # only taking the last 2 values

    if status_list[0] == 1 and status_list[1] == 0:  # The moment the object has just exited the frame
        email_thread = Thread(target=send_email, args=(selected_image,))  # Creating a new thread
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder())  # Creating a new thread
        clean_thread.daemon = True

        email_thread.start()


    cv2.imshow('Video', frame)

    key = cv2.waitKey(1)  # capturing the keyboard press 'q'

    if key == ord('q'):
        break

video.release()
clean_thread.start()


# print(check1)  # True
# print(frame1)  # numpy matrix representing the image captured
