import numpy as np
from ALP4 import *
import time
import os
import cv2

# input image
# DMD\data\test.jpg
dir_name_1="../data/test_resize/"
file_name_1="cameraman_resize.tif"
img_path_1=dir_name_1+file_name_1

dir_name_2="../data/test/"
file_name_2="cameraman.tif"
img_path_2=dir_name_2+file_name_2

if not os.path.exists(dir_name_1):
    raise FileNotFoundError("Such directory not found")
if not os.path.exists(img_path_1):
    raise FileNotFoundError("Such image file not found")
if not os.path.exists(dir_name_2):
    raise FileNotFoundError("Such directory not found")
if not os.path.exists(img_path_2):
    raise FileNotFoundError("Such image file not found")

ImgInput_1 = cv2.imread(img_path_1, cv2.IMREAD_GRAYSCALE)
print("ImgInput:", ImgInput_1)
ImgInput_1=np.flip(ImgInput_1)
ImgInput_2 = cv2.imread(img_path_2, cv2.IMREAD_GRAYSCALE)
print("ImgInput:", ImgInput_2)
##############################

# Load the Vialux .dll
DMD = ALP4(version = '4.3')
# Initialize the device
DMD.Initialize()

# Binary amplitude image (0 or 1)
bitDepth = 1
imgBlack = np.zeros([DMD.nSizeY,DMD.nSizeX])

img_Y,img_X=ImgInput_1.shape
pad_Y,pad_X=DMD.nSizeY-img_Y,DMD.nSizeX-img_X
print("img_Y:",img_Y)
print("pad_Y:", pad_Y)

# padding
ImgTarget_padding_1 = cv2.copyMakeBorder(ImgInput_1,
                                top=0,
                                bottom=pad_Y,
                                left=0,
                                right=pad_X,
                                borderType=cv2.BORDER_CONSTANT,
                                value=(0,0,0))

img_Y,img_X=ImgInput_2.shape
pad_Y,pad_X=DMD.nSizeY-img_Y,DMD.nSizeX-img_X
print("img_Y:",img_Y)
print("pad_Y:", pad_Y)

# padding
ImgTarget_padding_2 = cv2.copyMakeBorder(ImgInput_2,
                                top=0,
                                bottom=pad_Y,
                                left=0,
                                right=pad_X,
                                borderType=cv2.BORDER_CONSTANT,
                                value=(0,0,0))



# imgSeq  = np.concatenate([imgBlack.ravel(),imgWhite.ravel()])
imgSeq  = np.concatenate([ImgTarget_padding_1.ravel(),ImgTarget_padding_2.ravel()])
print("imgSeq:",imgSeq.shape)

# Allocate the onboard memory for the image sequence
DMD.SeqAlloc(nbImg = 2, bitDepth = bitDepth)
# Send the image sequence as a 1D list/array/numpy array
DMD.SeqPut(imgData = imgSeq)


# Set image rate to 50 Hz
# illuminationTime[μs],pictureTime[μs]
DMD.SetTiming(illuminationTime=5000000,pictureTime=5000000)
# Run the sequence in an infinite loop
DMD.Run()
print("DMD RUN")

time.sleep(30)

# Stop the sequence display
DMD.Halt()

time.sleep(5)
# Free the sequence from the onboard memory
DMD.FreeSeq()
# De-allocate the device
DMD.Free()
