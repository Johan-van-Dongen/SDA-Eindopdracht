import threading
import DoBotArm as Dbt
import time
from serial.tools import list_ports
import keyboard
import cv2
import tkinter as tk
from tkinter import Scale, HORIZONTAL
from PIL import Image, ImageTk
import imutils
from shape_detector import ShapeDetector



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

def update_frame():
    # Lees een frame van de webcam
    ret, frame = cap.read()
    
    if not ret:
        return

    # Ontvang de huidige waarden van de sliders
    x = x_slider.get()
    y = y_slider.get()
    w = w_slider.get()
    h = h_slider.get()

    # Crop het frame op basis van de sliderwaarden
    cropped_frame = frame[y:y+h, x:x+w]
    cv2.imwrite("test.jpg", cropped_frame)

    # Converteer het frame naar een afbeelding die in het Tkinter-venster kan worden weergegeven
    img = Image.fromarray(cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB))
    img = img.resize((320, 240))

    photo = ImageTk.PhotoImage(image=img)
    canvas1.create_image(0, 0, image=photo, anchor=tk.NW)
    canvas1.image = photo

    # Creëer een frame met rechthoek om het gecropte gebied weer te geven
    frame_with_rect = frame.copy()
    cv2.rectangle(frame_with_rect, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Groene rechthoek
    img_with_rect = Image.fromarray(cv2.cvtColor(frame_with_rect, cv2.COLOR_BGR2RGB))
    img_with_rect = img_with_rect.resize((320, 240))

    photo_with_rect = ImageTk.PhotoImage(image=img_with_rect)
    canvas2.create_image(0, 0, image=photo_with_rect, anchor=tk.NW)
    canvas2.image = photo_with_rect
    # Herhaal de functie om de frames te blijven bijwerken
    canvas1.after(10, update_frame)
    

if __name__ == "__main__":
    #List selected ports for selection
    port = port_selection()
        
    # Preprogrammed sequence
    homeX, homeY, homeZ = 90, -100, 10
    print("Connecting")
    print("Homing")
    ctrlBot = Dbt.DoBotArm(port, homeX, homeY, homeZ ) #Create DoBot Class Object with home position x,y,z
    # Creëer een OpenCV-videocapture-object voor de externe webcam
    cap = cv2.VideoCapture(1)
    # Controleer of de camera correct is geopend
    if not cap.isOpened():
        print("Kan de webcam niet openen.")
        exit()

    ctrlBot.moveArmXYZ(90, 30, 70, 0)

    # Maak een Tkinter-venster
    root = tk.Tk()
    root.title("Webcam Crop Tool")

    # Voeg sliders toe voor het aanpassen van het bijsnijden
    x_slider = Scale(root, label="X", from_=0, to=640, orient=HORIZONTAL)
    x_slider.pack()
    x_slider.set(0)

    y_slider = Scale(root, label="Y", from_=0, to=480, orient=HORIZONTAL)
    y_slider.pack()
    y_slider.set(0)

    w_slider = Scale(root, label="Width", from_=0, to=640, orient=HORIZONTAL)
    w_slider.pack()
    w_slider.set(640)

    h_slider = Scale(root, label="Height", from_=0, to=480, orient=HORIZONTAL)
    h_slider.pack()
    h_slider.set(480)

    # Maak twee Tkinter Canvassen om de videofeeds weer te geven
    canvas1 = tk.Canvas(root, width=320, height=240)
    canvas1.pack()

    canvas2 = tk.Canvas(root, width=320, height=240)
    canvas2.pack()

    # Start de functie voor het bijwerken van het frame
    update_frame()

    root.mainloop()

    # read the test.jpg
    image = cv2.imread("test.jpg")

    #move to home
    ctrlBot.moveArmXYZ(90, -100, 10, 0)

    # calculate the pixel to mm ratio
    mm_to_pixel_ratio = 0.681

    # convert the image to grayscale, blur it slightly and threshold it
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    thresh = cv2.threshold(blurred_image, 60, 255, cv2.THRESH_BINARY)[1]

    # move to the current position

    # find contours in the thresholded image and initialize the shape detector
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    shape_detector = ShapeDetector()

    # initialize lists to store the centroids and the colors
    centroids = []
    colors = []

    # loop over the contours
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

    # Print the color at each centroid
    for i, color in enumerate(colors):
        print(f"Color at Centroid {i+1} (B, G, R):", color)
    
    position = ctrlBot.getPosition()
    # Print the centroid coordinates for all shapes and draw a white circle at each centroid
    for i, centroid in enumerate(centroids):
        print(f"Centroid {i+1} (x, y):", centroid)
        #move to the first centroid
        
        #float to int
        position = [int(i) for i in position]

        ctrlBot.moveArmRelXYZ((centroid[0]*mm_to_pixel_ratio), (-centroid[1]*mm_to_pixel_ratio), 20, 0)
        time.sleep(10)

    # release the camera and close the windows
    cap.release()
    cv2.destroyAllWindows()
    exit()