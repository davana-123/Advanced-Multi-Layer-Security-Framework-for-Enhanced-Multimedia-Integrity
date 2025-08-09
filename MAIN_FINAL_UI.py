from tkinter import *
from PIL import ImageTk,Image
import os

mwin=Tk()
mwin.title("Video Stegnography")
mwin.configure(background="#b0f69f")
mwin.geometry("1600x850")
img=Image.open("stt.jpg")
img=img.resize((1600,850))
bg=ImageTk.PhotoImage(img)
lmain = Label(mwin,image=bg)
lmain.place(x=0, y=0)
lmain = Label(mwin,text="STEGANOGRAPHY",bg="#116cd4",fg="white",width=40,height=2,font=("Elephant",25,"bold"))
lmain.place(x=150, y=50)
def images():
    os.system("python image.py")
def audios():
    os.system("python AUDIO.py")
def videos():
    os.system("python stegnography_final.py")



labelL1=Button(mwin,text="IMAGE",bg="#116cd4",fg="white",width=20,height=2,font=("times",14,"bold"),activebackground="red", command=images)
labelL1.place(x=150,y=200)

labelL1=Button(mwin,text="AUDIO",bg="#116cd4",fg="white",width=20,height=2,font=("times",14,"bold"),activebackground="red", command=audios)
labelL1.place(x=150,y=300)

labelL1=Button(mwin,text="VIDEO",bg="#116cd4",fg="white",width=20,height=2,font=("times",14,"bold"),activebackground="red", command=videos)
labelL1.place(x=150,y=400)



mwin.mainloop()
    

