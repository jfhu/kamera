#!/usr/bin/env python

from PIL import Image

class Effect:
    enable = False
    # modify image to add on effect
    def render(self, img):
        # if this effect is disabled, then do nothing
        if enable == False:
            return img
        else:
            return apply(img)

    def apply(self, img):
        pass
        