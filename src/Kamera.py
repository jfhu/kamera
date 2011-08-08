import cv
import Image
import ImageTk
import numpy
import Tkinter as Tk
from Tkinter import N, E, W, S
import inspect
import sys
import tkFileDialog

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
    def createToolTip(self, widget, text ):
        def enter( event ):
            if self.tipwindow or not text:
                return
            x, y, cx, cy = widget.bbox( "insert" )
            x += widget.winfo_rootx() + 27
            y += widget.winfo_rooty() + 27
            # Creates a toplevel window
            self.tipwindow = tw = Tk.Toplevel( widget )
            # Leaves only the label and removes the app window
            tw.wm_overrideredirect( 1 )
            tw.wm_geometry( "+%d+%d" % ( x, y ) )
            label = Tk.Label( tw, text = text, justify = Tk.LEFT,
                           background = "#ffffe0", relief = Tk.SOLID, borderwidth = 1,
                           font = ( "tahoma", "8", "normal" ) )
            label.grid( ipadx = 1 )
        
        def close( event ):
            if self.tipwindow:
                self.tipwindow.destroy()
            self.tipwindow = None
            
        widget.bind( "<Enter>", enter )
        widget.bind( "<Leave>", close )


    def _test_use_black_white_effect(self):
        # self.effects_loader.set_effect('BlackWhiteEffect')
        # self.effects_loader.set_effect('Decoration')
        self.effects_loader.enable_effect('StaticDec')
        self.effects_loader.set_option('StaticDec', 'positions', [])
        # self.effects_loader.set_effect('DynamicDec')
        # self.effects_loader.set_effect('Other')
        # self.effects_loader.set_effect('Background')
    
    def __init__(self):
        self.effects_loader = EffectsLoader()
        self.effects_loader.load_effects()
        self.window = Tk.Tk()
        self.init_gui()
        self._test_use_black_white_effect()
    
    def run(self):
        self.window.mainloop()
    
    def exit(self, *args):
        sys.exit(0)
    
    def init_gui(self):
        # no resize on window
        self.window.resizable(width=False, height=False)
        
        # bind esc for quitting
        self.window.bind('<Escape>', self.exit)
        self.video = VideoLabel(self.window)
        self.video.grid(row=0, columnspan=3)

        # bind mouse click for pasting
        self.video.bind("<Button-1>", self.event_clicked)
        
        # Color effects variable
        self.str_var_a = Tk.StringVar()
        self.str_var_a.set('Original')
        # Mirror effects
        self.str_var_b = Tk.StringVar()
        self.str_var_b.set('No Mirror')
        # Face detection objects
        self.str_var_c = Tk.StringVar()
        self.str_var_c.set('None')
        self.str_var_d = Tk.StringVar()
        self.str_var_d.set('None')
        self.str_var_e = Tk.StringVar()
        self.str_var_e.set('None')
        self.str_var_f = Tk.StringVar()
        self.str_var_f.set('None')
        # Decoration objects
        self.str_var_g = Tk.StringVar()
        self.str_var_g.set('None')

        # Background Menu items
        self.labels['Background'] = Tk.Label(self.window, text='Background', font=("Impact","16")).grid(row=1)
        self.buttons['import'] = Tk.Button(self.window, command=self.event_import, text='Import')
        self.buttons['import'].grid(row=2, sticky=N+E+W+S,padx=15)
        self.createToolTip(self.buttons['import'],'Import background from an image file')
        self.buttons['reference'] = Tk.Button(self.window, command=self.event_reference, text='Reference')
        self.buttons['reference'].grid(row=3, sticky=N+E+W+S,padx=15)
        self.createToolTip(self.buttons['reference'],'Step outside of the frame and take a picture of the background')
        self.buttons['disable'] = Tk.Button(self.window, command=self.event_disable, text='Disable')
        self.buttons['disable'].grid(row=4, sticky=N+E+W+S,padx=15)
        self.createToolTip(self.buttons['disable'],'Restore the real background')

        # Effects Menu items
        self.labels['Effects'] = Tk.Label(self.window, text='Effects', font=("Impact","16")).grid(row=1,column=2)
        self.labels['color'] = Tk.Label(self.window, text='Color:').grid(row=2, column=1, sticky=E)
        self.labels['mirror'] = Tk.Label(self.window, text='Mirror:').grid(row=3, column=1, sticky=E)
        self.options['effects1'] = Tk.OptionMenu(self.window, self.str_var_a, 'Original', 'Black/White', 'Red Only', 'Green Only', 'Blue Only', 'R<->B', 'R<->G', 'B<->G', 'R->G->B->R', 'R->B->G->R')
        self.options['effects1'].grid(row=2,column=2, sticky=N+E+W+S,padx=15)
        self.createToolTip(self.options['effects1'],'Remove, Swap, or Cycle colors')
        self.options['effects2'] = Tk.OptionMenu(self.window, self.str_var_b, 'No Mirror', 'Vertical', 'Horizontal')
        self.options['effects2'].grid(row=3,column=2, sticky=N+E+W+S,padx=15)
        self.createToolTip(self.options['effects2'],'Reflect through the middle')

        # Decoration Menu items
        self.labels['decoration'] = Tk.Label(self.window, text='Decoration', font=("Impact","16")).grid(row=5,column=0)
        self.options['decoration'] = Tk.OptionMenu(self.window, self.str_var_g, 'None', 'Elephant', 'Giraffe', 'Goat', 'Balloons', 'Kiss', 'Plumber', 'Mushroom', 'Star', 'Shining Star', 'Heart')
        self.options['decoration'].grid(row=6,column=0, sticky=N+E+W+S,padx=15)
        self.createToolTip(self.options['decoration'],'Choose from a variety of items to add')
        self.buttons['remove'] = Tk.Button(self.window, command=self.event_remove, text='Remove')
        self.buttons['remove'].grid(row=7,column=0,sticky=N+E+W+S,padx=15)
        self.createToolTip(self.buttons['remove'],'Click to remove all decorations')

        # Face Detection Menu items
        self.labels['facedetect'] = Tk.Label(self.window, text='Face Detection', font=("Impact","16")).grid(row=4,column=2,columnspan=2,padx=15)
        self.labels['hair'] = Tk.Label(self.window, text='Hair:').grid(row=5,column=1, sticky=E)
        self.labels['eyes'] = Tk.Label(self.window, text='Eyes:').grid(row=6,column=1, sticky=E)
        self.labels['nose'] = Tk.Label(self.window, text='Nose:').grid(row=7,column=1, sticky=E)
        self.labels['mouth'] = Tk.Label(self.window, text='Mouth:').grid(row=8,column=1, sticky=E)
        self.options['face1'] = Tk.OptionMenu(self.window, self.str_var_c, 'None', 'Tiara', 'Crown')
        self.options['face1'].grid(row=5,column=2, sticky=N+E+W+S,padx=15)
        self.createToolTip(self.options['face1'],'Wear hats')
        self.options['face2'] = Tk.OptionMenu(self.window, self.str_var_d, 'None', 'Big Eyes', 'Glasses', 'Goggles')
        self.options['face2'].grid(row=6,column=2, sticky=N+E+W+S,padx=15)
        self.createToolTip(self.options['face2'],'Wear glasses')
        self.options['face3'] = Tk.OptionMenu(self.window, self.str_var_e, 'None', 'Mustache')
        self.options['face3'].grid(row=7,column=2, sticky=N+E+W+S,padx=15)
        self.createToolTip(self.options['face3'],'Add a mustache')
        self.options['face4'] = Tk.OptionMenu(self.window, self.str_var_f, 'None', 'Beard', 'Kiss')
        self.options['face4'].grid(row=8,column=2, sticky=N+E+W+S,padx=15)
        self.createToolTip(self.options['face4'],'Add a beard')
        self.buttons['apply'] = Tk.Button(self.window, command=self.event_save, text='Apply')
        self.buttons['apply'].grid(row=10,column=2,sticky=N+E+W+S,padx=15,pady=10)
        self.createToolTip(self.buttons['apply'],'Apply the selected effects')

        # Screenshot Button
        self.buttons['screenshot'] = Tk.Button(self.window, command=self.event_screenshot, text='Screenshot')
        self.buttons['screenshot'].grid(row=10, sticky=N+E+W+S, padx=15,pady=10)
        self.createToolTip(self.buttons['screenshot'],'Save a screenshot')
    
    #import an image and store it as the virtual background
    def event_import(self):
        filename = tkFileDialog.askopenfilename(title='Import Background Image',filetypes=[('Images', ('.jpg','.gif','.png')),('all files', '.*')])
        if filename != "":
            self.imp = Image.open(filename)
            self.effects_loader.set_option('Background', 'bgNew', self.imp)
            
        
    #take a snapshot of the current background for effect Background
    def event_reference(self):
        self.bg = self.video.getBackground()
        self.effects_loader.set_option('Background', 'bg', self.bg)

    def event_disable(self):
        self.effects_loader.set_option('Background', 'bg', None)
        self.effects_loader.set_option('Background', 'bgNew', None)
        print 'restore real background'

    def event_screenshot(self):
        filename = tkFileDialog.asksaveasfilename(title='Save Screenshot Image')
	self.video.getImage().save(filename,"JPEG")
	
    
    def event_save(self):
        pass
        # str_var_a.get() for color effects
            #'Original', 'Black/White', 'Red Only', 'Green Only', 'Blue Only', 'R<->B', 'R<->G', 'B<->G', 'R->G->B->R', 'R->B->G->R'
        # str_var_b.get() for mirror effects
            #'No Mirror', 'Vertical', 'Horizontal'
        # str_var_c.get(), str_var_d.get(), str_var_e.get(), str_var_f.get() for face items
            #'None'
            #'Tiara'    = crown.png
            #'Crown'    = bigcrown.png
            #'Big Eyes' = eye.png
            #'Glasses'  = glasses.png
            #'Goggles'  = goggle.png
            #'Mustache' = mustache.png
            #'Beard'    = beard.png
            #'Kiss'     = kiss.png

    def event_remove(self):
        pass

    def event_clicked(self, event):
        if self.str_var_g.get() != "None":
            positions = self.effects_loader.get_option('StaticDec', 'positions', default = [])
            positions.append({'name':self.str_var_g.get(), 'position':(event.x, event.y)})
            self.effects_loader.set_option('StaticDec', 'positions', positions)
                #'None'
                #'Elephant'     = elephant.png
                #'Giraffe'      = giraffe.png
                #'Goat'         = goat.png
                #'Balloons'     = heart_balloons.png
                #'Kiss'         = kiss.png
                #'Plumber'      = mario.png
                #'Mushroom'     = Mushroom.png
                #'Star'         = star.png
                #'Shining Star' = PowerStar.png
                #'Heart'        = red_heart.png

class EffectsLoader(object):
    """ singleton """
    _instance = None

    """
    what's in the effects_dict:
    key:
        'EffectClassName'
    value: a dict where:
        class : the effect class
        enabled : True | False
        option : another dict with key-value pairs
    """
    effects_dict = {}
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EffectsLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def load_effects(cls):
        import effects
        for name, obj in inspect.getmembers(effects):
            if inspect.isclass(obj) and name != 'KameraEffectBase':
                e = {}
                e['class'] = obj
                e['enabled'] = False
                e['option'] = {}
                cls._instance.effects_dict[name] = e
        print 'Loaded effects:', ", ".join(cls._instance.effects_dict.keys())
    
    def get_enabled_effects(cls):
        return [i for i in cls._instance.effects_dict.values() if i['enabled'] is True]

    def enable_effect(cls, name, should_enable = True):
        cls._instance.effects_dict[name]['enabled'] = should_enable
    
    def disable_effect(cls, name):
        cls.enable_effect(name, False)
    
    def set_option(cls, name, key, value):
        cls._instance.effects_dict[name]['option'][key] = value
    
    # default: return this if key not found in option
    def get_option(cls, name, key, default = None):
        if key in cls._instance.effects_dict[name]['option']:
            return cls._instance.effects_dict[name]['option'][key]
        else:
            return default
            
    
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
        effects = self.effects_loader.get_enabled_effects()
        if effects:
            for effect in effects:
                e = effect['class']()
                if e.get_name() == "DynamicDecoration":
                    pil_frame = e.process_image(frame_raw, effect['option'])
                else:
                    pil_frame = e.process_image(pil_frame, effect['option'])
        self.photo_image = ImageTk.PhotoImage(pil_frame)
        return pil_frame
        
    def getBackground(self):
        frame_raw = cv.QueryFrame(self.capture)
        frame = cv.CreateImage(cv.GetSize(frame_raw), 8, 3)
        cv.CvtColor(frame_raw, frame, cv.CV_BGR2RGB)
        pil_frame = Image.fromstring("RGB", cv.GetSize(frame), frame.tostring())
        data = numpy.asarray(pil_frame)
        data = numpy.fliplr(data)
        pil_frame = Image.fromarray(data)
        return pil_frame
        
    def update(self):
        self.getImage()
        self.config(image = self.photo_image)
        self.grid()
        self.after(5, self.update)


if __name__ == "__main__":
    kamera = Kamera()
    kamera.run()
