#!/usr/bin/env python

from PIL import Image
from Decoration import Decoration

class StaticDec(Decoration):
    
    path = '../image/'
    
    image_list = {
        'Elephant'      : 'elephant.png',
        'Giraffe'       : 'giraffe.png',
        'Goat'          : 'goat.png',
        'Balloons'      : 'heart_balloons.png',
        'Kiss'          : 'kiss.png',
        'Plumber'       : 'mario.png',
        'Mushroom'      : 'Mushroom.png',
        # FIXME: no 'star.png'
        'Star'          : 'star.png',
        'Shining Star'  : 'PowerStar.png',
        'Heart'         : 'red_heart.png',
    }
    
    image_cache = {}
     
    @classmethod
    def get_name(cls):
        return "Static Decoration"

    @classmethod
    def get_description(cls):
        return "Add decoration image to video"

    @classmethod
    def process_image(cls, image, options):
        ret = image
        for pos in options['positions']:
            ret = cls.add_image(image, pos['name'], pos['position'])
        return ret
        
    """
    def addImages(cls, image, dec, positions):
        for (x, y) in positions:
            cls.addImage(image, dec, (x, y))
        return image
    """

    @classmethod        
    def add_image(cls, image, dec_name, position):
        dec = cls.load_image(dec_name)
        # load the center of image at position
        new_x = position[0] - dec.size[0]/2
        new_y = position[1] - dec.size[1]/2
        image.paste(dec, (new_x, new_y), mask = dec)
        return image

    @classmethod
    def load_image(cls, name):
        if name not in cls.image_cache.keys():
            cls.image_cache[name] = Image.open(cls.path + cls.image_list[name])
        return cls.image_cache[name]
        
