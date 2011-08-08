import abc

class KameraEffectBase(object):
    
    @classmethod
    @abc.abstractmethod
    def get_name(cls):
        raise NotImplementedError
    
    @classmethod
    @abc.abstractmethod
    def get_description(cls):
        raise NotImplementedError
    
    @classmethod
    @abc.abstractmethod
    def process_image(cls, image, options):
        raise NotImplementedError
