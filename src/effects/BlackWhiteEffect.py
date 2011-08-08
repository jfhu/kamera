from KameraEffectBase import *

import ImageFilter

class BlackWhiteEffect(KameraEffectBase):

    @classmethod
    def get_name(cls):
        return "Black & White"
    
    @classmethod
    def get_description(cls):
        return "This is sample effect"
    
    @classmethod
    def process_image(cls, image, options):
        image = image.convert("L")
        return image