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
    tipwindow = None

# Creates a tooptip box for a widget.
def createToolTip( widget, text ):
    def enter( event ):
        global tipwindow
        x = y = 0
        if tipwindow or not text:
            return
        x, y, cx, cy = widget.bbox( "insert" )
        x += widget.winfo_rootx() + 27
        y += widget.winfo_rooty() + 27
        # Creates a toplevel window
        tipwindow = tw = Toplevel( widget )
        # Leaves only the label and removes the app window
        tw.wm_overrideredirect( 1 )
        tw.wm_geometry( "+%d+%d" % ( x, y ) )
        label = Label( tw, text = text, justify = LEFT,
                       background = "#ffffe0", relief = SOLID, borderwidth = 1,
                       font = ( "tahoma", "8", "normal" ) )
        label.grid( ipadx = 1 )
        
    def close( event ):
        global tipwindow
        tw = tipwindow
        tipwindow = None
        if tw:
            tw.destroy()
            
    widget.bind( "<Enter>", enter )
    widget.bind( "<Leave>", close )

    # TODO: remove this
    ##def _test_use_black_white_effect(self):
        ##self.effects_loader.set_effect('BlackWhiteEffect')
        ##self.effects_loader.set_option('any_option', 'any_value')
    
    def __init__(self):
        self.effects_loader = EffectsLoader()
        self.effects_loader.load_effects()
        self.window = Tk.Tk()
        self.init_gui()
        # TODO: remove this
        ##self._test_use_black_white_effect()
    
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
        str_var_a.set('Original')
        str_var_b = Tk.StringVar()
        str_var_b.set('No Mirror')
        str_var_c = Tk.StringVar()
        str_var_c.set('None')
        str_var_d = Tk.StringVar()
        str_var_d.set('None')
        str_var_e = Tk.StringVar()
        str_var_e.set('None')
        str_var_f = Tk.StringVar()
        str_var_f.set('None')

        self.labels['Background'] = Tk.Label(self.window, text='Background', font=("16")).grid(row=1,padx=5)
        self.buttons['import'] = Tk.Button(self.window, command=self.event_import, text='Import')
        self.buttons['import']grid(row=2, sticky=N+E+W+S)
        createToolTip(self.buttons['import'],'Import background from an image file')
        self.buttons['reference'] = Tk.Button(self.window, command=self.event_reference, text='Reference')
        self.buttons['reference'].grid(row=3, sticky=N+E+W+S)
        createToolTip(self.buttons['reference'],'Step outside of the frame and take a picture of the background')
        self.buttons['disable'] = Tk.Button(self.window, command=self.event_disable, text='Disable')
        self.buttons['disable'](row=4, sticky=N+E+W+S)
        createToolTip(self.buttons['disable'],'Restore the real background')

        self.labels['Effects'] = Tk.Label(self.window, text='Effects', font=("16")).grid(row=1,column=1,columnspan=2,padx=5)
        self.labels['color'] = Tk.Label(self.window, text='Change Color:').grid(row=2, column=1, sticky=E)
        self.labels['mirror'] = Tk.Label(self.window, text='Mirror:').grid(row=3, column=1, sticky=E)
        self.options['effects1'] = Tk.OptionMenu(self.window, str_var_a, 'Original', 'Black/White', 'Red Only', 'Green Only', 'Blue Only', 'R<->B', 'R<->G', 'B<->G', 'R->G->B->R', 'R->B->G->R')
        self.options['effects1'].grid(row=2,column=2, sticky=N+E+W+S)
        createToolTip(self.options['effects1'],'Remove, Swap, or Cycle colors')
        self.options['effects2'] = Tk.OptionMenu(self.window, str_var_b, 'No Mirror', 'Vertical', 'Horizontal')
        self.options['effects2'].grid(row=3,column=2, sticky=N+E+W+S)
        createToolTip(self.options['effects2'],'Reflect through the middle')
        self.buttons['apply1'] = Tk.Button(self.window, command=self.event_save, text='Apply')
        self.buttons['apply1'].grid(row=4,column=2,sticky=N+E+W+S)
        createToolTip(self.buttons['apply1'],'Apply the selected effects')

        self.labels['decoration'] = Tk.Label(self.window, text='Decoration', font=("16")).grid(row=1,column=3,padx=5)
        self.buttons['heart'] = Tk.Button(self.window, command=self.event_heart, text='Heart')
        self.buttons['heart'].grid(row=2,column=3,sticky=N+E+W+S)
        createToolTip(self.buttons['heart'],'Left click to add hearts, Right click to stop')
        self.buttons['star'] = Tk.Button(self.window, command=self.event_star, text='Star')
        self.buttons['star'].grid(row=3,column=3,sticky=N+E+W+S)
        createToolTip(self.buttons['star'],'Left click to add stars, Right click to stop')
        self.buttons['circle'] = Tk.Button(self.window, command=self.event_circle, text='Circle')
        self.buttons['circle'].grid(row=4,column=3,sticky=N+E+W+S)
        createToolTip(self.buttons['circle'],'Left click to add circles, Right click to stop')

        self.labels['facedetect'] = Tk.Label(self.window, text='Face Detection', font=("16")).grid(row=1,column=4,columnspan=2,padx=5)
        self.labels['hair'] = Tk.Label(self.window, text='Hair:').grid(row=2,column=4, sticky=E)
        self.labels['eyes'] = Tk.Label(self.window, text='Eyes:').grid(row=3,column=4, sticky=E)
        self.labels['nose'] = Tk.Label(self.window, text='Nose:').grid(row=4,column=4, sticky=E)
        self.labels['mouth'] = Tk.Label(self.window, text='Mouth:').grid(row=5,column=4, sticky=E)
        self.options['face1'] = Tk.OptionMenu(self.window, str_var_c, 'None')
        self.options['face1'].grid(row=2,column=5, sticky=N+E+W+S)
        createToolTip(self.options['face1'],'Wear hats and wigs')
        self.options['face2'] = Tk.OptionMenu(self.window, str_var_d, 'None')
        self.options['face2'].grid(row=3,column=5, sticky=N+E+W+S)
        createToolTip(self.options['face2'],'Wear glasses')
        self.options['face3'] = Tk.OptionMenu(self.window, str_var_e, 'None')
        self.options['face3'].grid(row=4,column=5, sticky=N+E+W+S)
        createToolTip(self.options['face3'],'Add a mustache')
        self.options['face4'] = Tk.OptionMenu(self.window, str_var_f, 'None')
        self.options['face4'].grid(row=5,column=5, sticky=N+E+W+S)
        createToolTip(self.options['face4'],'Add a beard')
        self.buttons['apply2'] = Tk.Button(self.window, command=self.event_save2, text='Apply')
        self.buttons['apply2'].grid(row=6,column=5,sticky=N+E+W+S)
        createToolTip(self.buttons['apply2'],'Apply the selected objects to your face')

        self.labels['Save'] = Tk.Label(self.window, text='Save', font=("16")).grid(row=1,column=7,padx=5)
        self.buttons['screenshot'] = Tk.Button(self.window, command=self.event_screenshot, text='Screenshot')
        self.buttons['screenshot'].grid(row=2, column=7, sticky=N+E+W+S)
        createToolTip(self.buttons['screenshot'],'Save a screenshot')
        self.buttons['record'] = Tk.Button(self.window, command=self.event_record, text='Record')
        self.buttons['record'].grid(row=3, column=7, sticky=N+E+W+S)
        createToolTip(self.buttons['record'],'Start a recording')
    
    def event_import(self):
        print 'import bg'

    def event_reference(self):
        print 'take reference photo'

    def event_disable(self):
        print 'restore real background'

    def event_screenshot(self):
        print 'screenshot saved'
    
    def event_record(self):
        print 'recording started'    
    
    def event_save(self):
        print str_var_a.get(), str_var_b.get()

    def event_save2(self):
        print str_var_c.get(), str_var_d.get(), str_var_e.get(), str_var_f.get()
    
    def event_heart(self):
        print 'add hearts'

    def event_star(self):
        print 'add stars'

    def event_circle(self):
        print 'add circles'

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