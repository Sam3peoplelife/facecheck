import os
import cv2
import numpy as np
from PIL import Image
import pickle


BASE_DIR = os.path.dirname(os.path.abspath((__file__)))

img_dir = os.path.join(BASE_DIR, "faces")
facescascade = cv2.CascadeClassifier("faces.xml")

recognizer = cv2.face.LBPHFaceRecognizer_create()

person_id = 0
label_of_id = {}
y_labels = []
x_train = []
for root, dirs, files in os.walk(img_dir):
    for file in files:
        if file.endswith("jpg"):
            path = os.path.join(root,file)
            label = os.path.basename(root).replace(" ", "-").lower()

        if not label in label_of_id:
            person_id += 1
            label_of_id[label] = person_id

        person_id = label_of_id[label]

        pil_image = Image.open(path).convert("L")
        size = (500,500)
        final_image = pil_image.resize(size, Image.ANTIALIAS)
        image_array = np.array(final_image, "uint8")

        faces = facescascade.detectMultiScale(image_array, scaleFactor = 2, minNeighbors = 4)

        for x,y,w,h in faces:
            rect = image_array[y:y+h, x:x+w]
            x_train.append(rect)
            y_labels.append(person_id)

with open("labels.pickle", "wb") as f:
    pickle.dump(label_of_id, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainer.yml")
print(label_of_id)
