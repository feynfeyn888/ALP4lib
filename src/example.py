import numpy as np
from ALP4 import *
import time
import os
import cv2

# input image
# DMD\data\test.jpg
dir_name="../data/test_resize/"
file_name="cameraman_resize.tif"
img_path=dir_name+file_name

if not os.path.exists(dir_name):
    raise FileNotFoundError("Directory not found")
if not os.path.exists(img_path):
    raise FileNotFoundError("Image file not found")

ImgInput = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
print("ImgInput:", ImgInput)

##############################

# Load the Vialux .dll
DMD = ALP4(version = '4.3')
# Initialize the device
DMD.Initialize()

# Binary amplitude image (0 or 1)
bitDepth = 1  
imgBlack = np.zeros([DMD.nSizeY,DMD.nSizeX])

if ImgInput is None:
    # rand
    np.random.seed(seed=0)
    imgBinaryRand = np.random.randint(low=0,high=2,size=(DMD.nSizeY//4,DMD.nSizeX//4))*(2**8-1)
    imgTarget=imgBinaryRand
else:
    imgTarget=ImgInput

img_Y,img_X=imgTarget.shape
pad_Y,pad_X=DMD.nSizeY-img_Y,DMD.nSizeX-img_X
print("img_Y:",img_Y)
print("pad_Y:", pad_Y)

print(imgTarget)
print(type(imgTarget))

#cv2.imshow("test1", imgTarget)
#cv2.waitKey(10)

# padding
imgTarget_padding = cv2.copyMakeBorder(imgTarget,
                                top=0,
                                bottom=pad_Y,
                                left=0,
                                right=pad_X,
                                borderType=cv2.BORDER_CONSTANT,
                                value=(0,0,0))

#cv2.imshow("test2", imgTarget_padding)
#cv2.waitKey(10)

# imgSeq  = np.concatenate([imgBlack.ravel(),imgWhite.ravel()])
imgSeq  = np.concatenate([imgBlack.ravel(),imgTarget_padding.ravel()])

# Allocate the onboard memory for the image sequence
DMD.SeqAlloc(nbImg = 2, bitDepth = bitDepth)
# Send the image sequence as a 1D list/array/numpy array
DMD.SeqPut(imgData = imgSeq)


# Set image rate to 50 Hz (if default value 20000)
DMD.SetTiming(pictureTime = 50000)

# Run the sequence in an infinite loop
DMD.Run()

time.sleep(10)

# Stop the sequence display
DMD.Halt()
# Free the sequence from the onboard memory
DMD.FreeSeq()
# De-allocate the device
DMD.Free()
