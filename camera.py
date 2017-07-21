# encoding: utf8

"""
Created on 2017.07.12

@author: yalei
"""


from picamera import PiCamera
from config import *


def capture_now(filename):
    try:
        camera = PiCamera()
        camera.capture(filename)
        camera.close()
        return 0, u'success'
    except Exception as e:
        return 1, str(e)
# camera.resolution = RESOLUTION
# camera.framerate = FPS