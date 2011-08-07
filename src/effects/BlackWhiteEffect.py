from KameraEffectBase import *

import ImageFilter

class BlackWhiteEffect(KameraEffectBase):

    def get_name(cls):
        return "Black & White"
    
    def get_description(cls):
        return "This is sample effect"
    
    def process_image(cls, image):
        image = image.convert("L")
        return image