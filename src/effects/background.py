from KameraEffectBase import *
from Decoration import Decoration
import Image
import cv
from math import fabs
import ImageChops
class Background(Decoration):
    # DIFF_THRESH = 5
    DIFF_THRESH = 100
    def get_name(cls):
        return "Black & White"
    
    def get_description(cls):
        return "This is sample effect"
    
    def process_image(cls, image, options):
        # mask = cls.get_mask(image, options)
        
        img = Image.new('RGB', image.size, (100,0,0))
        mask = cls.get_mask(image, img)
        cls.addImageMask(img, image, (0,0), mask)
        return img
        
    def get_mask(cls, fg, bg):
        mask = Image.new('1', fg.size)
        width, height = mask.size
        # ImageChops.difference(bg, fg)
        # for row in range(height):
        #     for col in range(width):
        #         (r1, g1, b1) = fg.getpixel((col, row))
        #         (r2, g2, b2) = bg.getpixel((col, row))
        #         if fabs(r1-r2) > cls.DIFF_THRESH and fabs(g1-g2) > cls.DIFF_THRESH and fabs(b1-b2) > cls.DIFF_THRESH:
        #             mask.putpixel((col, row), 1)
        return mask
        
if __name__ == "__main__":
    fg = Image.open("room2.jpg")
    bg = Image.open("room.jpg")
    im = Background().process_image(fg, bg)
    im.show()