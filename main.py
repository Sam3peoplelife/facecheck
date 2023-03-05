import cv2
import pickle
import checking
from win11toast import toast

faces = cv2.CascadeClassifier("faces.xml")
login = str(input("register or login?"))
if login == "register":
    nameID = checking.register()
    count = 0
    cap = cv2.VideoCapture(0)
    cap.set(3, 500)
    cap.set(4, 500)
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        results = faces.detectMultiScale(img_gray, scaleFactor=2, minNeighbors=4)
        for (x, y, w, h) in results:
            count+=1
            name = "./faces/"+nameID+"/"+str(count)+".jpg"
            cv2.imwrite(name, img_gray)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)
        cv2.imshow("FaceControl", img)

        if (cv2.waitKey(1) & 0xFF == ord('q')) or count == 200:
            break
    print("You are registered")
    print("You can login now")
elif login == "login":
    nameID = checking.login()
    nameID = nameID.replace(" ", "-")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")


    with open("labels.pickle", "rb") as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}

    cap = cv2.VideoCapture(0)
    cap.set(3, 500)
    cap.set(4, 400)
    count = 0
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        results = faces.detectMultiScale(gray, scaleFactor=2, minNeighbors=4)
        for (x, y, w, h) in results:
            count += 1
            color_gray = gray[y:y + h, x:x + h]
            person_id, conf = recognizer.predict(color_gray)
            if conf >= 50:
                name = labels[person_id]
                if name == nameID and count == 10:
                    toast("You are logged into system", "Welcome " + nameID)
                    cap.release()
                    cv2.destroyAllWindows()
                elif count >= 100:

                    toast("You are not logged into system", "Bye!")
                    cap.release()
                    cv2.destroyAllWindows()

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)

        cv2.imshow("Face", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    print("Invalid string. Try again")

cap.release()
cv2.destroyAllWindows()