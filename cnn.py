from stegano import lsb
from os.path import isfile,join
import time                                                                
import cv2
import numpy as np
import math
import os
import shutil
from subprocess import call,STDOUT
import subprocess
import random

def Rand(start,end,num):
    res=[]
    for j in range(num):
        res.append(random.randint(start,end))
    return res
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

def frame_extraction(video):
    if not os.path.exists("E:\\videosteg\\tmp"):
        os.makedirs("tmp")
    temp_folder="E:\\videosteg\\tmp"
    print("[INFO] tmp directory is created")

    vidcap = cv2.VideoCapture(video)
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
def encode_string(input_string,root="E:\\videosteg\\tmp\\"):
    split_string_list=split_string(input_string)
    for i in range(0,len(split_string_list)):
        f_name="{}{}.png".format(root,i)
        secret_enc=lsb.hide(f_name,split_string_list[i])
        secret_enc.save(f_name)
        print("[INFO] frame {} holds {}".format(f_name,split_string_list[i]))
global InputVideo
def decode_string(video):
    #frame_extraction(video)
    secret=[]
    print('video {} InputVideo {}'.format(video,main.InputVideo))
    if str(video) == str(main.InputVideo):
        print('Matched')
        root="E:\\videosteg\\tmp\\"
        print('lenght {}'.format(len(os.listdir(root))))
        for i in range(len(os.listdir(root))):
            f_name="{}{}.png".format(root,i)
            print('f_name {}'.format(f_name))
            secret_dec=lsb.reveal(f_name)
            print('secret_dec {}'.format(secret_dec))
            if secret_dec == None:
                print('breakkkkkkk{}'.format(secret_dec))
                break
            secret.append(secret_dec)
            
        print(''.join([i for i in secret]))
        print('breakkkkkkk{}'.format(secret))
    else:
        print('File Matched')
    #clean_tmp()
def clean_tmp(path="E:\\videosteg\\tmp\\"):
    if os.path.exists(path):
        shutil.rmtree(path)
        print("[INFO] tmp files are cleaned up")

def main():
    input_string = input("Enter the input string :")
    f_name=input("enter the name of video :")
    main.InputVideo=f_name
    frame_extraction(f_name)
    subprocess.call(["ffmpeg", "-i",f_name, "-q:a", "0", "-map", "a", "G:\\2022\\Projects\\video_steganography-main\\audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT,shell=True)
    
    encode_string(input_string)
    subprocess.call(["ffmpeg", "-i", "E:\\videosteg\\tmp\\%d.png" , "-vcodec", "png", "E:\\videosteg\\video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT,shell=True)
    
    subprocess.call(["ffmpeg", "-i", "E:\\videosteg\\video.mov", "-i", "E:\\videosteg\\audio.mp3", "-codec", "copy", "video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT,shell=True)
    #clean_tmp()
if __name__ == "__main__":
    while True:
        print("1.Hide a message in video 2.Reveal the secret from video")
        print("any other value to exit")
        choice = input()
        if choice == '1':
            main()

##            print('Sending the OTP')
##            num=4
##            start=0
##            end=9
##            otp=Rand(start,end,num)
##            print('Generated OTP {}'.format(otp))
##            otp=str(otp)
##            print('Enter the OTP :')
##            Ot=[]
##            Ot=str(input()) #[6, 2, 6, 6]
##            otp=str(otp)
##            #otp=listToString1(otp)
##            print('Type {}{}'.format(type(otp),type(Ot)))
##            print('Value {}{}'.format(otp,Ot))
##
##
##            if Ot==otp:
##                print('OTP matched')
##
##                print('Enter the Password :')
##                Ot='hello'
##                OT=str(input()) #[6, 2, 6, 6]
##                print('ot{}'.format(Ot))
##                otp=str(OT)
##                if Ot==otp:
##                    print('Second stage passed')
##                    main()
##                else :
##                    print('Password Not Matched')
##            else:
##                print('OTP Not Matched')
        elif choice == '2':

            decode_string(input("enter the name of video with extension"))

##            print('Sending the OTP')
##            num=4
##            start=0
##            end=9
##            otp=Rand(start,end,num)
##            print('Generated OTP {}'.format(otp))
##            otp=str(otp)
##            print('Enter the OTP :')
##            Ot=[]
##            Ot=str(input()) #[6, 2, 6, 6]
##            otp=str(otp)
##            #otp=listToString1(otp)
##            print('Type {}{}'.format(type(otp),type(Ot)))
##            print('Value {}{}'.format(otp,Ot))
##
##
##            if Ot==otp:
##                print('OTP matched')
##
##                print('Enter the Password :')
##                Ot='bye'
##                OT=str(input()) #[6, 2, 6, 6]
##                print('ot{}'.format(Ot))
##                otp=str(OT)
##                if Ot==otp:
##                    print('Second stage passed')
##                    decode_string(input("enter the name of video with extension"))
##                else :
##                    print('Password Not Matched')
##            else:
##                print('OTP Not Matched')
##            
        else:
            break
