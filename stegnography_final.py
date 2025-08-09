import tkinter as tk
from tkinter import *
import os
from PIL import Image,ImageTk
from tkinter.filedialog import askopenfilename
import shutil
import random
import sys
import cv2
from stegano import lsb
from os.path import isfile,join
import time                                                                
##import cv2
import numpy as np
import math
##import os
##import shutil
from subprocess import call,STDOUT
import subprocess
from PIL import Image,ImageTk
import telepot
bot=telepot.Bot("7007413336:AAFPbfg7z76UEtbuNW6607N62csdPzlXbN0")
ch_id="5759038138"
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad,unpad
from base64 import urlsafe_b64encode,urlsafe_b64decode


import os
import numpy as np
from PIL import Image

def calculate_psnr_mse(original_file, encrypted_file):
    # Open the images
    original_image = Image.open(original_file)
    encrypted_image = Image.open(encrypted_file)

    # Convert images to numpy arrays
    original_data = np.array(original_image)
    encrypted_data = np.array(encrypted_image)

    # Ensure both images have the same dimensions
    min_width = min(original_data.shape[1], encrypted_data.shape[1])
    min_height = min(original_data.shape[0], encrypted_data.shape[0])
    original_data = original_data[:min_height, :min_width]
    encrypted_data = encrypted_data[:min_height, :min_width]

    # Calculate Mean Square Error (MSE)
    mse = np.mean((original_data - encrypted_data) ** 2)

    # Calculate Peak Signal-to-Noise Ratio (PSNR) in dB
    max_pixel_value = np.max(original_data)
    psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))

    return psnr, mse

def calculate_embedding_capacity(original_file, encrypted_file):
    original_size = os.path.getsize(original_file)  # Size of the original image file in bytes
    encrypted_size = os.path.getsize(encrypted_file)  # Size of the encrypted image file in bytes

    embedding_capacity = original_size - encrypted_size

    return embedding_capacity


def generate_key(password, salt):
    kdf = PBKDF2(password, salt, dkLen=32, count=100000)
    return kdf

def aes_encrypt(plain_text, password):
    salt = get_random_bytes(16)
    key = generate_key(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC)
    cipher_text = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    return urlsafe_b64encode(salt + cipher.iv + cipher_text).decode()

def aes_decrypt(cipher_text, password):
    data = urlsafe_b64decode(cipher_text.encode())
    salt, iv, cipher_text = data[:16], data[16:32], data[32:]
    key = generate_key(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain_text = unpad(cipher.decrypt(cipher_text), AES.block_size)
    return plain_text.decode()

win=Tk()
win.title("Video Stegnography")
win.configure(background="black")
win.geometry("1600x850")  #500
img=Image.open("ste.jpg")
img=img.resize((1600,850))
bg=ImageTk.PhotoImage(img)
lb=Label(win,image=bg)
lb.place(x=0,y=0)
lmain = Label(win)
lmain.place(x=330, y=50)
lmainr = Label(win)
lmainr.place(x=1050, y=50)

video_file = ''
input_string = ''
def split_string(s_str,count=50):
    per_c=math.ceil(len(s_str)/count)
    c_cout=0
    out_str=''
    split_list=[]
    for s in s_str:
        out_str+=s
        c_cout+=1
        if c_cout == per_c:
            split_list.append(out_str)
            out_str=''
            c_cout=0
    if c_cout!=0:
        split_list.append(out_str)
    return split_list

def exitwindow():
    win.destroy()

    
def submit():
    global video_file, input_string
    secret_key=labelsk.get()
    messages=labelsm.get()
    # otp=labelot.get()
    otp=random.randint(1000, 9999)
    print(f"\n\n\n OTP is : {otp}\n\n\n")
    # bot.sendMessage(ch_id,str(otp))
    message = aes_encrypt(messages, secret_key)
    input_string = message
    lbl=tk.Label(win,text=input_string,font=("elephant",10,"italic"),bg="#0e77bb",fg="black")
    lbl.place(x=100,y=550)
    print(message)
    print(secret_key)
    f = open('Key.txt' ,'w')
    f.write(secret_key)
    f.close()

    f = open('Message.txt' ,'w')
    f.write(input_string)
    f.close()

    f = open('OTP.txt' ,'w')
    f.write(str(otp))
    f.close()

    f = open('Video.txt' ,'w')
    f.write(video_file)
    f.close()
    
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
        
    temp_folder="tmp"
    print("[INFO] tmp directory is created")

    print(video_file)
    vidcap = cv2.VideoCapture(video_file)
    count = 0

    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
        count += 1
        if count > 50:
            break
    
    print('Counts of frames {}'.format(count))
    labelL1=Button(win,text="Embedding",bg="#0e77bb",fg="black",width=20,height=2,font=("times",14,"bold"),activebackground="red", command=embed)
    labelL1.place(x=40,y=420)

def embed():
    global input_string
    print(input_string)
    root="tmp"
    split_string_list=split_string(input_string)
    imgg=cv2.imread("tmp\\0.png")
    cv2.imwrite("param\orginal.jpg", imgg)
    for i in range(0,len(split_string_list)):
        f_name="{}/{}.png".format(root,i)
        secret_enc=lsb.hide(f_name,split_string_list[i])
        secret_enc.save(f_name)
        print("[INFO] frame {} holds {}".format(f_name,split_string_list[i]))
    imggg=cv2.imread("tmp\\0.png")
    cv2.imwrite("param\changed.jpg", imggg)
    original_image_file = "param\\orginal.jpg"
    encrypted_image_file = "param\\changed.jpg"

    psnr, mse = calculate_psnr_mse(original_image_file, encrypted_image_file)
    print("PSNR:", psnr, "dB")
    print("MSE:", mse)

    ec = calculate_embedding_capacity(original_image_file, encrypted_image_file)
    print("Embedding Capacity:", ec, "bytes")
    lbl_enc=tk.Label(win,text="SUCCESS FULLY EMBEDDED \n PARAMETERS ARE  \n PSNR VALUE IS :  {}  \n MSE VALUE IS :  {}   \n  EMBEDDING CAPACITY IS : {} ".format(psnr,mse,ec)
                               ,font=("times",14,"italic"),bg="#0e77bb",fg="black")
    lbl_enc.place(x=250,y=650)
    
##    doneE=Label(win,text="Text Embedded successfully!!!",bg="#0e77bb",fg="black",width=25,height=2,font=("times",18,"bold")).place(x=335,y=430)


def decode_string():
    #frame_extraction(video)
    secret=[]

    f = open('Video.txt' ,'r')
    InputVideo = f.read()
    f.close()

    print('video {} InputVideo {}'.format(video_file, InputVideo))
    
    if str(video_file) == str(InputVideo):
        print('Matched')
        root="tmp"
        print('lenght {}'.format(len(os.listdir(root))))
        for i in range(len(os.listdir(root))):
            f_name="{}/{}.png".format(root,i)
            
            print('f_name {}'.format(f_name))
            secret_dec=lsb.reveal(f_name)
            print('secret_dec {}'.format(secret_dec))
            if secret_dec == None:
                print('break {}'.format(secret_dec))
                break
            secret.append(secret_dec)
        Msgg=""
        for i in secret:
            Msgg += i
        print(Msgg)
        lbl=tk.Label(win,text=Msgg,font=("elephant",10,"italic"),bg="#0e77bb",fg="black")
        lbl.place(x=900,y=550)
        f = open('Key.txt' ,'r')
        keyyy = f.read()
        f.close()
        Msg = aes_decrypt(Msgg, keyyy)#######################################################################################################################
        from recognition import detect
        res=detect()
        if res ==1:
            anss="Your Message is :  "+str(Msg)
        else:
            anss="Happy Birthday"
        labelE=Label(win,text=anss,bg="#0e77bb",fg="black",font=("times",14,"bold"),height=3).place(x=1120,y=600)
##        resultL=join([i for i in secret])
##        print(resultL)
        print('break {}'.format(secret))
    else:
        print("File doesn't Matched")
        labelE=Label(win,text="Wrong Video Choosed ",bg="#0e77bb",fg="black",font=("times",14,"bold")).place(x=1100,y=450)

    labelR1=Button(win,text="Exit",bg="#0e77bb",fg="black",width=20,height=2,font=("times",14,"bold"),activebackground="red",command=exitwindow)
    labelR1.place(x=720,y=500)

def submit1():
    f = open('Key.txt' ,'r')
    old_key = f.read()
    f.close()
    f = open('OTP.txt' ,'r')
    old_otp = f.read()
    f.close()
    check_otp=labelot1.get()

    new_key = labelsk1.get()

    if old_key == new_key and old_otp==check_otp:
        labelR1=Button(win,text="Extraction",bg="#0e77bb",fg="black",width=20,height=2,font=("times",14,"bold"),activebackground="red",command=decode_string)
        labelR1.place(x=720,y=450)
    else:
        print('Entered wrong key')
        labelR1=Label(win,text="Entered wrong\n secret key \n or Entered Wrong OTP",bg="#0e77bb",fg="black",width=20,height=3,font=("times",14,"bold"))
        labelR1.place(x=1100,y=450)

    

def inp1():
##    win.geometry("1400x400")
##    labelRF.configure(height=30)
    global labelsk1,labelot1
    labels1=Label(win,text="secret key",bg="#0e77bb",fg="black",font=("times",16,"bold"))
    labels1.place(x=720,y=250)
    labelsk1=Entry(win,text="",bg="#0e77bb",fg="black",font=("times",16,"bold"))# ,show="*")
    labelsk1.place(x=720,y=300)
    labels1=Label(win,text="Enter Otp",bg="#0e77bb",fg="black",font=("times",16,"bold"))
    labels1.place(x=720,y=350)
    labelot1=Entry(win,text="",bg="#0e77bb",fg="black",font=("times",16,"bold"))# ,show="*")
    labelot1.place(x=720,y=400)
    labelR1=Button(win,text="Submit",bg="#0e77bb",fg="black",width=20,height=2,font=("times",14,"bold"),activebackground="red", command=submit1)
    labelR1.place(x=720,y=450)
    
def choose_vid():
    global video_file
    # C:/Users/sagpa/Downloads/images is the location of the image which you want to test..... you can change it according to the image location you have  
    File = askopenfilename(initialdir='sample', title='Select image for analysis ',
                           filetypes=[('video files', '.mp4')])
    print(File)
    File = File.split('/')
    fileName1 = File[-1]
    video_file = 'sample/'+fileName1
    print(video_file)
##    win.geometry("1400x600")
    vs = cv2.VideoCapture(video_file)
    def video_stream():
        (grabbed, frame) = vs.read()
        if grabbed:
            frame=cv2.resize(frame,(350,380))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(1, video_stream)
        else:
            lmainr.after(1, video_stream)
    video_stream()
    
def inp():
##    win.geometry("1400x400")
##    labelLF.configure(height=30)
    global labelsk,labelsm
    labels=Label(win,text="secret key",bg="#0e77bb",fg="black",font=("times",16,"bold"))
    labels.place(x=90,y=280)
    labelsk=Entry(win,text="",bg="#0e77bb",fg="black",font=("times",16,"bold"),show="*")
    labelsk.place(x=40,y=315)
    labels=Label(win,text="secret msg",bg="#0e77bb",fg="black",font=("times",16,"bold"))
    labels.place(x=90,y=350)
    labelsm=Entry(win,text="",bg="#0e77bb",fg="black",font=("times",16,"bold"))# ,show="*")
    labelsm.place(x=40,y=380)
    # labels=Label(win,text="secret msg",bg="#0e77bb",fg="black",font=("times",16,"bold"))
    # labels.place(x=90,y=410)
    # labelot=Entry(win,text="",bg="#0e77bb",fg="black",font=("times",16,"bold"))# ,show="*")
    # labelot.place(x=40,y=450)

    

    Submit=Button(win,text="Submit",bg="#0e77bb",fg="black",width=20,height=2,font=("times",14,"bold"),activebackground="red",command=submit)
    Submit.place(x=40,y=420)
 
def choose_vide():
    global video_file
    # C:/Users/sagpa/Downloads/images is the location of the image which you want to test..... you can change it according to the image location you have  
    File = askopenfilename(initialdir='sample', title='Select image for analysis ',
                           filetypes=[('video files', '.mp4')])
    File = File.split('/')
    fileName1 = File[-1]
    video_file = 'sample/'+fileName1
    print(video_file)
##    win.geometry("1400x600")
    vs = cv2.VideoCapture(video_file)
    def video_stream():
        (grabbed, frame) = vs.read()
        if grabbed:
            frame=cv2.resize(frame,(350,380))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            lmainr.imgtk = imgtk
            lmainr.configure(image=imgtk)
            lmainr.after(1, video_stream)
        else:
            lmainr.after(1, video_stream)
    video_stream()

        

##labelLF=Label(win,text="",bg="#0e77bb",fg="black",width=40,height=15)
##labelLF.place(x=20,y=50)
labelL=Label(win,text="Encryption",bg="#0e77bb",fg="black",font=("times",14,"bold"))
labelL.place(x=150,y=55)
labelL=Label(win,text="Menu",bg="#0e77bb",fg="black",font=("times",14,"bold"))
labelL.place(x=25,y=55)


labelL1=Button(win,text="Browse i/p Video",bg="#0e77bb",fg="black",width=20,height=2,font=("times",14,"bold"),activebackground="red",command=choose_vid)
labelL1.place(x=40,y=140)
labelL1=Button(win,text="Enter Secret Key",bg="#0e77bb",fg="black",width=20,height=2,font=("times",14,"bold"),activebackground="red",command=inp)
labelL1.place(x=40,y=215)

##labelRF=Label(win,text="",bg="#0e77bb",fg="black",width=40,height=15)
##labelRF.place(x=700,y=50)
labelL=Label(win,text="Decryption",bg="#0e77bb",fg="black",font=("times",14,"bold"))
labelL.place(x=850,y=50)
labelR=Label(win,text="Menu",bg="#0e77bb",fg="black",font=("times",14,"bold"))
labelR.place(x=705,y=55)

labelR1=Button(win,text="Load Embedded video",bg="#0e77bb",fg="black",width=20,height=2,font=("times",14,"bold"),activebackground="red",command=choose_vide)
labelR1.place(x=720,y=100)
labelR1=Button(win,text="Secret key",bg="#0e77bb",fg="black",width=20,height=2,font=("times",14,"bold"),activebackground="red",command=inp1)
labelR1.place(x=720,y=175)

win.mainloop()
