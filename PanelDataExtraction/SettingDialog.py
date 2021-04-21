from tkinter import ttk
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2
from PanelRecognition import cv2_to_box
import DataCollation.Semantic_Class as SC

class SettingDialog:

    def __init__(self, parent,image):
        top = self.top = tk.Toplevel(parent)

        self.corner1=0
        self.corner2=0
        #create label to hold image
        self.image_label = tk.Label(top)
        self.cv_image = image
        self.cv_org_image=self.cv_image.copy()
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        #self.image_label.pack(side="left", fill="both", expand="yes", padx=10, pady=10)
        self.image_label.grid(row =0,column = 0,columnspan=4, rowspan=13)
        self.image_label.configure(image=image)
        self.image = image
        self.image_label.bind("<Button-1>", self.callback)
        
        self.myLabel1 = tk.Label(top, text='Step1:select the panel region \n using mouse')
        self.myLabel1.grid(sticky=tk.W,row =0,column = 5,columnspan=1, rowspan=1)
        #
        self.myCropButton = tk.Button(top,width = 18, text='Step2: crop the image', command=self.on_crop)
        self.myCropButton.grid(sticky=tk.W,padx=5,row =1,column = 5,columnspan=1, rowspan=1)
        
        self.myLabel2 = tk.Label(top, text='Step3:input components name')
        self.myLabel2.grid(sticky=tk.W,padx=5,row =2,column = 5,columnspan=1, rowspan=1)
        
        self.myLabel3 = tk.Label(top, text='number:')
        self.myLabel3.grid(sticky=tk.W+tk.S,padx=5,row =3,column = 5,columnspan=1, rowspan=1)
        
        self.num_var = tk.StringVar()
        self.number_combobox = ttk.Combobox(
            top,
            textvariable=self.num_var,
            values=["none"]
        )
        self.number_combobox.grid(sticky=tk.W,padx=5,row =4,column = 5,columnspan=1, rowspan=1)
        
        self.myLabel4 = tk.Label(top, text='type:')
        self.myLabel4.grid(sticky=tk.W+tk.S,padx=5,row =5,column = 5,columnspan=1, rowspan=1)
        self.type_var = tk.StringVar()
        self.type_combobox = ttk.Combobox(
            top,
            textvariable=self.type_var,
            values=["light","threestate", "dial", "knob", "silverswitch","disp7","voltmeter"]
        )
        
        
        self.type_combobox.grid(sticky=tk.W,padx=5,row =6,column = 5,columnspan=1, rowspan=1)
        
        self.myLabel5 = tk.Label(top, text='name:')
        self.myLabel5.grid(sticky=tk.W+tk.S,padx=5,row =7,column = 5,columnspan=1, rowspan=1)
        self.text_var = tk.StringVar()
        self.my_entry = ttk.Entry(
            top,
            textvariable=self.text_var
        )
        self.my_entry.grid(sticky=tk.W,padx=5,row =8,column = 5,columnspan=1, rowspan=1)
        
        self.myInputButton = tk.Button(top, text='input', width = 18, command=self.on_input)
        self.myInputButton.grid(sticky=tk.W,padx=5,row =9,column = 5,columnspan=1, rowspan=1)
        
        self.myfileButton = tk.Button(top, text='from file', width = 18, command=self.on_file)
        self.myfileButton.grid(sticky=tk.W,padx=5,row =10,column = 5,columnspan=1, rowspan=1)
        
        self.input_listbox = tk.Listbox(top)
        self.input_listbox.grid(sticky=tk.W,padx=5,row =11,column = 5,columnspan=1, rowspan=1)
     
        
        self.mySaveButton = tk.Button(top, text='save', width = 18,command=self.on_save)
        self.mySaveButton.grid(sticky=tk.W,padx=5,row =12,column = 5,columnspan=1, rowspan=1)
        
        self.click=0;


    def on_save(self):
        #self.username = self.myEntryBox.get()
        self.com_str=list(self.input_listbox.get(0,tk.END))
        #print(pro_str)
        
        save_str=""
        
        for x in self.com_str:
            name_str=x.split('_')
            if name_str[1]=='disp7':
                save_str+="(lambda b,np_img : create_disp(subscript_np_array(b,np_img))),\n"

            if name_str[1]=='voltmeter':
                save_str+="(lambda b,np_img : create_voltmeter(subscript_np_array(b,np_img))),\n"
                
            if name_str[1]=='silverswitch':
                save_str+="(lambda b,np_img : create_silver(subscript_np_array(b,np_img))),\n"
            
            if name_str[1]=='dial':    
                save_str+="(lambda b,np_img : create_dial(subscript_np_array(b,np_img))),\n"
                
            if name_str[1]=='threestate':     
                save_str+="(lambda b,np_img : create_threestate(subscript_np_array(b,np_img))),\n"
            
            if name_str[1]=='light': 
                save_str+="(lambda b,np_img : create_light(subscript_np_array(b, np_img),\""+name_str[2]+"\")),\n"
                
        self.save_str='['+ save_str[:-2]+']'       
        print(self.save_str)
        
        self.top.destroy()
        
    def on_input(self):

        input_str=self.num_var.get()+'_'+self.type_var.get()+'_'+self.text_var.get()
        self.input_listbox.insert('end', input_str)
            
    def on_file(self):

        sim_str=['1_disp7_temperature','2_voltmeter_motor','3_silverswitch_power','4_dial_water','5_threestate_fan','6_light_s','7_light_r','8_light_g']
        self.input_str=sim_str
        
        self.input_listbox.delete(0,'end')
        for iterm in self.input_str:
            self.input_listbox.insert('end', iterm)
        
    def on_crop(self):

        self.cv_org_image = self.cv_org_image[self.corner1[1]:self.corner2[1],self.corner1[0]:self.corner2[0]]
        self.cv_crop_image = self.cv_org_image.copy()
        self.boxes = cv2_to_box(self.cv_org_image) 
        self.boxes = self.boxes[1:] #fix off by one error
        #print('Boxes : ', len(boxes))
        
        self.number_combobox['values'] = tuple([x+1 for x in range(len(self.boxes))])
        count=0
        for c in self.boxes:
            x,y,w,h = c
            count += 1
            top_l, top_r, bot_l, bot_r = int(x-0.1*w), int(x+w*1.1), int(y-0.1*h), int(y+h*1.1)
            cv2.rectangle(self.cv_org_image,(top_l,bot_l),(top_r,bot_r),(0,255,0),2)
            cv2.putText(self.cv_org_image, str(count), (x - 10, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
        
        #resize before display
        self.cv_org_image=cv2.resize(self.cv_org_image,(480,640), interpolation = cv2.INTER_AREA)
        self.image = Image.fromarray(self.cv_org_image)
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.image)
        
    def callback(self,event):
        if self.click==0:
            self.click=self.click+1
            print("clicked first at", event.x, event.y)
            self.corner1 = (event.x, event.y)
            cv2.circle(self.cv_image,self.corner1,10,(255,0,0))
            
        elif self.click==1:
            #self.click=self.click+1
            print("clicked second at", event.x, event.y)
            self.corner2 = (event.x, event.y)
            cv2.circle(self.cv_image,self.corner2,10,(255,0,0))
            cv2.rectangle(self.cv_image,self.corner1,self.corner2,(255,255,0),3)
        
        #convert image to PIL library format which is required for Tk toolkit
        self.image = Image.fromarray(self.cv_image)
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.image)
