from datetime import datetime
from queue import Full
from re import fullmatch
from traceback import print_tb
import cv2
import sys
import numpy
import os
import gspread
import pymysql


# connect to service account
#sa = gspread.service_account()
# open project
#sh = sa.open("faces")
# open Sheet
#wks = sh.worksheet("Sheet1")


size = 4
pStr = ''
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'
Faceid = 0
Fullname = ""
data_Dict = {}
flag = 0
Access_level_flag = -1
frame_flag = 0
face_detected_flag = 0


print("Reading Directories")
# Create a list of images and a list of corresponding names
(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        # create array of names(folder id)
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1
(width, height) = (130, 100)

# Create a Numpy array from the two lists above
(images, labels) = [numpy.array(lis) for lis in [images, labels]]


# OpenCV trains a model from the images
# NOTE FOR OpenCV2: remove '.face'
print("Training Model please wait...")
model = cv2.face.LBPHFaceRecognizer_create()
model.train(images, labels)
print("Model Training Complete")

# Saving the Record
# File needs to be created beforehand


def records(name):
    with open('records.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            time_now = datetime.now()
            tStr = time_now.strftime('%H:%M:%D')
            dStr = time_now.strftime('%d/%m/%Y')

            # Writing into file \n for new line
            f.writelines(f'{name},{tStr},{dStr},{pStr}'"\n")
            # writing data in sheets
            #wks.update('A1', {name})


# Part 2: Use fisherRecognizer on camera stream
# Fetch
face_cascade = cv2.CascadeClassifier(haar_file)
# Create variable for Webcame Access
webcam = cv2.VideoCapture(0)
# records(names)
try:
    con = pymysql.connect(host="localhost", user="root",
                          password="", database="Visitor_data")
    cur = con.cursor()
    print("Datbase connection successful")
except:
    print("Error in Database Connection")
    print("     - Terminating Pogram")
    exit()


def set_frame_flag(flag_number):
    global frame_flag
    frame_flag = flag_number
    # records(names)
    global pStr
    if frame_flag == 1:
        # pStr = ''
        pStr = 'Security Room'
        # print(pStr)
    elif frame_flag == 2:
        # pStr = ''
        pStr = 'HOD office'
        # print(pStr)
    elif frame_flag == 3:
        # pStr = ''
        pStr = 'Canteen'
        # print(pStr)
    elif frame_flag == 4:
        pStr = 'Parking-1'
        # print(pStr)
        print('frame_flag set to:', frame_flag)


def Recognise_Face(im):
    global frame_flag, face_detected_flag
    face_detected_flag = 0
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        # Try to recognize the face
        prediction = model.predict(face_resize)
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
        im_result = cv2.putText(im, "", (x-180, y-40),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        if prediction[1] < 80:
            temp = '% s - %.0f' % (names[prediction[0]], prediction[1])
            # temp1 =temp[0:1]
            details = cur.execute(
                "select fname,lname,VisitReason,post,Access_level from Visitors_Data where id=%s", temp[0:1])
            data = cur.fetchone()
            global Faceid, Fullname, data_Dict, flag
            Faceid = temp[0:1]
            Fullname = data[0] + ' ' + data[1]
            if Fullname != '':
                face_detected_flag = 1
                print(face_detected_flag)
            # data_Dict = {id: Fullname}
            # print(data_Dict)
            cv2.line(im, (x-2, y-2), (x-60, y-30), (0, 0, 0), 2)
            im_result = cv2.putText(im, "ID=" + '% s - %.0f' %
                                    (names[prediction[0]],
                                     prediction[1]), (x-180, y-40),
                                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
            # Printing Name Data
            im_result = cv2.putText(im_result, data[0] + " " + data[1], (x-180, y-10),
                                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
            # Printing Reason
            im_result = cv2.putText(im_result, "Reason- " + data[2], (x-180, y+10),
                                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
            # Printing Position
            im_result = cv2.putText(im_result, "Position- " + data[3], (x-180, y+30),
                                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
            flag = 1
        else:  # If no match
            im_result = cv2.putText(im_result, 'not recognized',
                                    (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))


def Recognise_Face_Restricted(im):
    global Access_level_flag
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        # Try to recognize the face
        prediction = model.predict(face_resize)
        if Access_level_flag is 1:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 3)
        else:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
        im_result = cv2.putText(im, "", (x-180, y-40),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        if prediction[1] < 80:
            temp = '% s - %.0f' % (names[prediction[0]], prediction[1])
            # temp1 =temp[0:1]
            details = cur.execute(
                "select fname,lname,VisitReason,post,Access_level from Visitors_Data where id=%s", temp[0:1])
            data = cur.fetchone()
            global Faceid, Fullname, data_Dict, flag
            Faceid = temp[0:1]
            Fullname = data[0] + ' ' + data[1]
            # data_Dict = {id: Fullname}
            # print(data_Dict)
            if Access_level_flag is 1:
                cv2.line(im, (x-2, y-2), (x-60, y-30), (255, 0, 0), 2)
                im_result = cv2.putText(im, "ID=" + '% s - %.0f' %
                                        (names[prediction[0]],
                                         prediction[1]), (x-180, y-40),
                                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
                # Printing Name Data
                im_result = cv2.putText(im_result, data[0] + " " + data[1], (x-180, y-10),
                                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
                # Printing Reason
                im_result = cv2.putText(im_result, "Reason- " + data[2], (x-180, y+10),
                                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
                # Printing Position
                im_result = cv2.putText(im_result, "Position- " + data[3], (x-180, y+30),
                                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
                flag = 1
                if (data[4] < 4):
                    Access_level_flag = 1
                    # print('Access_level_flag is set to 1')
                else:
                    Access_level_flag = 0
            else:
                cv2.line(im, (x-2, y-2), (x-60, y-30), (0, 0, 0), 2)
                im_result = cv2.putText(im, "ID=" + '% s - %.0f' %
                                        (names[prediction[0]],
                                         prediction[1]), (x-180, y-40),
                                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
                # Printing Name Data
                im_result = cv2.putText(im_result, data[0] + " " + data[1], (x-180, y-10),
                                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
                # Printing Reason
                im_result = cv2.putText(im_result, "Reason- " + data[2], (x-180, y+10),
                                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
                # Printing Position
                im_result = cv2.putText(im_result, "Position- " + data[3], (x-180, y+30),
                                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
                flag = 1
                if (data[4] < 4):
                    Access_level_flag = 1
                    # print('Access_level_flag is set to 1')
                else:
                    Access_level_flag = 0
        else:  # If no match
            im_result = cv2.putText(im_result, 'not recognized',
                                    (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))


# def play_notification():
#     chime.info()
#     engine.say('Hello')


# def Recognise_Face_ID(im):
#     gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#     for (x, y, w, h) in faces:
#         face = gray[y:y + h, x:x + w]
#         face_resize = cv2.resize(face, (width, height))
#         # Try to recognize the face
#         prediction = model.predict(face_resize)
#         im_result = cv2.putText(im, "", (x-180, y-40),
#                                 cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
#         if prediction[1] < 80:
#             temp = '% s - %.0f' % (names[prediction[0]], prediction[1])
#             global FaceID_restricted_area
#             FaceID_restricted_area = temp[0:1]
#             Access_level = cur.execute(
#                 "select Access_level from employee where id=%s", temp[0:1])
#             Access_level_data = cur.fetchone()
#             # print(Access_level_data[0])
#             global Access_level_flag
#             if (Access_level_data[0] < 10):
#                 Access_level_flag = 1
#                 # print('Access_level_flag is set to 1')
#             else:
#                 Access_level_flag = 0
#                 # print('Access_level_flag is set to 0')
#                 # play_notification()
#                 # engine.runAndWait()

# def getDataID():
#     return id


# def getDatafn():
#     return Fullname

def getData():
    return Faceid, Fullname


cv2.destroyAllWindows()
