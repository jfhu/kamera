#!/usr/bin/env python
from KameraEffectBase import *
from PIL import Image

class Decoration(KameraEffectBase):
    def get_name(cls):
        return "Decoration"
    
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
        cls.addImageMask(image, dec, p, dec)

    def addImageMask(cls, image, dec, p, mask):
        image.paste(dec, p, mask)
        return image
        
        