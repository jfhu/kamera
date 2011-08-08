#!/usr/bin/env python
from KameraEffectBase import *

import Image
import ImageFilter
import numpy

class Other(KameraEffectBase):
    
    options = {}

    def get_name(cls):
        return "Color & Flip"
    
    def get_description(cls):
        return "This is miscellaneous effect"
    
    def process_image(cls, image, options):
        cls.options = options
        if options['color']:
            image = cls.process_color(image, options['color'])
        if options['mirror']:
            image = cls.process_mirror(image, options['mirror'])
        return image

    def process_mirror(cls, img, mode):
        if mode == 'Vertical':
            org = numpy.asarray(img)
            flip = numpy.fliplr(org)
            data1 = numpy.hsplit(org, 2)
            data2 = numpy.hsplit(flip, 2)
            data = numpy.hstack((data1[0], data2[1]))
            img = Image.fromarray(data)
        elif mode == 'Horizontal':
            org = numpy.asarray(img)
            flip = numpy.flipud(org)
            data1 = numpy.vsplit(org, 2)
            data2 = numpy.vsplit(flip, 2)
            data = numpy.vstack((data1[0], data2[1]))
            img = Image.fromarray(data)
        return img
    
    def process_color(cls, img, mode):
        return img

    def mirror_h(cls, img):
        mirror = img.copy()
        width, height = img.size
        for row in range(height/2):
            for col in range(width):
                (r, g, b) = img.getpixel((col, row))
                mirror.putpixel((col, height - row - 1), (r, g , b))
        return mirror
        
    def color(cls, img, mode):
        if mode == None:
            return img
        cycle = img.copy()
        width, height = img.size
        for row in range(height):
            for col in range(width):
                (r, g, b) = img.getpixel((col, row))
                if mode == 'blackwhite':
                    black = (r + b + g) /3
                    cycle.putpixel((col, row), (black, black , black))
                elif mode == 'redonly':
                    cycle.putpixel((col, row), (r, 0 , 0))
                elif mode == 'blueonly':
                    cycle.putpixel((col, row), (0, 0 , b))
                elif mode == 'greenonly':
                    cycle.putpixel((col, row), (0, g , 0))
                elif mode == 'rb':
                    cycle.putpixel((col, row), (r, 0, b))
                elif mode == 'rg':
                    cycle.putpixel((col, row), (r, g, b))
                elif mode == 'bg':
                    cycle.putpixel((col, row), (0, g , b))
                elif mode == 'rgbr':
                    cycle.putpixel((col, row), (b, r, g))
                elif mode == 'rbrg':
                    cycle.putpixel((col, row), (g, b , r))
        return cycle
        
if __name__ == "__main__":
    img = Image.open("room2.jpg")
    img_flipped = mirror_v(img)
    img_flipped.show()