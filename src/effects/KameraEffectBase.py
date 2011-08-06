import abc

class KameraEffectBase(object):
    
    @abc.abstractmethod
    def get_name(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_description(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def process_image(self, image):
        raise NotImplementedError
