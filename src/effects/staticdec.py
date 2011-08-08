#!/usr/bin/env python

from PIL import Image
from Decoration import Decoration

class StaticDec(Decoration):
     
    def get_name(cls):
        return "Static Decoration"
    
    def get_description(cls):
        return "Add decoration image to video"
    
    def process_image(cls, image, options):
        dec = Image.open('../image/mustache.png')
        return cls.addImages(image, dec,[(100, 100), (220, 130)])
        
    def addImages(cls, image, dec, positions):
        for (x, y) in positions:
            cls.addImage(image, dec, (x, y))
        return image
        
    def addImage(cls, image, dec, p):
        image.paste(dec, p, dec)
        return image
