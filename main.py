# Language: Python 3

# this is the main code that will be used to detect the shapes in the image using the shape_detector class
# the code will read the image and convert it to grayscale
# then it will apply the gaussian blur to the image to remove the noise
# then it will apply the canny edge detection to detect the edges in the image
# then it will find the contours in the image
# then it will loop through the contours and detect the shape of each contour
# then it will draw the contour and the name of the shape on the image

import cv2
import numpy as np
import imutils
from shape_detector import ShapeDetector
import argparse

def cropfunction(foto):
    # Converteer de afbeelding naar grijswaarden
    gray = cv2.cvtColor(foto, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Gray', gray)

# Definieer een drempelwaarde om zwart te detecteren (kan worden aangepast)
    threshold = 85

# Maak een masker voor de zwarte regio's
    mask = gray < threshold

# Vind de contouren van het zwarte gebied
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Als er contouren zijn gevonden, selecteer dan het grootste contour
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

    # Bepaal de begrenzende rechthoek rond het grootste contour
        x, y, w, h = cv2.boundingRect(largest_contour)

    # Snijd de afbeelding om het zwarte gebied te verwijderen
        cropped_image = foto[y+5:y+h-5, x+5:x+w-5]

    # Toon het bijgesneden resultaat
        cv2.imshow('Originele afbeelding', foto)
        
        cv2.imshow('Contour', cv2.drawContours(foto.copy(), [largest_contour], -1, (0, 255, 0), 2))
        cv2.imshow('Bijgesneden afbeelding', cropped_image)
        cv2.waitKey(0)
        return cropped_image
    else:
        print("Geen zwart gebied gevonden.")
    cv2.destroyAllWindows()
    



# read the image 
#image = cv2.imread('resources/shapes.png')
cap = cv2.VideoCapture(1)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Read the frame
ret, image = cap.read()

# Check if the frame was successfully read
if not ret:
    print("Error: Could not read frame.")
    exit()

# crop the image 
image = cropfunction(image)




# convert the image to grayscale, blur it slightly and threshold it
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray', gray_image)
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
cv2.imshow('Blurred', blurred_image)
thresh = cv2.threshold(blurred_image, 90 , 255, cv2.THRESH_BINARY)[1]
cv2.imshow('Thresh', thresh)
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

# Print the centroid coordinates for all shapes and draw a white circle at each centroid
for i, centroid in enumerate(centroids):
    print(f"Centroid {i+1} (x, y):", centroid)

cv2.waitKey(0)

