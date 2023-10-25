import cv2
import tkinter as tk
from tkinter import Scale, HORIZONTAL
from PIL import Image, ImageTk

# Functie om de webcambeelden bij te werken op basis van de geselecteerde sliders
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

# Creëer een OpenCV-videocapture-object voor de externe webcam
cap = cv2.VideoCapture(1)

# Controleer of de camera correct is geopend
if not cap.isOpened():
    print("Kan de webcam niet openen.")
    exit()

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

# Wanneer het venster wordt gesloten, release de webcam en stop het programma
cap.release()
cv2.destroyAllWindows()
