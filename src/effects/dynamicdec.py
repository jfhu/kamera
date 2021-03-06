#!/usr/bin/env python
import sys
import cv
from Decoration import Decoration
from PIL import Image
import numpy

class DynamicDec(Decoration):
    path = '../image/'
    
    image_list = {
        'Tiara'         : 'crown.png',
        'Crown'         : 'bigcrown.png',
        'Big Eyes'      : 'eye.png',
        'Glasses'       : 'glasses.png',
        'Goggles'       : 'goggle.png',
        'Mustache'      : 'mustache.png',
        'Beard'         : 'beard.png',
        'Kiss'          : 'kiss.png'
    }
    
    @classmethod
    def get_name(cls):
        return "DynamicDecoration"
    
    @classmethod
    def get_description(cls):
        return "This is sample effect"
    
    @classmethod
    def process_image(cls, image, options):
        frame = cv.CreateImage(cv.GetSize(image), 8, 3)
        cv.CvtColor(image, frame, cv.CV_BGR2RGB)
        pil_frame = Image.fromstring("RGB", cv.GetSize(frame), frame.tostring())
        data = numpy.asarray(pil_frame)
        data = numpy.fliplr(data)
        pil_frame = Image.fromarray(data)
        
        if options['decoration'] == ['None', 'None', 'None', 'None']:
            return pil_frame
        face = cls.detect_face(image)
        for (x,y,w,h),n in face:
            for image in options['decoration']:
                if image != 'None':
                    print cls.path + cls.image_list[image]
                    dec = Image.open(cls.path + cls.image_list[image])
                    pil_frame.paste( dec, (x, y), mask = dec)
        return pil_frame
    
    @classmethod
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

