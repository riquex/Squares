from PIL import ImageDraw
from PIL import Image

from numpy import array

class Square(object):
    def __init__(self, size=0, color=(255, 255, 255), angle=0, *args, **kwds):
        super().__init__(*args, **kwds)
        
        self.size = size
        self.angle = angle
        self._blanck = Image.new('RGBA', (self.size, self.size))

    @property
    def image(self):
        self._blanck = Image.new('RGBA', (self.size, self.size))
        draw = ImageDraw(self._blanck)
        
        dots = array([(angle, angle),
                    (self.size-angle, angle),
                    (self.size-angle, self.size-angle),
                    (angle, self.size-angle)])

        dots_angle = array([(0, angle),
                            (angle, angle),
                            ()])
        return img
