def play():
    #Import Modules
    import cv2
    import numpy as np
    import face_recognition
    import os
    from playsound import playsound

    path = 'Images'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for x in myList:
        curImg = cv2.imread(f'{path}/{x}')
        images.append(curImg)
        classNames.append(os.path.splitext(x)[0])
    print(classNames)

    #encoding the images
    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def play():
        mp3File = "tune.mp3"
        playsound(mp3File)

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                playsound("tune.mp3")
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)



        cv2.imshow('Webcam', img)
        cv2.waitKey(1)

def detect():
    # Import Modules
    import cv2
    import numpy as np
    import os

    path = 'ObjectImages'
    orb = cv2.ORB_create(nfeatures=1000)

    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        imgCur = cv2.imread(f'{path}/{cl}', 0)
        images.append(imgCur)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    def findDes(images):
        desList = []
        for img in images:
            kp, des = orb.detectAndCompute(img, None)
            desList.append(des)
        return desList

    def findID(img, desList, thres=15):
        kp2, des2 = orb.detectAndCompute(img, None)
        bf = cv2.BFMatcher()
        matchList = []
        finalVal = -1
        try:
            for des in desList:
                matches = bf.knnMatch(des, des2, k=2)
                good = []
                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good.append([m])
                matchList.append(len(good))
        except:
            pass
        # print(matchList)
        if len(matchList) != 0:
            if max(matchList) > thres:
                finalVal = matchList.index(max(matchList))
        return finalVal

    desList = findDes(images)
    print(len(desList))

    cap = cv2.VideoCapture(0)

    while True:

        success, img2 = cap.read()
        imgOriginal = img2.copy()
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        id = findID(img2, desList)
        if id != -1:
            cv2.putText(imgOriginal, classNames[id], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
            playsound("tune.mp3")
        cv2.imshow('img2', imgOriginal)
        cv2.waitKey(1)


#GUI
from tkinter import *
from PIL import ImageTk

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Find through Cam")
        self.root.geometry("1199x600+100+50")
        self.root.resizable(False, False)
        # ============================#
        self.bg = ImageTk.PhotoImage(file="front.jpg")
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        # ==============================#
        Frame_login = Frame(self.root, bg="white")
        Frame_login.place(x=150, y=150, height=360, width=700)

        title = Label(Frame_login, text="FIND THROUGH CAM", font=("Impact", 45, "bold"), fg="#FF5733",
                      bg="white").place(x=100, y=10)
        subtitle = Label(Frame_login, text="Click below button to find Missing Person",
                         font=("times new roman", 20, "bold"), fg="#FF5733", bg="white").place(x=40, y=100)
        Login_btn = Button(Frame_login, text="Click", fg="white", bg="#FF5733", font=("times new roman", 25, "bold"),
                           command=play).place(x=150, y=150)
        subtitle1 = Label(Frame_login, text="Click below button to find Missing Object",
                          font=("times new roman", 20, "bold"), fg="#FF5733", bg="white").place(x=40, y=220)
        Login_btn1 = Button(Frame_login, text="Click", fg="white", bg="#FF5733", font=("times new roman", 25, "bold"),
                            command=detect).place(x=150, y=270)



root=Tk()
obj=Login(root)
#obj=prog(root)
root.mainloop()
