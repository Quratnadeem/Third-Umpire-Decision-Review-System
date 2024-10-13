import tkinter #for GUIs
import cv2 #for video processing
from PIL import Image, ImageTk #for converting video frames into images
from functools import partial 
# Use partial to pass arguments to the function, as 'command' only accepts a function without parameters
import threading #Using threading to run the 'pending' function without blocking the main GUI thread
import imutils
import time

stream = cv2.VideoCapture("clip.mp4")
flag = True
def play(speed):
    global flag
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)
    grabbed, frame = stream.read()

    if not grabbed:
        exit()
        
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(100, 25, fill='black', font=("Times", 15, "bold"), text="Decision Pending.....")
    flag = not flag
    print(f"You clicked on speed {speed}")

def pending(decision):
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image = frame #keeps a reference to the image so it won’t be garbage collected, ensuring that it remains displayed on the canvas
    canvas.create_image(0, 0, image=frame, ancho=tkinter.NW)

    time.sleep(1)

    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image = frame 
    canvas.create_image(0, 0, image=frame, ancho=tkinter.NW)

    time.sleep(1.5)

    if decision == "Out":
        decisionImg = "out.png"
    else:
        decisionImg = "not_out.png"

    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image = frame 
    canvas.create_image(0, 0, image=frame, ancho=tkinter.NW)

def out():
    thread = threading.Thread(target=pending, args=("Out",)) #
    thread.daemon = 1 #runs in background and doesn't block program from exiting
    thread.start()
    print("Player is Out")

def not_out():
    thread = threading.Thread(target=pending, args=("Not Out",))
    thread.daemon = 1
    thread.start()
    print("Player is Not Out")

SET_WIDTH = 600
SET_HEIGHT = 338

window = tkinter.Tk()
window.title("Third Umpire Decision Review")
window.configure(bg='#81C784')


cv_img = cv2.cvtColor(cv2.imread("welcome.png"), cv2.COLOR_BGR2RGB) #Reads image file and convert into RGB
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT) #create canvas inside a window
picture = ImageTk.PhotoImage(image=Image.fromarray(cv_img)) #create tk photoimage from image data
image_on_canvas = canvas.create_image(0, 0, ancho= tkinter.NW, image=picture) #places pic on the canvas
canvas.pack(pady=(5, 0)) #packs canvas onto window making it visible

#buttons
btn = tkinter.Button(window, text="<< Previous (fast)", width=40, command=partial(play, -25))
btn.pack(pady=(5, 10))
btn = tkinter.Button(window, text="<< Previous (slow)", width=40, command=partial(play, -3))
btn.pack(pady=(0, 10))
btn = tkinter.Button(window, text="Next (fast) >>", width=40, command=partial(play, 25))
btn.pack(pady=(0, 10))
btn = tkinter.Button(window, text="Next (slow) >>", width=40, command=partial(play, 3))
btn.pack(pady=(0, 10))
btn = tkinter.Button(window, text="Give Out", width=40, command=out)
btn.pack(pady=(0, 10))
btn = tkinter.Button(window, text="Give Not Out", width=40, command=not_out)
btn.pack()
 
window.mainloop() #starts event loop




