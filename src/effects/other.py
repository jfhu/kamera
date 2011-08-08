#!/usr/bin/env python
from KameraEffectBase import *

import Image

import ImageFilter


class Other(KameraEffectBase):

    def get_name(cls):
        return "Color & Flip"
    
    def get_description(cls):
        return "This is miscellaneous effect"
    
    def process_image(cls, image, options):
        # image = cls.mirror_wrapper(image, 'verticle')
        image = cls.color(image, 'redonly')
        return image

    def mirror_wrapper(cls, img, mode):
        if mode == None:
            return img
        if mode == "verticle":
            return cls.mirror_v(img)
        else:
            return cls.mirror_h(img)
        
    def mirror_v(cls, img):
        mirror = img.copy()
        width, height = img.size
        for row in range(height):
            for col in range(width/2):
                (r, g, b) = img.getpixel((col, row))
                mirror.putpixel((width - col - 1, row), (r, g , b))
        return mirror

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