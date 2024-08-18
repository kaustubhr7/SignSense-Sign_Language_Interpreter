import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time
import os

# Create directory if it doesn't exist
folder = "Data/A"
if not os.path.exists(folder):
    os.makedirs(folder)

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

offset = 20
imgSize = 300
counter = 0

while True:
    success, img = cap.read()
    if not success:
        print("Failed to grab frame")
        break

    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

            # Debugging statements
        # print(f"Hand BBox: x={x}, y={y}, w={w}, h={h}")

        # Ensure cropping coordinates are within the image dimensions
        x_min = max(x - offset, 0)
        y_min = max(y - offset, 0)
        x_max = min(x + w + offset, img.shape[1])
        y_max = min(y + h + offset, img.shape[0])

        if x_min < x_max and y_min < y_max:
            imgCrop = img[y_min:y_max, x_min:x_max]
        else:
            imgCrop = np.zeros((0, 0, 3), np.uint8)
        
        if imgCrop.size == 0:
            print("Cropped image is empty.")
            continue

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCropShape = imgCrop.shape
        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize

        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord("s"):
        counter += 1
        img_name = f'{folder}/Image_{time.time()}.jpg'
        cv2.imwrite(img_name, imgWhite)
        print(f"Image saved: {img_name}, Counter: {counter}")
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
