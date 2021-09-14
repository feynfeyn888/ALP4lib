from PIL import Image
import numpy as np
from module_.pyueye_example_camera import Camera
from pyueye import ueye
from time import sleep
import time
from datetime import datetime
import os
import cv2

def ImgCap(cap_id, exposure_time, img_y, img_x, path):
    # camera class to simplify uEye API access
    exposure_time=exposure_time/1000
    print((img_y,img_x))
    file_path = path + "\img_{}.jpg".format(str(cap_id))
    cam = Camera()
    cam.init()
    cam.set_colormode(ueye.IS_CM_BGR8_PACKED)
    cam.set_aoi(0,0,img_y,img_x)
    cam.alloc()
    #print(ueye.is_GetImageMem(self.h_cam,buff.mem_ptr))
    cam.set_pixelclock()
    cam.set_framerate()
    # 露光時間(ms). 実験条件に合わせる
    # cam.set_exposure(exposure_time)
    cam.capture_video()
    time.sleep(exposure_time)
    cam.image_file(file_path)
    cam.stop_video()
    cam.exit()

    return file_path

def Random_Binary(nx,ny,pre_sampling,seed=0,Input_Matrix_Flag=0):
    # rand
    np.random.seed(seed)
    if Input_Matrix_Flag==0:
        Input_Matrix = np.random.randint(low=0,high=2,size=(pre_sampling,ny,nx))
    elif Input_Matrix_Flag==1:
        Input_Matrix = np.ones([pre_sampling,ny,nx])
    
    elif Input_Matrix_Flag==2:
        Input_Matrix = np.zeros([pre_sampling,ny,nx])
    
    elif Input_Matrix_Flag==3:
        # 回転確認
        Input_Matrix = np.ones([pre_sampling,ny,nx])*(2**8-1)
        Input_Matrix[:,int(ny*0.1):int(ny*0.3),int(nx*0.1):int(nx*0.3)]=0

    elif Input_Matrix_Flag==4:
        # 符号拡大. カメラとDMDの同期チェック用.
        if nx%100 != 0:
            print("100で割り切れる数字を入力してください")
            exit()
        
        Input_Matrix = np.random.randint(low=0,high=2,size=(pre_sampling,int(ny/100),int(nx/100)))
        Input_Matrix = Input_Matrix.repeat(100,axis=1).repeat(100,axis=2)

    return Input_Matrix

def Padding_Input_Matrix(Input_Matrix,top,bottom,left,right):
    Padding_Input_Matrix=np.pad(Input_Matrix,[(0,0),(top,bottom),(left,right)],'constant')

    return Padding_Input_Matrix.flatten()

############################################################33

if __name__=="__main__":
    #[ms]
    exposure_time=50
    img_directory_path="./"
    img_y,img_x=20,20
    ret=ImgCap(cap_id=0, exposure_time=exposure_time, img_y=img_y, img_x=img_x, path=img_directory_path)
    
    # 読み込み
    Output_Matrix=cv2.imread(img_directory_path+"img_0.jpg",0)
    print("Output_matrix:", Output_Matrix)

    # 
    print(Output_Matrix.reshape(1,img_y*img_x))

    # # save Output Matrix as text file.
    # for i in range(2):
    #     with open(img_directory_path+"test.txt","a") as f:
    #         np.savetxt(f,Output_Matrix.reshape(1,img_y*img_x),fmt="%.0f")
    #     #np.savetxt(img_directory_path+"test.txt",Output_Matrix.reshape(1,img_y*img_x),fmt="%.0f")
    for i in range(2):
        with open(img_directory_path+"test.csv","a") as f:
            np.savetxt(f,Output_Matrix.reshape(1,img_y*img_x),fmt="%.0f")



    # Input_Matrix=Random_Binary(ny=4,nx=3,pre_sampling=1,seed=0,Input_Matrix_Flag=0)
    # print("Random_Binary:",Input_Matrix)
    # print("Input_Matrix.shape",Input_Matrix.shape)
    # print("type",type(Input_Matrix))

    # Reshape_Input_Matrix=Input_Matrix.reshape(1,4*3)
    # print(Reshape_Input_Matrix)
    # print(Reshape_Input_Matrix.shape)

    # ret=Input_Matrix.reshape(2,4*3).T
    # print(ret)

    # ret=Padding_Input_Matrix(Input_Matrix,top=1580,bottom=0,left=2580,right=0)
    # print(ret)
    # print(ret.shape)
