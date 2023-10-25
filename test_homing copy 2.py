import DoBotArm as Dbt
import time
from serial.tools import list_ports
import keyboard
import cv2
import imutils
from shape_detector import ShapeDetector
import math
import numpy as np


def port_selection():
    # Choosing port
    available_ports = list_ports.comports()
    print('Available COM-ports:')
    for i, port in enumerate(available_ports):
        print(f"  {i}: {port.description}")

    choice = int(input('Choose port by typing a number followed by [Enter]: '))
    return available_ports[choice].device

def homing_prompt():
    while (True):
        response = input("Do you wanna home? (y/n)")
        if(response == "y") :
            return True
        elif (response == "n"):
            return False
        else:
            print("Unrecognised response")

#--Main Program--
def main():
    #List selected ports for selection
    port = port_selection()
        
    # Preprogrammed sequence
    homeX, homeY, homeZ = 60, -105, 70
    print("Connecting")
    print("Homing")
    ctrlBot = Dbt.DoBotArm(port, homeX, homeY, homeZ ) #Create DoBot Class Object with home position x,y,z

def keyboard_input(keyboard):
    key = keyboard.name
    stepover = 5

    if key == '1':
        stepover = 5
    elif key == '2':
        stepover = 5
    elif key == '3':
        stepover = 5

    if key == 'w':
        position = ctrlBot.getPosition()
        ctrlBot.moveArmXYZ(position[0] + stepover, position[1], position[2] , 0)
    if key == 's':
        position = ctrlBot.getPosition()
        ctrlBot.moveArmXYZ(position[0] - stepover, position[1], position[2] , 0)
    if key == 'a':
        position = ctrlBot.getPosition()
        ctrlBot.moveArmXYZ(position[0], position[1] + stepover, position[2] , 0)
    if key == 'd':
        position = ctrlBot.getPosition()
        ctrlBot.moveArmXYZ(position[0], position[1] - stepover, position[2] , 0)
    if key == 'q':
        position = ctrlBot.getPosition()
        ctrlBot.moveArmXYZ(position[0], position[1], position[2] + stepover , 0)
    if key == 'e':
        position = ctrlBot.getPosition()
        ctrlBot.moveArmXYZ(position[0], position[1], position[2] - stepover , 0)
    if key == 'r':
        ctrlBot.rehome(None, None, None, False)

def ofset_correction(xdistance,ydistance,z,w):
    b = math.sqrt(ydistance**2+xdistance**2)
    xmove = (z/b)*ydistance + (w/b)*xdistance
    ymove = (z/b)*xdistance + (w/b)*ydistance
    return xmove,ymove


if __name__ == "__main__":
    #List selected ports for selection
    port = port_selection()
        
    # Preprogrammed sequence
    homeX, homeY, homeZ = 90, -100, 10
    print("Connecting")
    print("Homing")
    ctrlBot = Dbt.DoBotArm(port, homeX, homeY, homeZ ) #Create DoBot Class Object with home position x,y,z
    cap = cv2.VideoCapture(1)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    
    # start the keyboard listener
    keyboard.on_press(keyboard_input)
    print("move to the first corner and press c to continue")   
    #wait fot the user to press c
    keyboard.wait('c')
    # stop the keyboard listener
    keyboard.unhook_all()
    # read te current position
    first_corner=ctrlBot.getPosition()
    print(first_corner)
    # start the keyboard listener
    keyboard.on_press(keyboard_input)
    print("move to the second corner and press c to continue")
    #wait fot the user to press c
    keyboard.wait('c')
    # stop the keyboard listener
    keyboard.unhook_all()
    # read te current position
    second_corner=ctrlBot.getPosition()
    print(second_corner)
    # move the arm to the home position
    ctrlBot.moveArmXYZ(homeX,homeY,homeZ,0)
    time.sleep(1)
    distance_x=second_corner[0]-first_corner[0]
    distance_y=second_corner[1]-first_corner[1]
    if distance_y < 0:
        distance_y = distance_y * -1

    print(distance_x)
    print(distance_y)

    ret, image = cap.read()
    # Check if the frame was successfully read
    if not ret:
        print("Error: Could not read frame.")
        exit()

    # crop the image
    image = image[158:158+212, 136:136+207]
    cv2.imshow("Image", image)
    # filter the red color out of the image and blur it slightly and threshold it
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.imshow("hImage", hsv_image)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv_image, lower_red, upper_red)
    cv2.imshow("mImage", mask)
    blurred_image = cv2.GaussianBlur(mask, (5, 5), 0)
    thresh = cv2.threshold(blurred_image, 50, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("sImage", thresh)

    # find contours in the thresholded image and initialize the shape detector
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    shape_detector = ShapeDetector()

    # initialize lists to store the centroids and the colors
    centroids = []
    colors = []
    for c in cnts:
        # compute the center of the contour, then detect the name of the shape using only the contour
        M = cv2.moments(c)
        cX = int((M["m10"] / M["m00"]))
        cY = int((M["m01"] / M["m00"]))
        shape = shape_detector.detect(c)

        # append the centroid coordinates to the list
        centroids.append((cX, cY))
        cv2.circle(image, (cX,cY), 5, (155, 155, 155), -1)

        # append the color to the list
        color = image[cY, cX]
        colors.append(color)

        # draw the contours and the name of the shape on the image
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.putText(image, shape, (cX+10, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # show the output image
        cv2.imshow("Image", image)


    frame_y = image.shape[0]
    frame_x = image.shape[1]
    pixel_y = -distance_y/frame_x
    for i, centroid in enumerate(centroids):
        ctrlBot.moveArmXYZ(first_corner[0],first_corner[1],first_corner[2],0)
        time.sleep(1)
        print(f"Centroid {i+1} (x,y):", centroid)
        y_pixels = frame_x-centroid[1]
        x_pixels = frame_y-centroid[0]
        y_steps = y_pixels*pixel_y
        x_steps = x_pixels*pixel_y
        movex,movey = ofset_correction(distance_x,distance_y,x_steps,y_steps)
        print(movex)
        print(movey)
        print(x_steps)
        print(y_steps)

        #move the arm to the first corner
        ctrlBot.moveArmXYZ(first_corner[0],first_corner[1],first_corner[2]+10,0)
        ctrlBot.commandDelay()
        #move the pixel amount of x steps and y steps
        ctrlBot.moveArmXYZ(first_corner[0]-movex-6,first_corner[1]+movey,first_corner[2]-10,0)
        ctrlBot.commandDelay()
        ctrlBot.moveArmRelXYZ(0,0,-15,0)
        ctrlBot.commandDelay()
        ctrlBot.toggleSuction()
        ctrlBot.commandDelay()
        ctrlBot.moveArmRelXYZ(0,0,50,0)
        ctrlBot.commandDelay()
        ctrlBot.moveArmXYZ(150,60,homeZ+20,0)
        ctrlBot.commandDelay()
        ctrlBot.toggleSuction()
        ctrlBot.commandDelay()
        ctrlBot.SetConveyor(True,speed=-15000)
        ctrlBot.commandDelay()
        time.sleep(10)
        ctrlBot.SetConveyor(False)





    exit()