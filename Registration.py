from asyncio.windows_events import NULL
from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk
import pymysql
import cv2
import sys
import numpy
import os
import re


haar_file = 'haarcascade_frontalface_default.xml'

# Global variable
# sub_data = 'Akash'

# All the faces data will be
# present this folder
datasets = 'datasets'


class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Page")  # For Title of the page
        # Resolution of the page top, bottom
        self.root.geometry("1350x900+0+0")
        self.root.config(bg="white")
        self.Access_level = 0
        self.Id = ''
        self.new_ID = 0

        # ===BackGround Image===
        self.bg = ImageTk.PhotoImage(file="images/back.png")
        bg = Label(self.root, image=self.bg).place(
            x=0, y=0, relwidth=1, relheight=1)
        # ===Side Image===
        self.left = ImageTk.PhotoImage(file="images/side.jpg")
        left = Label(self.root, image=self.left).place(
            x=250, y=250, width=230, height=230)

        # ===Register Frame===
        frame1 = Frame(self.root, bg="white")
        frame1.place(x=480, y=85, width=700, height=650)

        # ====Footer Frame=====
        footer = Frame(self.root, bg="gray")
        footer.place(x=0, y=750, relwidth=1, relheight=30)

        footer_name = Label(footer, text="Created by Group-1",
                            font=("comic sans ms", 25, "bold"), bg="gray", fg="#ECF0F1").place(x=700, y=12)

        title = Label(frame1, text="Registration", font=(
            "times new roman", 20, "bold"), bg="white", fg="green").place(x=270, y=15)

        # --------ID Row
        self.Db_con()
        User_ID = Label(frame1, text="ID", font=(
            "times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=60)
        # self.txt_User_ID = Entry(frame1, font=(
        #     "times new roman", 15), bg="lightgray",  state="disabled")
        txt_User_ID = Label(frame1, text=self.new_ID, font=(
            "times new roman", 15, "bold"), bg="white", fg="gray").place(x=250, y=60)
        # self.txt_User_ID.place(x=220, y=60, width=250)
        # --------First Row
        f_name = Label(frame1, text="First Name", font=(
            "times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=100)
        self.txt_fname = Entry(frame1, font=(
            "times new roman", 15), bg="lightgray")
        self.txt_fname.place(x=220, y=100, width=250)

        # --------Second Raw
        l_name = Label(frame1, text="Last Name", font=(
            "times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=140)
        self.txt_lname = Entry(frame1, font=(
            "times new roman", 15), bg="lightgray")
        self.txt_lname.place(x=220, y=140, width=250)

        # --------3rd Raw
        user_name = Label(frame1, text="User Name", font=(
            "times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=180)
        self.txt_username = Entry(frame1, font=(
            "times new roman", 15), bg="lightgray")
        self.txt_username.place(x=220, y=180, width=250)

        # -------Contact
        contact = Label(frame1, text="Contact No ", font=(
            "times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=220)
        self.txt_contact = Entry(frame1, font=(
            "times new roman", 15), bg="lightgray")
        self.txt_contact.place(x=220, y=220, width=250)

        # -------Email
        email = Label(frame1, text="Email", font=(
            "times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=260)
        self.txt_email = Entry(frame1, font=(
            "times new roman", 15), bg="lightgray")
        self.txt_email.place(x=220, y=260, width=250)

        # -------Age
        age = Label(frame1, text="Age", font=("times new roman", 15,
                    "bold"), bg="white", fg="gray").place(x=50, y=300)
        self.txt_age = Entry(frame1, font=(
            "times new roman", 15), bg="lightgray")
        self.txt_age.place(x=220, y=300, width=250)

        # -------Gender
        gender = Label(frame1, text="Gender", font=(
            "times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=340)
        self.cmb_gender = ttk.Combobox(frame1, font=(
            "times new roman", 13), state='readonly', justify=CENTER)
        self.cmb_gender['values'] = ("Male", "Female", "Other")
        self.cmb_gender.place(x=220, y=340, width=250)
        self.cmb_gender.current(0)

        # ---------Password
        password = Label(frame1, text="Password", font=(
            "times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=380)
        self.txt_password = Entry(
            frame1, show="*", font=("times new roman", 15), bg="lightgray")
        self.txt_password.place(x=220, y=380, width=250)

        # --------Confirm Password
        cpassword = Label(frame1, text="Confirm Password", font=(
            "times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=420)
        self.txt_cpassword = Entry(
            frame1, show="*", font=("times new roman", 15), bg="lightgray")
        self.txt_cpassword.place(x=220, y=420, width=250)

        # -------Reason
        reason = Label(frame1, text="Reason", font=(
            "times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=460)
        self.txt_reason = Entry(frame1, font=(
            "times new roman", 15), bg="lightgray")
        self.txt_reason.place(x=220, y=460, width=250)

        # -------Post
        pos = Label(frame1, text="Position", font=("times new roman",
                    15, "bold"), bg="white", fg="gray").place(x=50, y=500)
        self.txt_pos = ttk.Combobox(frame1, font=(
            "times new roman", 13), state='readonly', justify=CENTER)
        self.txt_pos['values'] = (
            "Professor", "Staff", "Student", "Visitor")
        self.txt_pos.place(x=220, y=500, width=250)

        # --------Terms
        self.var_chk = IntVar()
        chk = Checkbutton(frame1, text="I Agree the Terms & Conditions ", variable=self.var_chk,
                          onvalue=1, offvalue=0, bg="white", font=("times new roman", 12)).place(x=50, y=540)

        # # Register_face Button
        self.btn_img = ImageTk.PhotoImage(file="images/register.jpg")
        btn_register = Button(frame1, image=self.btn_img, bd=0,
                              cursor="hand2", command=self.register_data).place(x=50, y=570)

        # -------Sign in Button-----
        btn_login = Button(self.root, text="Sign In", command=self.login_window, font=(
            "times new roman", 20), bd=0, cursor="hand2").place(x=320, y=480)

    def login_window(self):
        self.root.destroy()
        import login

    def Db_con(self):
        con = pymysql.connect(
            host="localhost", user="root", password="", database="visitor_data")
        cur = con.cursor()
        cur.execute("select max(ID) from visitors_data")
        Id_data = cur.fetchone()
        Id_data = Id_data[0]
        self.new_ID = int(Id_data) + 1
        # print(self.new_ID)

    def clear_data(self):
        self.txt_User_ID.delete(0, END)
        self.txt_fname.delete(0, END)
        self.txt_lname.delete(0, END)
        self.txt_username.delete(0, END)
        self.txt_contact.delete(0, END)
        self.txt_email.delete(0, END)
        self.txt_age.delete(0, END)
        self.cmb_gender.current(0)
        self.txt_password.delete(0, END)
        self.txt_cpassword.delete(0, END)
        self.txt_reason.delete(0, END)

    def numberValidation(self, s):
        phonePattern = re.compile("(0|91)?[6-9][0-9]{9}")
        return phonePattern.match(s)

    def mailValidation(self, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.fullmatch(regex, email)

    def set_access_level(self):
        Position = self.txt_pos.get()
        if Position == "Professor":
            self.Access_level = 4
        elif Position == "Staff":
            self.Access_level = 3
        elif Position == "Student":
            self.Access_level = 2
        elif Position == "Visitor":
            self.Access_level = 1

    def register_data(self):
        self.set_access_level()

        if self.txt_fname.get() == "" or self.txt_lname.get() == "" or self.txt_username.get() == "" or self.txt_contact.get() == "" or self.txt_email.get() == "" or self.txt_age.get() == "" or self.cmb_gender.get() == "" or self.txt_password.get() == "" or self.txt_cpassword.get() == "" or self.txt_reason.get() == "":
            messagebox.showerror(
                "Error !", "All Fields are Required !", parent=self.root)
        elif not self.numberValidation(self.txt_contact.get()):
            messagebox.showerror(
                "Error !", "Invalid Number", parent=self.root)
        elif not self.mailValidation(self.txt_email.get()):
            messagebox.showerror(
                "Error !", "Invalid Email", parent=self.root)
        elif self.txt_password.get() != self.txt_cpassword.get():
            messagebox.showerror(
                "Error !", "Password Didn't Match !", parent=self.root)
        elif self.var_chk.get() == 0:
            messagebox.showerror(
                "Error !", "Please Agree our Terms & Conditions", parent=self.root)
        else:
            try:
                con = pymysql.connect(
                    host="localhost", user="root", password="", database="visitor_data")
                cur = con.cursor()

                cur.execute("select * from visitors_data where email=%s",
                            self.txt_email.get())
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Error !", "Already Exists Email ! Try with another one.", parent=self.root)

                else:
                    cur.execute("insert into visitors_data (ID,fname,lname,username,contact,email,age,gender,password,visitreason,post,Access_level) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (self.new_ID, self.txt_fname.get(
                    ), self.txt_lname.get(), self.txt_username.get(), self.txt_contact.get(), self.txt_email.get(), self.txt_age.get(), self.cmb_gender.get(), self.txt_password.get(), self.txt_reason.get(), self.txt_pos.get(), self.Access_level))
                    con.commit()
                    con.close()
                    messagebox.showinfo(
                        "Success !", "Registration Completed !", parent=self.root)
                    # sub_data = NULL
                    self.register_face()

                    self.clear_data()

            except EXCEPTION as es:
                messagebox.showerror(
                    "Error", f"Error due to : {str(es)}", parent=self.root)

    def register_face(self):
        connection = pymysql.connect(
            host="localhost", user="root", password="", database="visitor_data")
        cur = connection.cursor()
        sub_data = int(cur.execute(
            "select ID from visitors_data where email=%s", self.txt_email.get()))
        # sub_data2 = cur.execute("select lname from visitor_data where email=%s", self.txt_email.get())
        print(sub_data)
        # print(sub_data2)
        connection.close()
        # sub_data = sub_data1+sub_data2
        sub_data = self.txt_User_ID.get()
        path = os.path.join(datasets, sub_data)
        if not os.path.isdir(path):
            os.mkdir(path)
        (width, height) = (130, 100)
        face_cascade = cv2.CascadeClassifier(haar_file)
        webcam = cv2.VideoCapture(0)
        count = 0
        while count < 30:
            (_, im) = webcam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (width, height))
                cv2.imwrite('% s/% s.png' % (path, count), face_resize)

            count = count+1

            cv2.imshow('OpenCV', im)
            key = cv2.waitKey(10)
            if key == 27:
                break


root = Tk()
obj = Register(root)
root.mainloop()
