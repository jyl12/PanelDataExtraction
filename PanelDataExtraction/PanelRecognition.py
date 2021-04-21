#import the libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2

from imutils.perspective import four_point_transform
from imutils import contours
import imutils

def edge_detection (image):
    # image is cropped grayscale original image
    img = cv2.Canny(image,100,200)
    #cv2.imshow('test', img)
    #cv2.waitKey(0)
    return img

def dilate_then_erode (image):
    #cv2.imshow('test',image)
    #cv2.waitKey(0)
    #print(image.shape())
    # image is output of edge_detection
    kernel = np.ones((5,5),np.uint8)
    #print(kernel)

    dilation = cv2.dilate(image,kernel,iterations = 2)
    erode = cv2.erode(dilation,kernel,iterations = 1)
    return erode

def fill (image):
    # image is output of dilate_then_erode
    # (input "image" is white on black so that "erode_inversed" is black on white)
    erode_inversed = cv2.bitwise_not(image)

    # Threshold.
    # Set values equal to or above 220 to 0.
    # Set values below 220 to 255. 
    th, im_th = cv2.threshold(erode_inversed, 220, 255, cv2.THRESH_BINARY_INV)
    
    # Copy the thresholded image.
    im_floodfill = im_th.copy()
    
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    
    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0,0), 255)
    
    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    
    # Combine the two images to get the foreground.
    im_out = im_th | im_floodfill_inv

    # im_out is the filled in white on black image
    return im_out

def create_img_sections (image):
    # image_detect is the im_out from fill function
    # image_display is the original image in colour

    # convert the grayscale image to binary image
    ret,thresh = cv2.threshold(image,127,255,0)
    
    # find contours in the binary image
    contours, heirarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    rectangle_coords = []
    count = 1
    for c in contours:
        
        # creating adding rectangles
        x,y,w,h = cv2.boundingRect(c)
        if (w/h < 0.3 or w/h > 3) or w < 15 or h < 15:
            pass
        else:
            top_l, top_r, bot_l, bot_r = int(x-0.1*w), int(x+w*1.1), int(y-0.1*h), int(y+h*1.1)
            rectangle_coords.append((x, y, w, h))
            cv2.rectangle(image,(top_l,bot_l),(top_r,bot_r),(0,255,0),2)
            cv2.putText(image, str(count), (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
        count += 1
    return rectangle_coords

def cv2_to_box(img):
    return create_img_sections(fill(dilate_then_erode(edge_detection(img))))


if __name__ == '__main__':
    img = cv2.imread('samplepic_cropped.png',0)
    print(cv2_to_box(img))

if __name__ == "__main__":
    img = cv2.imread('samplepic_cropped.png', 1)
    cv2.imshow('test',dilate_then_erode(img))
    cv2.waitKey(0)



