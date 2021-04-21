
# coding: utf-8

# # Application GUI

# In[1]:
from tkinter import ttk
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2
import threading
import queue
import numpy as np
from MultiListbox import MultiListbox
from ImageProcessing import*
import DataCollation.Semantic_Class as SC
from DataBase import*
from SettingDialog import SettingDialog
from DataPlotDialog import DataPlotDialog
# ## Left Screen Views

# In[3]:
VALIDATE=0

class LeftView(tk.Frame):
    def __init__(self, root):
        #call super class (Frame) constructor
        tk.Frame.__init__(self, root)
        #save root layour for later references
        self.root = root
        #load all UI
        self.setup_ui()
        
    def setup_ui(self):
        #create a output label
        self.output_label = tk.Label(self, text="Webcam Live", bg="black", fg="white")
        self.output_label.pack(side="top", fill="both", expand="yes", padx=10)
        
        #create label to hold image
        self.image_label = tk.Label(self)
        #put the image label inside left screen
        self.image_label.pack(side="left", fill="both", expand="yes", padx=10, pady=10)
        #self.image_label.grid(row =0,column = 0,columnspan=4, rowspan=20)
        
    def update_image(self, image):
        #configure image_label with new image 
        self.image_label.configure(image=image)
        #this is to avoid garbage collection, so we hold an explicit reference
        self.image = image
    

# ## All App GUI Combined


# In[6]:

class AppGui:
    def __init__(self):
        #initialize the gui toolkit
        self.root = tk.Tk()
        #set the geometry of the window
        #self.root.geometry("550x300+300+150")
        self.crop=None
        self.calibration=None
        self.start=0
        self.data=None
        #set title of window
        self.root.title("Panel data extraction")     
        #create left screen view
        self.left_view = LeftView(self.root)
        #self.left_view.pack(side='left')
        self.left_view.grid(row =0,column = 0,columnspan=4, rowspan=15)

        #output window
        
        #self.label = ttk.Label(self.root, text="calibration")
        #self.label.grid(sticky=tk.W, row=0, column = 5)
        #

        self.calbutton = ttk.Button(self.root, text="calibration", width = 28,command=self.on_cal)
        self.calbutton.grid(row=2, column = 5,rowspan=2)
        
        #
        self.image_width=480
        self.image_height=640
#         self.my_text_var = tk.StringVar()
#         self.my_text_var.set("100")
#         self.my_entry = ttk.Entry(self.root,textvariable=self.my_text_var)
#         self.my_entry.grid(sticky=tk.E, row=1, column = 5)
        
        self.display = MultiListbox(self.root, (('Num', 1),('Name', 10),('Type', 10), ('Value', 8)))
        self.display.grid(row=4, column = 5,columnspan=1, rowspan=1)

        self.startbutton = ttk.Button(self.root, text="start", width = 28,command=self.on_start)
        self.startbutton.grid(row=5, column = 5,rowspan=2)
        
        self.stopbutton = ttk.Button(self.root, text="stop", width = 28,command=self.on_stop)
        self.stopbutton.grid(row=6, column = 5,rowspan=2)
     
        self.plotbutton = ttk.Button(self.root, text="plot", width = 28,command=self.on_plotData)
        self.plotbutton.grid(row=7, column = 5,rowspan=2)
        # status bar
        #self.status = tk.StringVar()
        #self.statusbar = ttk.Label(self.root, textvariable=self.status)
        #self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)
        #self.records_saved = 0

        #define the center of the cirlce based on image dimentions
        #this is the cirlce we will use for user focus
        #self.circle_center = (int(self.image_width/2),int(self.image_height/4))
        #define circle radius
        #self.circle_radius = 15
        #define circle color == red
        #self.circle_color = (255, 0, 0)

        
        self.is_ready = True
        
    def launch(self):
        #start the gui loop to listen for events
        self.root.mainloop()
        
    def process_image(self, current_frame):

        if self.crop !=None:
            current_frame = current_frame[self.crop[1]:self.crop[3],self.crop[0]:self.crop[2]]
            img_colour=current_frame.copy()
            
            if self.calibration !=None:
                count=0
                for c in self.calibration:
                    x,y,w,h = c
                    count += 1
                    top_l, top_r, bot_l, bot_r = int(x-0.1*w), int(x+w*1.1), int(y-0.1*h), int(y+h*1.1)
                    cv2.rectangle(current_frame,(top_l,bot_l),(top_r,bot_r),(0,255,0),2)
                    cv2.putText(current_frame, str(count), (x - 10, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
                    name=self.components[count-1].split('_')
                    cv2.putText(current_frame, name[2], (x + 10, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
        
                if self.start==1:
                    print("image processing")
                    self.results=[]
                    self.results=update_so_values(self.SOs,img_colour)
                    print(self.results)
                    
                    #display
                    self.display.delete(0,self.display.size())
                    for i,result in enumerate(self.results):
                        if result[0:5]=='couldn':
                            value='nan'
                        else:
                            value=result
                            
                        name=self.components[i].split('_')
                        self.display.insert('end', (i+1, name[2],name[1],value))
                    #log
                    if VALIDATE==1:
                        if self.data !=None:
                            write_to_log_validation(self.SOs,self.val_data)   
                    else:
                        write_to_log(self.SOs)
                
        #display
        current_frame=cv2.resize(current_frame,(480,640), interpolation = cv2.INTER_AREA)
        
        if VALIDATE==1:
            if self.data !=None:
                cv2.putText(current_frame, self.data[:-2], (10, 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
            
        #convert image to PIL library format which is required for Tk toolkit
        current_frame = Image.fromarray(current_frame)
        current_frame = ImageTk.PhotoImage(current_frame)

        return current_frame
        
    def update_webcam_output(self, image):
        #pre-process image to desired format, height etc.
        self.cv_image=image
        self.image = self.process_image(image)
        #pass the image to left_view to update itself
        self.left_view.update_image(self.image)
        
    def on_cal(self):
        
        inputDialog = SettingDialog(self.root,self.cv_image)
        self.root.wait_window(inputDialog.top)
        
        #get crop region
        self.crop=inputDialog.corner1+inputDialog.corner2
        print('crop ', self.crop)
        
        #get components name 
        self.components=inputDialog.com_str
        print('components',self.components)
        
        #get name list
        for i,iterm in enumerate(self.components):
            name=iterm.split('_')
            self.display.insert('end', (i+1, name[2],name[1],'nan'))
            
        self.calibration=inputDialog.boxes
        
        #define functions
        self.SOs = []
        list_of_stuff=eval(inputDialog.save_str)   
        self.SOs=get_so_list(list_of_stuff,inputDialog.boxes[0:len(self.components)],inputDialog.cv_crop_image)
        
        #define log

        if VALIDATE==1:
            define_log_validation(self.SOs)
        else:
            define_log(self.SOs)

        
    def update_values(self,data):
        self.data=data #from uart
        data_pro=data.split(":")
        self.val_data=data_pro[1:-1:2]
        
    
    def on_start(self):
        self.start=1
        print("start")
        
    def on_stop(self):
        self.start=0
        print("stop")

    def on_plotData(self):
        plotDialog = DataPlotDialog(self.root)
        self.root.wait_window(plotDialog.top)
# ## Class to Access Webcam

# In[7]:

import cv2

class VideoCamera:
    def __init__(self):
        #passing 0 to VideoCapture means fetch video from webcam
        self.video_capture = cv2.VideoCapture(0)
                
    #release resources like webcam
    def __del__(self):
        self.video_capture.release()
        
    def read_image(self):
        #get a single frame of video
        ret, frame = self.video_capture.read()
        frame=cv2.rotate(frame,rotateCode = 0)
        #print(frame.shape)
        #return the frame to user
        return ret, frame
    
    #method to release webcam manually 
    def release(self):
        self.video_capture.release()
     
import serial

class UART:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
 
    def __del__(self):
        self.ser.close() 
        
    def read_data(self): 
        data = self.ser.readline().decode()
        return data
    
    def release(self):
        self.ser.close()
        
# ## Thread Class for Webcam Feed

# In[8]:

class WebcamThread(threading.Thread):
    def __init__(self, app_gui, callback_queue):
        #call super class (Thread) constructor
        threading.Thread.__init__(self)
        #save reference to callback_queue
        self.callback_queue = callback_queue
        
        #save left_view reference so that we can update it
        self.app_gui = app_gui
        
        #set a flag to see if this thread should stop
        self.should_stop = False
        
        #set a flag to return current running/stop status of thread
        self.is_stopped = False
        
        #create a Video camera instance
        self.camera = VideoCamera()
        
    #define thread's run method
    def run(self):
        #start the webcam video feed
        while (True):
            #check if this thread should stop
            #if yes then break this loop
            if (self.should_stop):
                self.is_stopped = True
                break
            
            #read a video frame
            ret, self.current_frame = self.camera.read_image()
            #self.data = self.uart.read_data()

            if(ret == False):
                print('Video capture failed')
                exit(-1)
                
            
            if self.callback_queue.full() == False:
                #put the update UI callback to queue so that main thread can execute it
                self.callback_queue.put((lambda: self.update_on_main_thread(self.current_frame, self.app_gui)))
        
        #fetching complete, let's release camera
        #self.camera.release()
        
            
    #this method will be used as callback and executed by main thread
    def update_on_main_thread(self, current_frame, app_gui):
        
        #wide=app_gui.update_values()
        #wide=int(wide)
        #if wide>0:
            #cv2.rectangle(current_frame,(5,5),(wide,wide),(255,255,0),3)
 #
#         if app_gui.crop !=None:
#             current_frame = current_frame[app_gui.crop[1]:app_gui.crop[3],app_gui.crop[0]:app_gui.crop[2]]
#             
#             if app_gui.calibration !=None:
#                 count=0
#                 for c in app_gui.calibration:
#                     x,y,w,h = c
#                     count += 1
#                     top_l, top_r, bot_l, bot_r = int(x-0.1*w), int(x+w*1.1), int(y-0.1*h), int(y+h*1.1)
#                     cv2.rectangle(current_frame,(top_l,bot_l),(top_r,bot_r),(0,255,0),2)
#                     cv2.putText(current_frame, str(count), (x - 10, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
#                     name=app_gui.components[count-1].split('_')
#                     cv2.putText(current_frame, name[1], (x + 10, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
#          
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
        #cv2.putText(current_frame, self.data, (10, 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
#          
        app_gui.update_webcam_output(current_frame)


    def __del__(self):
        self.camera.release()
            
    def release_resources(self):
        self.camera.release()
        
    def stop(self):
        self.should_stop = True
    
#####################
        
        
class UartThread(threading.Thread):
    def __init__(self, app_gui, callback_queue):
        #call super class (Thread) constructor
        threading.Thread.__init__(self)
        #save reference to callback_queue
        self.callback_queue = callback_queue
        
        #save left_view reference so that we can update it
        self.app_gui = app_gui
        
        #set a flag to see if this thread should stop
        self.should_stop = False
        
        #set a flag to return current running/stop status of thread
        self.is_stopped = False
        
        self.uart =UART()
        
    #define thread's run method
    def run(self):
        #start the webcam video feed
        while (True):
            #check if this thread should stop
            #if yes then break this loop
            if (self.should_stop):
                self.is_stopped = True
                break
            
            #read a video frame
            
            self.data = self.uart.read_data()

      
            if self.callback_queue.full() == False:
                #put the update UI callback to queue so that main thread can execute it
                self.callback_queue.put((lambda: self.update_on_main_thread(self.data, self.app_gui)))
            
    #this method will be used as callback and executed by main thread
    def update_on_main_thread(self, data, app_gui):       
        app_gui.update_values(data)
 
        
    def __del__(self):
        self.uart.release()
            
    def release_resources(self):
        self.uart.release()
        
    def stop(self):
        self.should_stop = True
    
        


# ## A GUI Wrappr (Interface) to Connect it with Data

# In[9]:

class Wrapper:
    def __init__(self):
        self.app_gui = AppGui()
        
        #create a Video camera instance
        #self.camera = VideoCamera()
        
        #intialize variable to hold current webcam video frame
        self.current_frame = None
        
        #create a queue to fetch and execute callbacks passed 
        #from background thread
        self.callback_queue = queue.Queue()
        
        #create a thread to fetch webcam feed video
        self.webcam_thread = WebcamThread(self.app_gui, self.callback_queue)
        
        #save attempts made to fetch webcam video in case of failure 
        self.webcam_attempts = 0
        
        #register callback for being called when GUI window is closed
        self.app_gui.root.protocol("WM_DELETE_WINDOW", self.on_gui_closing)
        
        #start webcam
        self.start_video()
        
        #start fetching video
        self.fetch_webcam_video()
        
        ##uart
        self.uart_attempts = 0
        self.callback_uart_queue = queue.Queue()
        if VALIDATE==1:
            self.uart_thread = UartThread(self.app_gui, self.callback_queue)
            self.start_uart()
            self.fetch_uart_data()
    
    def on_gui_closing(self):
        self.webcam_attempts = 51
        self.webcam_thread.stop()
        self.webcam_thread.join()
        self.webcam_thread.release_resources()
        
        self.app_gui.root.destroy()

    def start_video(self):
        self.webcam_thread.start()
        
    def fetch_webcam_video(self):
        try:
            #while True:
            #try to get a callback put by webcam_thread
            #if there is no callback and call_queue is empty
            #then this function will throw a Queue.Empty exception 
            callback = self.callback_queue.get_nowait()
            callback()
            self.webcam_attempts = 0
            #self.app_gui.root.update_idletasks()
            self.app_gui.root.after(70, self.fetch_webcam_video)
                
        except queue.Empty:
            if (self.webcam_attempts <= 50):
                self.webcam_attempts = self.webcam_attempts + 1
                self.app_gui.root.after(100, self.fetch_webcam_video)
                
    def fetch_uart_data(self):
        try:
 
            callback = self.callback_uart_queue.get_nowait()
            callback()
            self.uart_attempts = 0
            #self.app_gui.root.update_idletasks()
            self.app_gui.root.after(70, self.fetch_uart_data)
                
        except queue.Empty:
            if (self.uart_attempts <= 50):
                self.uart_attempts = self.uart_attempts + 1
                self.app_gui.root.after(100, self.fetch_uart_data)              
    
    def read_images(self):
        image = cv2.imread('data/test1.jpg')
    
        #conver to RGB space and to gray scale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        return image, gray
    
    def launch(self):
        self.app_gui.launch()
        
    def __del__(self):
        self.webcam_thread.stop()
   
    def start_uart(self):
        self.uart_thread.start()

# ## The Launcher Code For GUI

# In[10]:

# if __name__ == "__main__":
wrapper = Wrapper()
wrapper.launch()

