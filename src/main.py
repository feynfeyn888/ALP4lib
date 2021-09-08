import numpy as np
from ALP4 import *
import time
import datetime
import os
import cv2
from my_module import ImgCap
from my_module import Random_Binary

today = datetime.date.today()
now=datetime.now()

# Load the Vialux .dll
DMD = ALP4(version = '4.3')
# Initialize the device
DMD.Initialize()

# number of sampling
pre_sampling=1000

# exposure time(ms)
exposure_time = 150.0

##################################################

# Input_Matirx
Input_Matrix=Random_Binary(nx=DMD.nSizeY, ny=DMD.nSizeX, pre_sampling=1, seed=0)
ImgBinaryRand = Input_Matrix*(2**8-1)

directory_path='.\Input_Matrix\{}'.format(today)
file_path='{}}\{}'.format(directory_path,now)
# フォルダの有無確認
if not os.path.exist(directory_path):
    os.makedirs(directory_path)
with open(file_path,mode='w') as f:
    f.write(ImgBinaryRand)


# img path
img_directory_path='.\Img\{}'.format(today)
# フォルダの有無確認
if not os.path.exist(img_directory_path):
    os.makedirs(img_directory_path)

# Binary amplitude image (0 or 1)
bitDepth = 1
ImgBlack = np.zeros([DMD.nSizeY,DMD.nSizeX])

img_Y,img_X=ImgBinaryRand.shape
pad_Y,pad_X=DMD.nSizeY-img_Y,DMD.nSizeX-img_X

# padding
ImgTarget_padding = cv2.copyMakeBorder(ImgBinaryRand,
                                top=0,
                                bottom=pad_Y,
                                left=0,
                                right=pad_X,
                                borderType=cv2.BORDER_CONSTANT,
                                value=(0,0,0))

for iter in range(pre_sampling):
    # imgSeq  = np.concatenate([imgBlack.ravel(),imgWhite.ravel()])
    imgSeq  = np.concatenate([ImgBlack.ravel(),ImgTarget_padding.ravel()])

    # Allocate the onboard memory for the image sequence
    DMD.SeqAlloc(nbImg = 2, bitDepth = bitDepth)
    # Send the image sequence as a 1D list/array/numpy array
    DMD.SeqPut(imgData = imgSeq)


    # Set image rate to 50 Hz
    DMD.SetTiming(pictureTime = 50000)

    # Run the sequence in an infinite loop
    DMD.Run()

    time.sleep(1)

    # Stop the sequence display
    DMD.Halt()
    # Free the sequence from the onboard memory
    DMD.FreeSeq()
    # De-allocate the device
    DMD.Free()
    
    # Capture
    ImgCap(cap_id=iter, break_time=1, exposure_time=exposure_time, relative_path=img_directory_path)