from tkinter import ttk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from DataBase import*
import matplotlib.dates as mdates
import datetime

class DataPlotDialog:

    def __init__(self, parent=None):
        top = self.top = tk.Toplevel(parent)
        
        #create label to hold image
        self.image_label = tk.Label(top)
        validate_data=None
        csv_data=read_from_log()
        validate_data=read_from_validation()

        button = tk.Button(top, text="Quit", command=self.on_click)
        button.grid(row=1, column=0)

        self.mu = tk.DoubleVar()
        self.mu.set(5.0)  # default value for parameter "mu"
        slider_mu = tk.Scale(top,
                             from_=7, to=0, resolution=0.1,
                             label='mu', variable=self.mu,
                             command=self.on_change
                             )
        slider_mu.grid(row=0, column=0)

        self.n = tk.IntVar()
        self.n.set(512)  # default value for parameter "n"
        slider_n = tk.Scale(top,
                            from_=512, to=2,
                            label='n', variable=self.n, command=self.on_change
                            )
        slider_n.grid(row=0, column=1)

        if validate_data!=None:
            self.plot_data(csv_data,validate_data)
        else:
            self.plot_data(csv_data)

    def plot_data(self,data,validate=None):
        name=data[0][:]
        print(name)
        print(len(data))
  
        fig = Figure(figsize=(len(name), len(name)), dpi=96,tight_layout=True,constrained_layout=None)
        
        time=self.read_time(data,0)
        for i in range(len(name)-1):#colume 2 to end
            pos=i+1
            ax = fig.add_subplot(len(name),1,pos)
            
            y=self.read_data(data,pos)
            #x=range(0,len(y))
            #x, y = self.data(self.n.get(), self.mu.get())
            self.line1, = ax.plot(time, y,label='values over time')
            ax.xaxis.set_major_formatter(self.fmt)
            ax.set_title(name[pos],fontsize= 10)
            #ax.set_title(name[i],x=-20,y=10,fontsize= 10)
            #ax.set_xlabel(name[i])
            #ax.set_ylabel(name[i])
            #ax.autoscale_view(True, True, True)
            #ax.grid(True)
            
            if validate!=None:
                val_pos=[1,2,0,0,0,5,4,3]
                if val_pos[pos-1]!=0:
                    y1=self.read_validation(validate,val_pos[pos-1])
                    #ax.hold(True)
                    ax.plot(time, y1,label='values over time')
            
        self.graph = FigureCanvasTkAgg(fig, master=self.top)
        canvas = self.graph.get_tk_widget()
        canvas.grid(row=0, column=2)
        print('data')
        
    def read_data(self,data,num):
        out=[]

        for i in range(len(data)-1):#raw 2 to end
            value=data[i+1][num]
            
            if value=="On":
                number=1
            elif value=="Off":
                number=0
            elif value=="left":
                number=3       
            elif value=="middle":
                number=2    
            elif value=="right":
                number=1
            elif value=='':
                number=0
            else:
                number=value[1:-2]

            out.append(float(number))
        return out

    def read_time(self,data,num):
        timeArray=[]
        for i in range(len(data)-1):#raw 2 to end
            day_time=data[i+1][num].split(" ")
            timeArray.append(day_time[1])
            
        self.fmt = mdates.DateFormatter('%H:%M:%S')
        time = [datetime.datetime.strptime(i, '%H:%M:%S.%f') for i in timeArray]
    
        return time
  
    def read_validation(self,data,num):
        out=[]
        for i in range(len(data)-1):#raw 2 to end
            value=data[i+1][num]
            out.append(value)
        return out
  
    def on_click(self):
        self.top.destroy()

    def on_change(self, value):
        x, y = self.data(self.n.get(), self.mu.get())
        self.line1.set_data(x, y)  # update data

        # set plot limit
        # ax = self.graph.figure.axes[0]
        # ax.set_xlim(min(x), max(x))
        # ax.set_ylim(min(y), max(y))

        # update graph
        self.graph.draw()

    def data(self, n, mu):
        lst_y = []
        for i in range(n):
            lst_y.append(mu * random.random())
        return range(n), lst_y

