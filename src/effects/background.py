from KameraEffectBase import *
from Decoration import Decoration
import Image
import ImageFilter
import cv
from math import fabs
import ImageChops
import numpy

class Background(Decoration):
    DIFF_THRESH = 15
    
    mask_cache = None
    
    @classmethod
    def get_name(cls):
        return "Black & White"
    
    @classmethod
    def get_description(cls):
        return "This is sample effect"
    
    @classmethod
    def process_image(cls, image, options):
        bg = options['bg']
        img = options['bgNew']
        if bg is None or img is None:
            return image
        img = img.copy()
        
        mask = cls.get_mask(image, bg)
        cls.addImageMask(img, image, (0,0), mask)
        return img
    
    @classmethod
    def get_mask(cls, fg, bg):
        fg = fg.filter(ImageFilter.BLUR)
        numfg = numpy.asarray(fg)
        numbg = numpy.asarray(bg)
        diff_r = numpy.subtract(numfg[:,:,0], numbg[:,:,0])
        diff_r = numpy.logical_or(diff_r > cls.DIFF_THRESH, diff_r < -cls.DIFF_THRESH)
        diff_g = numpy.subtract(numfg[:,:,1], numbg[:,:,1])
        diff_g = numpy.logical_or(diff_g > cls.DIFF_THRESH, diff_g < -cls.DIFF_THRESH)
        diff_b = numpy.subtract(numfg[:,:,2], numbg[:,:,2])
        diff_b = numpy.logical_or(diff_b > cls.DIFF_THRESH, diff_b < -cls.DIFF_THRESH)
        diff = 1 * diff_r + 1 * diff_g + 1 * diff_b
        diff = numpy.logical_and(diff > 2, diff > 2)
        data = 255 * diff;
        mask = Image.fromarray(data.astype('int8'))
        mask = mask.convert("L")
        mask = mask.filter(ImageFilter.MedianFilter(5))
        return mask
    
    # @classmethod
    # def RGB2HSV(cls, image):
    #     # convert it to hsv array
    #     # http://stackoverflow.com/questions/4890373/detecting-thresholds-in-hsv-color-space-from-rgb-using-python-pil
    #     a = numpy.asarray(image, int)
    #     R, G, B = a.T
    #     m = numpy.min(a, 2).T
    #     M = numpy.max(a, 2).T
    #     C = M-m
    #     Cmsk = C!=0
    #     # Hue
    #     H = numpy.zeros(R.shape, int)
    #     mask = (M==R)&Cmsk
    #     H[mask] = numpy.mod(60*(G-B)/C, 360)[mask]
    #     mask = (M==G)&Cmsk
    #     H[mask] = (60*(B-R)/C + 120)[mask]
    #     mask = (M==B)&Cmsk
    #     H[mask] = (60*(R-G)/C + 240)[mask]
    #     H *= 255
    #     H /= 360 # if you prefer, leave as 0-360, but don't convert to uint8
    #     # Value
    #     V = M
    #     # Saturation
    #     S = numpy.zeros(R.shape, int)
    #     S[Cmsk] = ((255*C)/V)[Cmsk]
    #     return (H, S, V)
    # 
    # @classmethod
    # def get_mask_2(cls, fg, bg):
    #     print cls.mask_cache
    #     if cls.mask_cache and cls.mask_cache['count'] > 0:
    #         print cls.mask_cache['count']
    #         cls.mask_cache['count'] -= 1
    #         return cls.mask_cache['mask']
    #     
    #     print 'here'
    #     fg = cls.RGB2HSV(fg)
    #     diff_h = numpy.subtract(fg[0], bg[0])
    #     diff_s = numpy.subtract(fg[1], bg[1])
    #     diff_h = numpy.logical_or(diff_h>20, diff_h<-20)
    #     diff_s = numpy.logical_or(diff_s>30, diff_s<-30)
    #     diff = 1 * diff_h + 1 * diff_s
    #     diff = numpy.logical_and(diff>1, diff>0)
    #     diff = 255 * diff
    #     diff = numpy.transpose(diff)
    #     mask = Image.fromarray(diff.astype('int8'))
    #     mask = mask.convert("L")
    #     mask = mask.filter(ImageFilter.MedianFilter(30))
    #     
    #     cls.mask_cache = {'mask':mask, 'count':3}
    #     return mask
        
        
if __name__ == "__main__":
    fg = Image.open("room2.jpg")
    bg = Image.open("room.jpg")
    im = Background().process_image(fg, bg)
    im.show()