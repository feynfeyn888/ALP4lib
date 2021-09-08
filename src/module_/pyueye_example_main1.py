#!/usr/bin/env python

from pyueye_example_camera import Camera
from pyueye import ueye
import time
import cv2
import numpy as np

def main():
    for i in range(6):
    # camera class to simplify uEye API access
        cam = Camera()
        cam.init()
        cam.set_colormode(ueye.IS_CM_BGR8_PACKED)
        cam.set_aoi(0,0, 2000, 2000)
        cam.alloc()
        cam.set_pixelclock()
        cam.set_framerate()
        cam.set_exposure()
        cam.capture_video()
        time.sleep(0.5)
        cam.image_file(i)
        cam.stop_video()
        cam.exit()

if __name__ == "__main__":
    main()



