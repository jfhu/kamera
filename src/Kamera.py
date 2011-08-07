import cv
import Image
import ImageTk
import numpy
import Tkinter as Tk
import inspect
import sys

CAMERAINDEX = 1

class Kamera:
    """
    opens up a window; displays video and buttons
    """
    
    window = None
    
    options = {}
    labels = {}
    buttons = {}
    video = None
    
    effects_loader = None
    
    # TODO: remove this
    def _test_use_black_white_effect(self):
        self.effects_loader.set_effect('BlackWhiteEffect')
        self.effects_loader.set_option('any_option', 'any_value')
    
    def __init__(self):
        self.effects_loader = EffectsLoader()
        self.effects_loader.load_effects()
        self.window = Tk.Tk()
        self.init_gui()
        # TODO: remove this
        self._test_use_black_white_effect()
    
    def run(self):
        self.window.mainloop()
    
    def exit(self, *args):
        sys.exit(0)
    
    def init_gui(self):
        # bind esc for quitting
        self.window.bind('<Escape>', self.exit)
        self.video = VideoLabel(self.window)
        self.video.grid(row=0, columnspan=3)
        
        str_var_a = Tk.StringVar()
        str_var_a.set('aa')
        str_var_b = Tk.StringVar()
        str_var_b.set('bb')
        self.options['option1'] = Tk.OptionMenu(self.window, str_var_a, 'A', 'B', 'C')
        self.options['option2'] = Tk.OptionMenu(self.window, str_var_b, 'A', 'B', 'C')
        
        label_texts = {
            'eyes':'Eyes', 
            'nose':'Nose',
        }
        for (k, v) in label_texts.items():
            self.labels[k] = Tk.Label(self.window, text=v)
        
        self.buttons['screenshot'] = Tk.Button(self.window, command=self.event_screenshot, text='Screenshot')
        self.buttons['record'] = Tk.Button(self.window, command=self.event_record, text='Record')
        self.buttons['effects'] = Tk.Button(self.window, command=self.event_effects, text='Add Effects')
        self.buttons['save'] = Tk.Button(self.window, command=self.event_save, text='Save')
        self.buttons['cancel'] = Tk.Button(self.window, command=self.event_cancel, text='Cancel')
        self._show_init_buttons()
    
    def _show_init_buttons(self, show = True):
        if show is True:
            self.buttons['screenshot'].grid(row = 2)
            self.buttons['record'].grid(row = 2, column = 1)
            self.buttons['effects'].grid(row = 2, column = 2)
        else:
            self.buttons['screenshot'].grid_remove()
            self.buttons['record'].grid_remove()
            self.buttons['effects'].grid_remove()
    
    def _show_all_labels_and_options(self, show = True):
        if show is True:
            for idx, l in enumerate(self.labels.values()):
                l.grid(row=idx+1)
            for idx, opt in enumerate(self.options.values()):
                opt.grid(row=idx+1, column=1)
        else:
            for k,v in self.labels.items():
                v.grid_remove()
            for k,v in self.options.items():
                v.grid_remove()
    
    def _show_save_and_cancel_buttons(self, show = True):
        if show is True:
            self.buttons['save'].grid(row=1, column=2)
            self.buttons['cancel'].grid(row=2, column=2)
        else:
            self.buttons['save'].grid_remove()
            self.buttons['cancel'].grid_remove()
    
    def event_screenshot(self):
        print 'screenshot saved'
    
    def event_record(self):
        print 'recording started'
    
    def event_effects(self):
        self._show_init_buttons(False)
        self._show_all_labels_and_options(True)
        self._show_save_and_cancel_buttons(True)        
    
    def event_save(self):
        print 'saved'
        self.event_cancel()
    
    def event_cancel(self):
        self._show_all_labels_and_options(False)
        self._show_save_and_cancel_buttons(False)
        self._show_init_buttons(True)

class EffectsLoader(object):
    """ singleton """
    _instance = None
    
    # TODO: make this list of effects
    effects_list = {}
    current_effect = None
    options = {}
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EffectsLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def load_effects(cls):
        import effects
        for name, obj in inspect.getmembers(effects):
            if inspect.isclass(obj) and name != 'KameraEffectBase':
                cls._instance.effects_list[name] = obj
        print 'Loaded effects:', ",".join(cls._instance.effects_list)
    
    def get_current_effect(cls):
        return cls._instance.current_effect
    
    def get_effects_list(cls):
        return cls._instance.effects_list
    
    def set_effect(cls, effect_name):
        cls._instance.current_effect = cls._instance.effects_list[effect_name]
        cls._instance.clear_options()

    def set_option(cls, key, value):
        cls._instance.options[key] = value
    
    def get_option(cls, key):
        return cls._instance.options[key]
    
    def get_options(cls):
        return cls._instance.options
    
    def clear_option(cls, key):
        cls._instance.options[key] = None
        
    def clear_options(cls):
        cls._instance.options = {}


class VideoLabel(Tk.Label):
    capture = None
    photo_image = None
    effects_loader = None
    
    def __init__(self, *args, **kwarg):
        self.effects_loader = EffectsLoader()
        Tk.Label.__init__(self, *args, **kwarg)
        global CAMERAINDEX
        self.capture = cv.CaptureFromCAM(CAMERAINDEX)
        self.update()
    
    def getImage(self):
        frame_raw = cv.QueryFrame(self.capture)
        frame = cv.CreateImage(cv.GetSize(frame_raw), 8, 3)
        cv.CvtColor(frame_raw, frame, cv.CV_BGR2RGB)
        pil_frame = Image.fromstring("RGB", cv.GetSize(frame), frame.tostring())
        data = numpy.asarray(pil_frame)
        data = numpy.fliplr(data)
        pil_frame = Image.fromarray(data)
        # Apply effects here?
        current_effect_class = self.effects_loader.get_current_effect()
        if current_effect_class is not None:
            pil_frame = current_effect_class().process_image(pil_frame, self.effects_loader.get_options())
        self.photo_image = ImageTk.PhotoImage(pil_frame)
        
    def update(self):
        self.getImage()
        self.config(image = self.photo_image)
        self.grid()
        self.after(5, self.update)


if __name__ == "__main__":
    kamera = Kamera()
    kamera.run()
