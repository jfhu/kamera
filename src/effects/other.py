#!/usr/bin/env python

from PIL import Image

class Other(Effect):
    DISABLE = 'None'
    MV = "sth"
    MH = "sthelse"
    
    def __init__():
        self.edict = {'color': DISABLE, 'mirror': DISABLE}
        
    def seteffect(self, cmode, mmode):
        if cmode == 'original'
            self.edict['color'] = DISABLED
        else:
            self.edict['color'] = cmode
        self.edict['mirror'] = mmode
        if self.edict['color'] == DISABLED and self.edict['mirror'] = DISABLED:
            self.enable = False
        else:
            self.enable = True
        
    def apply(self, img):
        img = color(img, self.edict['color'])
        img = mirror_wrapper(img, self.edict['mirror'])
        return img

    def mirror_wrapper(img, mode):
        if mode == self.DISABLE:
            return img
        if mode == MV:
            return mirror_v(img)
        else
            return mirror_h(img)
        
    def mirror_v(img):
        mirror = img.copy()
        width, height = img.size
        for row in range(height):
            for col in range(width/2):
                (r, g, b) = img.getpixel((col, row))
                mirror.putpixel((width - col - 1, row), (r, g , b))
        return mirror

    def mirror_h(img):
        mirror = img.copy()
        width, height = img.size
        for row in range(height/2):
            for col in range(width):
                (r, g, b) = img.getpixel((col, row))
                mirror.putpixel((col, height - row - 1), (r, g , b))
        return mirror
        
    def color(img, mode):
        if mode == self.DISABLE:
            return img
        cycle = img.copy()
        width, height = img.size
        for row in range(height):
            for col in range(width):
                (r, g, b) = img.getpixel((col, row))
                if mode == 'blackwhite':
                    black = (r + b + g) /3
                    cycle.putpixel((col, row), (black, black , black))
                else if mode == 'redonly':
                    cycle.putpixel((col, row), (r, 0 , 0))
                else if mode == 'blueonly':
                    cycle.putpixel((col, row), (0, 0 , b))
                else if mode == 'greenonly':
                    cycle.putpixel((col, row), (0, g , 0))
                else if mode == 'rb':
                    cycle.putpixel((col, row), (r, 0, b))
                else if mode == 'rg':
                    cycle.putpixel((col, row), (r, g, b))
                else if mode == 'bg':
                    cycle.putpixel((col, row), (0, g , b))
                else if mode == 'rgbr':
                    cycle.putpixel((col, row), (b, r, g))
                else if mode == 'rbrg':
                    cycle.putpixel((col, row), (g, b , r))
        return cycle
        
if __name__ == "__main__":
    img = Image.open("room2.jpg")
    img_flipped = mirror_v(img)
    img_flipped.show()