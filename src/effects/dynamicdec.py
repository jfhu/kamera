#!/usr/bin/env python
import sys
import cv
from Decoration import Decoration
from PIL import Image
import numpy

class DynamicDec(Decoration):
    def get_name(cls):
        return "DynamicDecoration"
    
    def get_description(cls):
        return "This is sample effect"
    
    def process_image(cls, image, options):
        frame = cv.CreateImage(cv.GetSize(image), 8, 3)
        cv.CvtColor(image, frame, cv.CV_BGR2RGB)
        pil_frame = Image.fromstring("RGB", cv.GetSize(frame), frame.tostring())
        data = numpy.asarray(pil_frame)
        data = numpy.fliplr(data)
        pil_frame = Image.fromarray(data)
        
        dec = Image.open('../image/beard.png')
        face = cls.detect_face(image)
        for (x,y,w,h),n in face:
            pil_frame = cls.addImage(pil_frame, dec, (x, y))
        
        return pil_frame
            
    def detect_face(cls, image):
        image_size = cv.GetSize(image)
        cv.Flip(image, None, 1)
        # create grayscale version
        grayscale = cv.CreateImage(image_size, 8, 1)
        cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
        
        # create storage
        storage = cv.CreateMemStorage(0)
        # equalize histogram
        cv.EqualizeHist(grayscale, grayscale)
        # detect objects
        cascade = cv.Load('haarcascade_frontalface_alt.xml')
        # cascade = cv.Load('haarcascade_eye.xml')
        faces = cv.HaarDetectObjects(grayscale, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (50, 50))
        if faces:
            print 'face detected!'
        return faces

