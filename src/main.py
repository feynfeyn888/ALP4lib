import numpy as np
from ALP4 import *
import time
import os
import sys
import cv2
import datetime
from my_module import Random_Binary, Padding_Input_Matrix, ImgCap

    ##########################
    # before loop
    # Generate folder

    # in loop
    # 1. Generate Input Matrix
    # 2. Save Input Matrix to CSV file
    # 3. DMD Start
    # 4. Capture and save Output Matrix to CSV file
    # 5. DMD Stop

def main():

    bitDepth=1 # Binary amplitude image (0 or 1)
    nbImg=1    # Number of transfered images to DMD in 1 loop.

    # Display Time on DMD(~10**7[μs]). 
    # display_time=t[s](t=1~10)
    display_time=1

    # 0:Random Binary, 1:Ones, 2:Zeros, 3:Partially Ones, 4:Shifted Ones
    Input_Matrix_Flag=0
    # up/down/left/right inversion
    Invertion_Flag=1

    ## Input Matrix
    pre_sampling=1
    ny,nx=10,10

    # Camera Setup
    exposure_time = 100 # [ms]
    img_cap_y,img_cap_x=20,20

    # Save Input_Matrix by text.
    today = datetime.date.today()
    t_now=datetime.datetime.now().time()
    with open("../path_info.txt","w") as f:
        f.write("{},{}{}".format(today,t_now.hour,t_now.minute))

    directory_path='..\data\{}\{}{}'.format(today,t_now.hour,t_now.minute)
    img_directory_path='..\data\{}\{}{}\Img'.format(today,t_now.hour,t_now.minute)

    # check if folder exist.
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    if not os.path.exists(img_directory_path):
        os.makedirs(img_directory_path)

    with open('..\data\{}\{}{}\info.txt'.format(today,t_now.hour,t_now.minute),"w") as f:
        f.write("pre_sampling:{}\n input_size:({},{})\n exposure_time:{}\n output_size:({},{})".format(pre_sampling,ny,nx,exposure_time,img_cap_y,img_cap_x))


    for iter in range(pre_sampling):
        index=iter+1
        print("loop:",index)
        # Load the Vialux .dll
        DMD = ALP4(version = '4.3')
        # Initialize the device
        DMD.Initialize()
        img_Y,img_X=DMD.nSizeY,DMD.nSizeX

        # pre_sampling=1, ret is 2d array
        Input_Matrix=Random_Binary(ny=ny,nx=nx,pre_sampling=nbImg,seed=index,Input_Matrix_Flag=Input_Matrix_Flag)
        # print("Input_Matrix.shape:", Input_Matrix.shape)

        # save Input_Matrix. あとで転置する
        with open(directory_path+"\input_matrix.csv","a") as f:
            np.savetxt(f,Input_Matrix.reshape(nbImg,ny*nx),fmt="%.0f")

        # up/down/left/right inversion
        if Invertion_Flag==1:
            Input_Matrix = Input_Matrix[:,::-1,::-1]

        imgSeq=Padding_Input_Matrix(Input_Matrix,top=0,bottom=img_Y-ny,left=0,right=img_X-nx)*(2**8-1)
        # print("Img.shape:",imgSeq.shape)

        # Allocate the onboard memory for the image sequence
        DMD.SeqAlloc(nbImg = nbImg, bitDepth = bitDepth)
            # nbImg:Number of images in the sequence(int)
            # bitDepth:1(on-off)-8(256 pwm grayscale levels)(int)

        # Send the image sequence as a 1D list/array/numpy array
        DMD.SeqPut(imgData = imgSeq)

        # Set image rate to 50 Hz
        # illuminationTime[μs],pictureTime[μs]
        DMD.SetTiming(illuminationTime=display_time*10**6,pictureTime=display_time*10**6)

        # Run the sequence in an infinite loop
        DMD.Run()

        time.sleep(1)

        # Capture
        saved_img_path=ImgCap(cap_id=index,exposure_time=exposure_time,img_y=img_cap_y,img_x=img_cap_x,path=img_directory_path)
        Output_Matrix=cv2.imread(saved_img_path,0)
        # save Output Matrix as text file.
        with open(directory_path+"\output_matrix.csv","a") as f:
            np.savetxt(f,Output_Matrix.reshape(nbImg,img_cap_y*img_cap_x),fmt="%.0f")

        # Stop the sequence display
        DMD.Halt()
        # Free the sequence from the onboard memory
        DMD.FreeSeq()
        # De-allocate the device
        DMD.Free()

if __name__ == "__main__":
    main()