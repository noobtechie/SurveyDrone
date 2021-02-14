import cv2
import numpy as np

class PhotoCapture:
    def __init(self):
        self.path = ""
        self.namePrefix = ''
        self.width = 640
        self.height = 480
        self.imageCount = 0

    def getPath(self):
        return self.path

    def getResolution(self):
        return (self.width, self.height)

    def getNamePrefix(self):
        return self.namePrefix

    def config(self, path, width, height, namePrefix):
        self.path = path
        self.namePrefix = namePrefix
        self.width = width
        self.height = height
        self.imageCount = 0

    def capture(self):
        # Open camera and capture image form it
        cap = cv2.VideoCapture('v4l2src ! video/x-raw,width=640,height=480 ! decodebin ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
        ret,frame = cap.read()

        # Resize to make processing faster
        frame = cv2.resize(frame, (self.width,self.height), interpolation = cv2.INTER_AREA)

        # Create name for the image
        name = "{}_{}.png".format(self.namePrefix, self.imageCount)

        # Write images to disk for debugging
        cv2.imwrite(name, frame)

        # Close camera
        cap.release()

