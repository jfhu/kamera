#!/usr/bin/env python
from KameraEffectBase import *

import Image
import ImageFilter
import numpy

class Other(KameraEffectBase):
    
    options = {}

    @classmethod
    def get_name(cls):
        return "Color & Flip"

    @classmethod
    def get_description(cls):
        return "This is miscellaneous effect"
    
    @classmethod
    def process_image(cls, image, options):
        cls.options = options
        if options['color']:
            image = cls.process_color(image, options['color'])
        if options['mirror']:
            image = cls.process_mirror(image, options['mirror'])
        return image

    @classmethod
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
    
    @classmethod
    def process_color(cls, img, mode):
        """
        'Black/White', 'Red Only', 'Green Only', 'Blue Only', 'R<->B', 'R<->G', 'B<->G', 'R->G->B->R', 'R->B->G->R'
        """
        arr = numpy.asarray(img)
        arr = numpy.copy(arr)
        if mode == 'Black/White':
            img = img.convert("L")
        elif mode == 'Red Only':
            arr[:, :, 1:3] = 0
            img = Image.fromarray(arr)
        elif mode == 'Green Only':
            arr[:, :, 0] = 0
            arr[:, :, 2] = 0
            img = Image.fromarray(arr)
        elif mode == 'Blue Only':
            arr[:, :, 0:2] = 0
            img = Image.fromarray(arr)
        elif mode == 'R<->B':
            tmp = numpy.copy(arr[:,:,0])
            arr[:,:,0] = arr[:,:,1]
            arr[:,:,1] = tmp
            img = Image.fromarray(arr)
        elif mode == 'R<->G':
            tmp = numpy.copy(arr[:,:,0])
            arr[:,:,0] = arr[:,:,2]
            arr[:,:,2] = tmp
            img = Image.fromarray(arr)
        elif mode == 'B<->G':
            tmp = numpy.copy(arr[:,:,1])
            arr[:,:,1] = arr[:,:,2]
            arr[:,:,2] = tmp
            img = Image.fromarray(arr)
        elif mode == 'R->G->B->R':
            tmp = numpy.copy(arr[:,:,2])
            arr[:,:,2] = arr[:,:,1]
            arr[:,:,1] = arr[:,:,0]
            arr[:,:,0] = tmp
            img = Image.fromarray(arr)
        elif mode == 'R->B->G->R':
            tmp = numpy.copy(arr[:,:,0])
            arr[:,:,0] = arr[:,:,1]
            arr[:,:,1] = arr[:,:,2]
            arr[:,:,2] = tmp
            img = Image.fromarray(arr)
        return img
    
if __name__ == "__main__":
    img = Image.open("room2.jpg")
    img_flipped = mirror_v(img)
    img_flipped.show()