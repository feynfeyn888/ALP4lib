from PIL import Image
import numpy as np
from module_.pyueye_example_camera import Camera
from pyueye import ueye
from time import sleep
import time
from datetime import datetime
import os
import cv2

def ImgCap(cap_id, break_time, exposure_time, relative_path, img_y=1000, img_x=1000):
    # camera class to simplify uEye API access
    file_name = relative_path + "\img_{}.jpg".format(str(cap_id))
    cam = Camera()
    cam.init()
    cam.set_colormode(ueye.IS_CM_BGR8_PACKED)
    cam.set_aoi(0,0, img_y, img_x)
    cam.alloc()
    #print(ueye.is_GetImageMem(self.h_cam,buff.mem_ptr))
    cam.set_pixelclock()
    cam.set_framerate()
    # 露光時間(ms). 実験条件に合わせる
    cam.set_exposure(exposure_time)
    cam.capture_video()
    time.sleep(1)
    cam.image_file(file_name)
    cam.stop_video()
    cam.exit()
    print(datetime.now())
    print("capture")
    time.sleep(break_time)

def Random_Binary(nx,ny,pre_sampling,seed=0,Input_Matrix_Flag=0):
    # rand
    np.random.seed(seed)
    if Input_Matrix_Flag==0:
        Input_Matrix = np.random.randint(low=0,high=2,size=(pre_sampling,ny,nx))*(2**8-1)

    elif Input_Matrix_Flag==1:
        Input_Matrix = np.ones([pre_sampling,ny,nx])*(2**8-1)
    
    elif Input_Matrix_Flag==2:
        Input_Matrix = np.zeros([pre_sampling,ny,nx])
    
    elif Input_Matrix_Flag==3:
        # 回転確認
        Input_Matrix = np.ones([pre_sampling,ny,nx])*(2**8-1)
        Input_Matrix[:,int(ny*0.1):int(ny*0.3),int(nx*0.1):int(nx*0.3)]=0

    elif Input_Matrix_Flag==4:
        # 符号拡大. カメラとDMDの同期チェック用.
        if nx%100 != 0:
            print("100で割り切る数字を入力してください")
            exit()
        
        Input_Matrix = np.random.randint(low=0,high=2,size=(pre_sampling,int(ny/100),int(nx/100)))*(2**8-1)
        Input_Matrix = Input_Matrix.repeat(100,axis=1).repeat(100,axis=2)

    return Input_Matrix

def Padding_Input_Matrix(Input_Matrix,top,bottom,left,right):
    Padding_Input_Matrix=np.pad(Input_Matrix,[(0,0),(top,bottom),(left,right)],'constant')
    print(Padding_Input_Matrix)

    return Padding_Input_Matrix.flatten()

def Resize_img(path,img_y,img_x):
    img = Image.open(path)
    img_resize = img.resize((img_y, img_x), Image.LANCZOS)
    img_resize.save(path)

############################################################33

if __name__=="__main__":

    Input_Matrix=Random_Binary(ny=20,nx=20,pre_sampling=1,seed=0,Input_Matrix_Flag=4)
    print("Random_Binary:",Input_Matrix)
    print("Input_Matrix.shape",Input_Matrix.shape)
    print("type",type(Input_Matrix))

    ret=Padding_Input_Matrix(Input_Matrix,top=1580,bottom=0,left=2580,right=0)
    print(ret)
    print(ret.shape)