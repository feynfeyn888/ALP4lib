import numpy as np
from ALP4 import *
import time
import os
import cv2
from my_module import Random_Binary, Padding_Input_Matrix, ImgCap

# Load the Vialux .dll
DMD = ALP4(version = '4.3')
# Initialize the device
DMD.Initialize()
img_Y,img_X=DMD.nSizeY,DMD.nSizeX

#################################3

# input image
# DMD\data\test.jpg
dir_name_1="../data/test_resize/"
file_name_1="cameraman_resize.tif"
img_path_1=dir_name_1+file_name_1

if not os.path.exists(dir_name_1):
    raise FileNotFoundError("Such directory not found")
if not os.path.exists(img_path_1):
    raise FileNotFoundError("Such image file not found")


##############################

# Binary amplitude image (0 or 1)
bitDepth = 1

# Display Time on DMD(~10**7[μs]). 
# display_time=t[s](t=1~10)
display_time=1

# 0:Random Binary, 1:Ones, 2:Zeros, 3:Partially Ones, 4:Shifted Ones
Input_Matrix_Flag=4
# up/down/left/right inversion
Invertion_Flag=1

## Input Matrix
pre_sampling=100
ny,nx=1000,1000

# Binary
Input_Matrix=Random_Binary(ny=ny,nx=nx,pre_sampling=pre_sampling,seed=0,Input_Matrix_Flag=Input_Matrix_Flag)
# print("Input_Matrix.shape:", Input_Matrix.shape)

# Save Input_Matrix by text.


# up/down/left/right inversion
if Invertion_Flag==1:
    Input_Matrix = Input_Matrix[:,::-1,::-1]

ret=Padding_Input_Matrix(Input_Matrix,top=0,bottom=img_Y-ny,left=0,right=img_X-nx)
print("ret.shape:",ret.shape)

# # 0
# Input_Matrix=Random_Binary(ny=ny,nx=nx,pre_sampling=pre_sampling,seed=0,Flag=2)
# print("Input_Matrix.shape:", Input_Matrix.shape)
# ret_=Padding_Input_Matrix(Input_Matrix,top=Y-ny,bottom=0,left=X-nx,right=0)

# np.concatenate:reshape 1d_array
# for _ in range(len(Input_Matrix))
# imgSeq = np.concatenate([ret,ret_])
imgSeq=ret
print("ImgSeq",imgSeq)
print("Img.shape:",imgSeq.shape)
# Allocate the onboard memory for the image sequence

DMD.SeqAlloc(nbImg = pre_sampling, bitDepth = bitDepth)
    # nbImg:Number of images in the sequence(int)
    # bitDepth:1(on-off)-8(256 pwm grayscale levels)(int)

# Send the image sequence as a 1D list/array/numpy array
DMD.SeqPut(imgData = imgSeq)

# Set image rate to 50 Hz
# illuminationTime[μs],pictureTime[μs]
DMD.SetTiming(illuminationTime=display_time*10**6,pictureTime=display_time*10**6)

# Run the sequence in an infinite loop
DMD.Run()
print("DMD RUN")

for i in range(pre_sampling):
    print(i+1)
    time.sleep(display_time)

# Stop the sequence display
DMD.Halt()
print("DMD HALT")

# Free the sequence from the onboard memory
DMD.FreeSeq()
# De-allocate the device
DMD.Free()
print("DMD Free")
