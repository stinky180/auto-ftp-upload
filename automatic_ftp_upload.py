#Automatic FTP Upload
import os
import time, threading
import tkinter
from tkinter import *
from tkinter import filedialog
from ftplib import FTP
#from PIL import ImageTk, Image

class upload:
    def __init__(self):
        self.main_window = Tk()
        self.main_window.title("Automatic FTP Upload")
        self.main_window.geometry("450x300+300+300")

        #self.path = "wheelsdirty-logo-big.gif"
        #self.img = ImageTk.PhotoImage(Image.open(self.path))

        #GLOBAL VARIABLES
        self.__ftp = FTP()
        self.run = False
        self.file = ""
        self.count = 0
        
        #testing purposes
        

        #frame layout
        self.logo_frame = Frame(self.main_window)
        self.user_frame = Frame(self.main_window)
        self.pass_frame = Frame(self.main_window)
        self.host_frame = Frame(self.main_window)
        self.conn_frame = Frame(self.main_window)
        self.conn_btn_frame = Frame(self.main_window)
        self.remo_frame = Frame(self.main_window)
        self.locl_frame = Frame(self.main_window)
        self.misc_frame = Frame(self.main_window)
        self.cont_frame = Frame(self.main_window)
        self.exec_frame = Frame(self.main_window)
        

        #logo_frame widgets
        #self.logo_image = Label(self.logo_frame, image = self.img)
        #self.logo_image.pack(side="bottom", fill="both", expand="yes")
        self.logo_frame.pack()


        #user_frame widgets
        self.user_label = Label(self.user_frame, text="User:")
        self.user = Entry(self.user_frame, width=30)
        self.user_label.pack(side='left')
        self.user.pack(side='left')
        self.user_frame.pack()

        #pass_frame widgets
        self.pass_label = Label(self.pass_frame, text="Pass:")
        self.password = Entry(self.pass_frame, width=30, show="*")
        self.pass_label.pack(side='left')
        self.password.pack(side='left')
        self.pass_frame.pack()

        #host_frame widgets
        #includes a port entry and label
        self.host_label = Label(self.host_frame, text="Host:")
        self.port_label = Label(self.host_frame, text="Port:")
        self.host = Entry(self.host_frame, width=25)
        self.port = Entry(self.host_frame, width=10)
        self.host_label.pack(side='left')
        self.host.pack(side='left')
        self.port_label.pack(side='left')
        self.port.pack(side='left')
        self.host_frame.pack()

        #conn_frame widgets
        self.conn_label = Label(self.conn_frame, text="Connection status....  ")
        #ADD BINDING IN FUTURE
        #BIND TO STATUS METHOD
        self.status = StringVar()
        self.stat_label = Label(self.conn_frame, textvariable=self.status)
        self.conn_label.pack(side='left')
        self.stat_label.pack(side='left')
        self.conn_frame.pack()

        #conn_btn_frame widgets
        #ADD BINDINGS IN FUTURE
        #BIND TO CONNECT AND DISCONNECT METHODS
        self.conn_btn = Button(self.conn_btn_frame, text='Connect', command=self.connect)
        self.disc_btn = Button(self.conn_btn_frame, text='Disconnect', command=self.disconnect)
        self.disc_btn.config(state='disabled')
        self.conn_btn.pack(side='left')
        self.disc_btn.pack(side='left')
        self.conn_btn_frame.pack()

        #remo_frame widgets
        self.remo_label = Label(self.remo_frame, text="Remote Path:")
        self.remo_entry = Entry(self.remo_frame, width=30)
        self.remo_btn = Button(self.remo_frame, text="Set Path")
        self.remo_btn.config(state='disabled')
        self.remo_label.pack(side='left')
        self.remo_entry.pack(side='left')
        self.remo_btn.pack(side='left')
        self.remo_frame.pack()

        #locl_frame widgets
        self.locl_label = Label(self.locl_frame, text="Local Path")
        self.path = StringVar()
        
        self.locl_entry = Entry(self.locl_frame, textvariable = self.path, width=30)
        self.locl_btn = Button(self.locl_frame, text="Get Path", command=self.get_local_path)
        self.locl_label.pack(side='left')
        self.locl_entry.pack(side='left')
        self.locl_btn.pack(side='left')
        self.locl_frame.pack()

        #misc_frame widgets
        #working directory text
        self.misc_label = Label(self.misc_frame, text="Working DIR")
        self.pwd = StringVar()
        self.pwd_label = Label(self.misc_frame, textvariable=self.pwd)
        self.misc_label.pack(side='left')
        self.pwd_label.pack(side='left')
        self.misc_frame.pack()

        #cont_frame widgets
        #upload counter
        self.cont_label = Label(self.cont_frame, text="Uploaded: ")
        self.cnt_label = Label(self.cont_frame, text=self.count)
        self.cont_label.pack(side='left')
        self.cnt_label.pack(side='left')
        self.cont_frame.pack()

        #exec_frame widgets
        self.exec_label = Label(self.exec_frame, text="Upload:")
        self.exec_start_btn = Button(self.exec_frame, text="Start", command=self.start)
        self.exec_stop_btn = Button(self.exec_frame, text="Stop")
        self.exec_label.pack(side='left')
        self.exec_start_btn.pack(side='left')
        self.exec_stop_btn.pack(side='left')
        self.exec_frame.pack()

        tkinter.mainloop()

    ##BUTTON METHODS
    def get_local_path(self):
        self.file_path = tkinter.filedialog.askopenfilename()
        self.file = self.file_path
        self.path.set(self.file_path)

    def connect(self):
        ftp = FTP(host=self.host.get(), user=self.user.get(), passwd=self.password.get())
        self.__ftp = ftp
        
        if len(self.remo_entry.get()) > 0:
            self.__ftp.cwd(self.remo_entry.get())
            self.remo_btn.config(state='disabled')
            self.pwd.set(self.__ftp.pwd())
        else:
            self.remo_btn.config(state='active')
            self.need_remote_path()
            
        if len(self.__ftp.getwelcome()) > 0:
            self.status.set("OK")
            self.conn_btn.config(state='disabled')
            self.disc_btn.config(state='active')
        else:
            self.status.set("FAILED")
        
    def disconnect(self):
        self.__ftp.quit()
        self.conn_btn.config(state='active')
        self.disc_btn.config(state='disabled')
        self.status.set("DISC")


    def start(self):
        self.run = True
        self.upload()

    def stop(self):
        self.run = False
      

    def need_remote_path(self):
        messagebox.showwarning("Notice","Please enter a remote path and click set path")
       
    def upload(self):
        if self.run:
            myfile = open(self.file, 'rb')
            self.__ftp.storbinary("STOR test.txt" , myfile)
            self.count += 1
            myfile.close
            self.main_window.after(30000, self.upload)
        else:
            self.main_window.mainloop()
        
      

    

session = upload()
