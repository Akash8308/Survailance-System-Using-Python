from cProfile import label
from pickle import TRUE
from re import X
from sqlite3 import Row
from sys import flags
import tkinter as tk
from tkinter.tix import COLUMN
from warnings import catch_warnings
import cv2
import PIL.Image
import PIL.ImageTk
import time
import datetime as dt
import argparse
import face_recognize
import pyttsx3
import chime
import threading

# Alert
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 145)

chime.theme('mario')

data_Dict = dict()
data_Dict1 = dict()
data_Dict_red = dict()
log_string = ''
log_string_alert = ''
voiceLine = ''


class App:
    def __init__(self, window, window_title, video_source=0, video_source1=1, video_source2=2, video_source3=3):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("850x850")
        self.video_source = video_source
        self.video_source1 = video_source1
        self.video_source2 = video_source2
        self.video_source3 = video_source3
        self.ok = False
        self.vid = VideoCapture(self.video_source)
        self.vid1 = VideoCapture(self.video_source1)
        self.vid2 = VideoCapture(self.video_source2)
        self.vid3 = VideoCapture(self.video_source3)

        # Create a canvas that can fit the above video source size

        self.simulation_Time_panel = tk.Frame(bg="Black")
        self.simulation_Time_panel.pack(
            side=tk.TOP, fill=tk.X)
        self.simulation_Side_panel_2 = tk.Frame(bg="Black")
        self.simulation_Side_panel_2.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.simulation_Side_panel_1 = tk.Frame(bg='black')
        self.simulation_Side_panel_1.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.simulation_panel_1 = tk.Frame(bg="Black")
        self.simulation_panel_1.pack(side=tk.TOP, fill=tk.BOTH)
        self.simulation_panel_2 = tk.Frame(bg="Black")
        self.simulation_panel_2.pack(side=tk.LEFT, fill=tk.BOTH)

        self.canvas_1 = tk.Canvas(
            self.simulation_panel_1, width=self.vid.width, height=self.vid.height)
        self.canvas_1.pack(side='left', padx=1, pady=1)
        self.canvas_2 = tk.Canvas(
            self.simulation_panel_1, width=self.vid.width, height=self.vid.height)
        self.canvas_2.pack(side='left', padx=1, pady=1)
        self.canvas_3 = tk.Canvas(
            self.simulation_panel_2, width=self.vid.width, height=self.vid.height)
        self.canvas_3.pack(side='left', padx=1, pady=1)
        self.canvas_4 = tk.Canvas(
            self.simulation_panel_2, width=self.vid.width, height=self.vid.height)
        self.canvas_4.pack(side='left', padx=1, pady=1)

        # Button that lets the user take a snapshot
        # self.btn_snapshot = tk.Button(
        #     self.simulation_Side_panel_2, text="Snapshot")
        # self.btn_snapshot.pack()

        # Label to display the Title
        self.lbl_title = tk.Label(
            self.simulation_Time_panel, text="Live feed",  bg='black', fg='white', font="Calibri, 20")
        self.lbl_title.pack(side='left',  padx=20, pady=20)

        # Label to display the Date
        # Time
        date = dt.datetime.now()
        self.label = tk.Label(
            self.simulation_Time_panel, text=f"{date:%A, %B %d, %Y}",  bg='black', fg='white', font="Calibri, 20")
        self.label.pack(side='right',  padx=20, pady=20)

        # Label for log
        self.label_log_Header_detected_faces = tk.Label(
            self.simulation_Side_panel_1, text='Detected Faces', font="Calibri, 20", bg='black', fg='white')
        self.label_log_Header_detected_faces.pack(
            side=tk.TOP,  padx=1, pady=1)

        self.label_log_Header_threat = tk.Label(
            self.simulation_Side_panel_2, text='Threats', font="Calibri, 20", bg='black', fg='white')
        self.label_log_Header_threat.pack(
            side=tk.TOP,  padx=1, pady=1, fill=tk.X)

        self.label_log_id = tk.Label(
            self.simulation_Side_panel_1,  font="Calibri, 20", padx=2, pady=2, wraplengt=200, bg='black', fg='white')
        self.label_log_id.pack()
        self.label_log_id_Alert = tk.Label(
            self.simulation_Side_panel_2,  font="Calibri, 20", padx=2, pady=2, wraplengt=200, bg='black', fg="RED")
        self.label_log_id_Alert.pack()

        # quit button
        self.btn_quit = tk.Button(
            self.simulation_Side_panel_2, text='QUIT', command=self.terminateProgram)
        self.btn_quit.pack(padx=1, pady=2, side='bottom')

        # stop alert
        self.btn_stop = tk.Button(
            self.simulation_Side_panel_2, text='STOP ALERT', command=self.Access_level_flag_stop)
        self.btn_stop.pack(padx=1, pady=2, side='bottom')
        # # get data
        # self.btn_getdata = tk.Button(
        #     self.simulation_Side_panel_2, text='Get Data', command=self.getData)
        # self.btn_quit.pack(padx=1, pady=2, side='bottom')

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 33
        self.update()

        self.window.mainloop()

    def getData(self):
        print("working")

    def Access_level_flag_stop(self):
        face_recognize.Access_level_flag = 0

    def terminateProgram(self):
        exit()

    def update(self):
        # Get a frame from the video source
        ret_1, ret_2, ret_3, ret_4, frame_1, frame_2, frame_3, frame_4 = self.vid.get_frame()

        if self.ok:
            self.vid.out.write(cv2.cvtColor(frame_1, cv2.COLOR_RGB2BGR))
            self.vid1.out.write(cv2.cvtColor(frame_2, cv2.COLOR_RGB2BGR))
            self.vid2.out.write(cv2.cvtColor(frame_3, cv2.COLOR_RGB2BGR))
            self.vid3.out.write(cv2.cvtColor(frame_4, cv2.COLOR_RGB2BGR))

        if ret_1 & ret_2 & ret_3 & ret_4:
            # face_recognize.Recognise_Face(frame_1)
            face_recognize.set_frame_flag(1)
            face_recognize.Recognise_Face_Restricted(frame_1)
            face_recognize.set_frame_flag(2)
            face_recognize.Recognise_Face(frame_2)
            # face_recognize.Recognise_Face_Restricted(frame_2)
            face_recognize.set_frame_flag(3)
            face_recognize.Recognise_Face(frame_3)
            # face_recognize.Recognise_Face_Restricted(frame_3)
            face_recognize.set_frame_flag(4)
            face_recognize.Recognise_Face(frame_4)
            # face_recognize.Recognise_Face_Restricted(frame_4)

            frame_1 = cv2.putText(frame_1, "Security Room", (10, 40),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0))
            self.photo_1 = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame_1))
            self.canvas_1.create_image(
                0, 0, image=self.photo_1, anchor=tk.NW)
            frame_2 = cv2.putText(frame_2, "HOD office", (10, 40),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0))
            self.photo_2 = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame_2))
            self.canvas_2.create_image(
                0, 0, image=self.photo_2, anchor=tk.NW)

            frame_3 = cv2.putText(frame_3, "Canteen", (10, 40),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0))
            self.photo_3 = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame_3))
            self.canvas_3.create_image(
                0, 0, image=self.photo_3, anchor=tk.NW)
            frame_4 = cv2.putText(frame_4, "Parking-1", (10, 40),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0))
            self.photo_4 = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame_4))
            self.canvas_4.create_image(
                0, 0, image=self.photo_4, anchor=tk.NW)

            global data_Dict, data_Dict1, log_string, log_string_alert, voiceLine
            id, fn = face_recognize.getData()
            data_Dict[id] = fn
            for id in data_Dict:
                if id in data_Dict1:
                    continue
                else:
                    data_Dict1[id] = fn
                    if face_recognize.flag is 1:
                        log_string += str(id) + ": " + fn + "\n"
                        voiceLine = 'Detected ' + 'ID' + id + 'name' + fn
                        self.label_log_id.config(text=log_string)
                        self.notification(voiceLine)
                        t2 = threading.Thread(target=engine.runAndWait)
                        t2.start()
                        face_recognize.flag = 0
                        face_recognize.records(face_recognize.names)
                if id in data_Dict_red:
                    continue
                else:
                    if face_recognize.Access_level_flag is 1:
                        data_Dict_red[id] = fn
                        log_string_alert += str(id) + ": " + fn + "\n"
                        self.label_log_id_Alert.config(
                            text=log_string_alert)
            if face_recognize.Access_level_flag is 1:
                voiceLine_alert = 'Alert! ' + fn + 'is not allowed in this area'
                # update threat log
                self.notification(voiceLine_alert)
        self.window.after(self.delay, self.update)

    def notification(self, voiceLine):
        chime.info()
        engine.say(voiceLine)
        t3 = threading.Thread(target=engine.runAndWait)
        t3.start()


class VideoCapture:
    def __init__(self, video_source=0, video_source1=1):
        # Open the video source
        self.vid = cv2.VideoCapture(0)
        self.vid1 = cv2.VideoCapture(1)
        self.vid2 = cv2.VideoCapture(2)
        self.vid3 = cv2.VideoCapture(3)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        if not self.vid1.isOpened():
            raise ValueError("Unable to open video source", video_source1)
        if not self.vid2.isOpened():
            raise ValueError("Unable to open video source", video_source1)
        if not self.vid3.isOpened():
            raise ValueError("Unable to open video source", video_source1)

        # Command Line Parser
        args = CommandLineParser().args

        # create videowriter

        # 1. Video Type
        VIDEO_TYPE = {
            'avi': cv2.VideoWriter_fourcc(*'XVID'),
            # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
            'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        }

        self.fourcc = VIDEO_TYPE[args.type[0]]

        # 2. Video Dimension
        STD_DIMENSIONS = {
            '480p': (640, 480),
            '720p': (1280, 720),
            '1080p': (1920, 1080),
            '4k': (3840, 2160),
        }
        res = STD_DIMENSIONS[args.res[0]]
        print(args.name, self.fourcc, res)
        self.out = cv2.VideoWriter(
            args.name[0]+'.'+args.type[0], self.fourcc, 10, res)

        # set video sourec width and height
        self.vid.set(3, res[0])
        self.vid.set(4, res[1])
        self.vid1.set(3, res[0])
        self.vid1.set(4, res[1])
        self.vid2.set(3, res[0])
        self.vid2.set(4, res[1])
        self.vid3.set(3, res[0])
        self.vid3.set(4, res[1])

        # Get video source width and height
        self.width, self.height = res

    # To get frames

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            ret1, frame1 = self.vid1.read()
            ret2, frame2 = self.vid2.read()
            ret3, frame3 = self.vid3.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, ret1, ret2, ret3,  cv2.cvtColor(frame, cv2.COLOR_RGB2BGR), cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR), cv2.cvtColor(frame2, cv2.COLOR_RGB2BGR), cv2.cvtColor(frame3, cv2.COLOR_RGB2BGR))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            # self.out.release()
            cv2.destroyAllWindows()


class CommandLineParser:

    def __init__(self):

        # Create object of the Argument Parser
        parser = argparse.ArgumentParser(description='Script to record videos')

        # Create a group for requirement
        # for now no required arguments
        # required_arguments=parser.add_argument_group('Required command line arguments')

        # Only values is supporting for the tag --type. So nargs will be '1' to get
        parser.add_argument('--type', nargs=1, default=[
                            'avi'], type=str, help='Type of the video output: for now we have only AVI & MP4')

        # Only one values are going to accept for the tag --res. So nargs will be '1'
        parser.add_argument('--res', nargs=1, default=[
                            '480p'], type=str, help='Resolution of the video output: for now we have 480p, 720p, 1080p & 4k')

        # Only one values are going to accept for the tag --name. So nargs will be '1'
        parser.add_argument(
            '--name', nargs=1, default=['output'], type=str, help='Enter Output video title/name')

        # Parse the arguments and get all the values in the form of namespace.
        # Here args is of namespace and values will be accessed through tag names
        self.args = parser.parse_args()


def main():
    # Create a window and pass it to the Application object
    App(tk.Tk(), 'RTS')


print('Starting...')
main()
