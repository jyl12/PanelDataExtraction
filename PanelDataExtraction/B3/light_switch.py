"""
INPUT --> cropped image array of light switch + calibration values
OUTPUT --> boolean TRUE when on

assumes:
- nothing

This requires calibration values for each button
record values for average
    r/g  and   b/g
for the on and off state of each button used

store in json file?
"""
import numpy as np
import cv2
from matplotlib import pyplot as plt
import json
import os
from collections import defaultdict

static = defaultdict(lambda: 0)
static['num']=0;
def get_button_state(raw_switch,typeof_light,cal_on,cal_off):
    
    static['num']=1
    #name=typeof_light[0].split(' ')
    #print('light',name[1])

    #print('num',static['num'])
    
    size = np.shape(raw_switch)
    f = 100/size[1]
    dsize = (int( size[1]*f ),int( size[0]*f ))
    raw_switch = cv2.resize(raw_switch,dsize)

    raw_switch = cv2.normalize(raw_switch, raw_switch,0,255,cv2.NORM_MINMAX)

    switch = cv2.medianBlur(raw_switch,5)
    gswitch = cv2.cvtColor(switch,cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(gswitch,cv2.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=0,maxRadius=0)
    circles = np.uint16(np.around(circles))

    blank = np.zeros((dsize[1],dsize[0]),np.uint8)
    for i in circles[0,:]:
        cv2.circle(blank,(i[0],i[1]),i[2],1,-1)

    masked = cv2.bitwise_and(raw_switch, raw_switch, mask=blank)
    b,g,r = cv2.split(masked)
    mean_r = np.mean(r)
    mean_g = np.mean(g)
    mean_b = np.mean(b)

    

    if static['num']==1:
        #if typeof_light=='light r':
        print('mean_g',mean_g)
        print('pre_g',static['pre_g'])
        dif=abs(mean_g-static['pre_g'])
        print('dif',dif)
        if dif>60:
            if mean_g>static['pre_g']:
                static['condition']=0
                print('on')
            else:
                static['condition']=1
                print('off')
                
        else:
            print(static['condition'])
            
    else:
        static['condition']=1
        print('first time')
      


    static['pre_g']=mean_g


    return static['condition']


