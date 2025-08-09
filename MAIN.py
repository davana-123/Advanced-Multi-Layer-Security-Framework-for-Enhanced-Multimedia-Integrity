from tkinter import *
from PIL import ImageTk,Image
import os

mwin=Tk()
mwin.title("Video Stegnography")
mwin.configure(background="#b0f69f")
mwin.geometry("1600x850")
img=Image.open("bagg.jpg")
img=img.resize((1600,850))
bg=ImageTk.PhotoImage(img)
lmain = Label(mwin,image=bg)
lmain.place(x=0, y=0)
lmain = Label(mwin,text="STEGANOGRAPHY",bg="white",fg="black",width=25,height=2,font=("Elephant",25,"bold "))
lmain.place(x=700, y=50)
def images():
    os.system("python image.py")
def audios():
    os.system("python AUDIO.py")
def videos():
    os.system("python stegnography_final.py")
def logout():
    mwin.destroy()
    os.system("python LOGIN.py")
labelL1=Button(mwin,text="IMAGE",bg="white",fg="black",width=20,height=2,font=("times",14,"bold"),activebackground="#93aebf", command=images)
labelL1.place(x=850,y=200)

labelL1=Button(mwin,text="AUDIO",bg="white",fg="black",width=20,height=2,font=("times",14,"bold"),activebackground="#93aebf", command=audios)
labelL1.place(x=850,y=320)

labelL1=Button(mwin,text="VIDEO",bg="white",fg="black",width=20,height=2,font=("times",14,"bold"),activebackground="#93aebf", command=videos)
labelL1.place(x=850,y=440)

labelL1=Button(mwin,text="Logout",bg="white",fg="black",width=20,height=2,font=("times",14,"bold"),activebackground="#93aebf", command=logout)
labelL1.place(x=850,y=560)

mwin.mainloop()
    

