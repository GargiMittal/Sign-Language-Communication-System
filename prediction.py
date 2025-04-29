import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import pyttsx3
import time

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speaking rate
engine.setProperty('volume', 1.0)  # Set volume to maximum

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("smnist.h5", "labels.txt")

offset = 20
imgSize = 300
labels = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z'
]


previous_label = None  # To avoid repeating the same label
label_timestamp = None  # To track when the label was first detected
stable_duration = 2  # Time duration to wait for a stable sign (3 seconds)

while True:
    success, img = cap.read()
    if not success:
        continue

    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        # Ensure cropping boundaries are within the image
        y1 = max(0, y - offset)
        y2 = min(img.shape[0], y + h + offset)
        x1 = max(0, x - offset)
        x2 = min(img.shape[1], x + w + offset)

        imgCrop = img[y1:y2, x1:x2]

        if imgCrop.size == 0:
            continue  # Skip if the cropped image is empty

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

        aspectRatio = h / w

        try:
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wGap + wCal] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hGap + hCal, :] = imgResize

            prediction, index = classifier.getPrediction(imgWhite, draw=False)

            label = labels[index]

            # If the label is the same as the previous one, check for stability
            if label == previous_label:
                if label_timestamp is None:
                    label_timestamp = time.time()  # Start timer when label is stable
                elif time.time() - label_timestamp >= stable_duration:
                    # If the label has been stable for 3 seconds, speak it
                    print(f"Detected: {label}")
                    engine.say(label)  # Queue the label to be spoken
                    engine.runAndWait()  # Speak queued phrases
                    label_timestamp = None  # Reset the timer after speaking

            else:
                # Reset timer when the label changes
                previous_label = label
                label_timestamp = None  # Reset timer when label changes

            # Draw information on the screen
            cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                          (x - offset + 90, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
            cv2.putText(imgOutput, label, (x, y - 26),
                        cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
            cv2.rectangle(imgOutput, (x - offset, y - offset),
                          (x + w + offset, y + h + offset), (255, 0, 255), 4)

            cv2.imshow("ImageCrop", imgCrop)
            cv2.imshow("ImageWhite", imgWhite)

        except Exception as e:
            print(f"Error during resizing or classification: {e}")

    cv2.imshow("Image", imgOutput)

    # Stop the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
