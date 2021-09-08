import numpy as np
from ALP4 import *
import time
import os
import datetime
from my_module import Random_Binary, Padding_Input_Matrix, ImgCap

# Load the Vialux .dll
DMD = ALP4(version = '4.3')
# Initialize the device
DMD.Initialize()
img_Y,img_X=DMD.nSizeY,DMD.nSizeX

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
pre_sampling=1
ny,nx=1000,1000

# Camera Setup
exposure_time = 150.0

# Binary
Input_Matrix=Random_Binary(ny=ny,nx=nx,pre_sampling=pre_sampling,seed=0,Input_Matrix_Flag=Input_Matrix_Flag)
# print("Input_Matrix.shape:", Input_Matrix.shape)

# reshape
Reshape_Input_Matrix=Input_Matrix.reshape(pre_sampling,ny*nx).T

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

# Save Input_Matrix by text.
today = datetime.date.today()
t_now=datetime.datetime.now().time()
directory_path='.\Input_Matrix\{}'.format(today)
file_path='{}\{}{}'.format(directory_path,t_now.hour,t_now.minute)
# フォルダの有無確認
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
# save Input_Matrix
np.savetxt(file_path,Reshape_Input_Matrix,fmt="%.0f")

img_directory_path=directory_path='.\Img\{}\{}{}'.format(today,t_now.hour,t_now.minute)
if not os.path.exists(img_directory_path):
    os.makedirs(img_directory_path)

# Run the sequence in an infinite loop
DMD.Run()
print("DMD RUN")

for iter in range(pre_sampling):
    print(iter+1)
     # Capture
    ImgCap(cap_id=iter, break_time=display_time, exposure_time=exposure_time, relative_path=img_directory_path)

# Stop the sequence display
DMD.Halt()
print("DMD HALT")

# Free the sequence from the onboard memory
DMD.FreeSeq()
# De-allocate the device
DMD.Free()
print("DMD Free")
