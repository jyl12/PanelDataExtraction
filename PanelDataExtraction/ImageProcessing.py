import cv2
import numpy as np
import DataCollation.Semantic_Class as SC
import B3.dial
import B3.light_switch
import B3.silver_switch
import B3.voltmeter
import B3.seven_seg

def subscript_np_array(box, arr):
    return np.array([x[box[0]:box[0] + box[2]] for x in arr[box[1]:box[1] + box[3]]])

list_of_stuff = [
    (lambda b,np_img : create_disp(subscript_np_array(b,np_img))),
    (lambda b,np_img : create_voltmeter(subscript_np_array(b,np_img))),
    (lambda b,np_img : create_silver(subscript_np_array(b,np_img))),
    (lambda b,np_img : create_dial(subscript_np_array(b,np_img))),
    (lambda b,np_img : create_threestate(subscript_np_array(b,np_img))),
    (lambda b,np_img : create_light(subscript_np_array(b, np_img), "s")), #6
    (lambda b,np_img : create_light(subscript_np_array(b, np_img), "r")),
    (lambda b,np_img : create_light(subscript_np_array(b, np_img), "g"))
]

cals_dict = {
    "g" : {
    "on" : [0.00,0.95],
    "off" : [0.17,0.84]
    },
    "r" : {
    "on" : [2.66,0.68],
    "off" : [5.18,0.79]
    },
    "s" : {
    "on" : [1.06,1.04],
    "off" : [1.38,0.74]
    }
}

measure_func_dict = {
    "light": lambda so : B3.light_switch.get_button_state(so.np, np.array(so.cal_on), np.array(so.cal_off)),
    "volt": lambda so: B3.voltmeter.get_voltmeter_angle(so.np),
    "silver": lambda so: B3.silver_switch.get_switch_state(so.np),
    "dial": lambda so: B3.dial.get_angle(so.np),
    "display": lambda so: B3.seven_seg.seven_seg_disp(so.np)
}

dial_dic = {
    'cont' : ((-180,180),(-10,10)),
}

def create_disp(pixels):
    r = SC.LCDDisplay('7sed_disp')
    r.measure_func = lambda so : B3.seven_seg.seven_seg_disp(so.np)
    return r

def create_silver(pixels):
    r = SC.Discrete('silver_switch')
    r.measure_func = lambda so : B3.silver_switch.get_switch_state(so.np)
    return r

def create_dial(pixels,typeof_dial='cont'):
    range_d,val_d = dial_dic[typeof_dial]
    r = SC.ContinuousDial(typeof_dial + ' dial',range_d[0],range_d[1],val_d[0],val_d[1])
    r.measure_func = lambda so : B3.dial.get_angle(so.np)
    return r

def create_threestate(pixels):
    r = SC.Discrete('threestate',valueMap={-45.0:'left',0.0:'middle',45.0:'right'})
    r.measure_func = lambda so : B3.dial.get_angle(so.np)[0]
    return r

def create_voltmeter(pixels,range_d=(-30,30),val_d=(0,15)):
    r = SC.ContinuousDial('voltmeter',range_d[0],range_d[1],val_d[0],val_d[1])
    r.measure_func = lambda so : B3.voltmeter.get_voltmeter_angle(so.np)
    return r

def create_light(pixels, typeof_light):
    r = SC.Discrete(typeof_light + 'light')
    r.measure_func = lambda so : B3.light_switch.get_button_state(so.np,typeof_light, np.array(so.cal_on), np.array(so.cal_off))

    
    r.cal_on = cals_dict[typeof_light]["on"]
    r.cal_off = cals_dict[typeof_light]["off"]
    return r    

def create_placeholder(pixels):
    r = SC.Discrete("light")
    return r


def get_so_list(list_of_stuff,boxes,img_colour):
    #print(img_colour, type(img_colour), np.shape(img_colour))
    SOs = []
    # main list of all semantic objects

    np_img = np.asarray(img_colour)

    for i,b in enumerate(boxes):
        SOs.append(list_of_stuff[i](b,np_img))        
        SOs[-1].box = b

    return SOs

def update_so_values(SOs,img_colour):#
    results=[]
    for so in SOs:
        so.np = subscript_np_array(so.box,img_colour)
        try:
            #print(so)
            #print(so.value)
            so.value = so.measure_func(so)
            results.append(so.value)
        except:
            warn_str='couldn\'t update SO: ' + so.meaning
            #print(warn_str)
            results.append(warn_str)
            
    return results
    

if __name__ == '__main__':
    img = cv2.imread('newimage.png',1)
    SOs = get_so_list(img)
    update_so_values(SOs,img)

    for so in SOs:
        print(so.meaning)
        print(so.value)
        print(so.box)
        print('\n')


