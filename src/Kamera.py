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
        self.effects_loader.set_effect('StaticDec')
        # self.effects_loader.set_effect('DynamicDec')
        # self.effects_loader.set_effect('Other')
        # self.effects_loader.set_effect('Background')
        self.effects_loader.set_option('any_option', 'any_value')
    
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
        self.labels['Background'] = Tk.Label(self.window, text='Background', font=("Impact","16")).grid(row=1,padx=5)
        self.buttons['import'] = Tk.Button(self.window, command=self.event_import, text='Import')
        self.buttons['import'].grid(row=2, sticky=N+E+W+S,padx=5)
        self.createToolTip(self.buttons['import'],'Import background from an image file')
        self.buttons['reference'] = Tk.Button(self.window, command=self.event_reference, text='Reference')
        self.buttons['reference'].grid(row=3, sticky=N+E+W+S,padx=5)
        self.createToolTip(self.buttons['reference'],'Step outside of the frame and take a picture of the background')
        self.buttons['disable'] = Tk.Button(self.window, command=self.event_disable, text='Disable')
        self.buttons['disable'].grid(row=4, sticky=N+E+W+S,padx=5)
        self.createToolTip(self.buttons['disable'],'Restore the real background')

        # Effects Menu items
        self.labels['Effects'] = Tk.Label(self.window, text='Effects', font=("Impact","16")).grid(row=1,column=2,padx=5)
        self.labels['color'] = Tk.Label(self.window, text='Change Color:').grid(row=2, column=1, sticky=E)
        self.labels['mirror'] = Tk.Label(self.window, text='Mirror:').grid(row=3, column=1, sticky=E)
        self.options['effects1'] = Tk.OptionMenu(self.window, self.str_var_a, 'Original', 'Black/White', 'Red Only', 'Green Only', 'Blue Only', 'R<->B', 'R<->G', 'B<->G', 'R->G->B->R', 'R->B->G->R')
        self.options['effects1'].grid(row=2,column=2, sticky=N+E+W+S,padx=5)
        self.createToolTip(self.options['effects1'],'Remove, Swap, or Cycle colors')
        self.options['effects2'] = Tk.OptionMenu(self.window, self.str_var_b, 'No Mirror', 'Vertical', 'Horizontal')
        self.options['effects2'].grid(row=3,column=2, sticky=N+E+W+S,padx=5)
        self.createToolTip(self.options['effects2'],'Reflect through the middle')

        # Decoration Menu items
        self.labels['decoration'] = Tk.Label(self.window, text='Decoration', font=("Impact","16")).grid(row=5,column=0,padx=5)
        self.options['decoration'] = Tk.OptionMenu(self.window, self.str_var_g, 'None', 'Elephant', 'Giraffe', 'Goat', 'Balloons', 'Kiss', 'Plumber', 'Mushroom', 'Star', 'Shining Star', 'Heart')
        self.options['decoration'].grid(row=6,column=0, sticky=N+E+W+S,padx=5)
        self.createToolTip(self.options['decoration'],'Choose from a variety of items to add')

        # Face Detection Menu items
        self.labels['facedetect'] = Tk.Label(self.window, text='Face Detection', font=("Impact","16")).grid(row=4,column=2,columnspan=2,padx=5)
        self.labels['hair'] = Tk.Label(self.window, text='Hair:').grid(row=5,column=1, sticky=E)
        self.labels['eyes'] = Tk.Label(self.window, text='Eyes:').grid(row=6,column=1, sticky=E)
        self.labels['nose'] = Tk.Label(self.window, text='Nose:').grid(row=7,column=1, sticky=E)
        self.labels['mouth'] = Tk.Label(self.window, text='Mouth:').grid(row=8,column=1, sticky=E)
        self.options['face1'] = Tk.OptionMenu(self.window, self.str_var_c, 'None')
        self.options['face1'].grid(row=5,column=2, sticky=N+E+W+S,padx=5)
        self.createToolTip(self.options['face1'],'Wear hats and wigs')
        self.options['face2'] = Tk.OptionMenu(self.window, self.str_var_d, 'None')
        self.options['face2'].grid(row=6,column=2, sticky=N+E+W+S,padx=5)
        self.createToolTip(self.options['face2'],'Wear glasses')
        self.options['face3'] = Tk.OptionMenu(self.window, self.str_var_e, 'None')
        self.options['face3'].grid(row=7,column=2, sticky=N+E+W+S,padx=5)
        self.createToolTip(self.options['face3'],'Add a mustache')
        self.options['face4'] = Tk.OptionMenu(self.window, self.str_var_f, 'None')
        self.options['face4'].grid(row=8,column=2, sticky=N+E+W+S,padx=5)
        self.createToolTip(self.options['face4'],'Add a beard')
        self.buttons['apply'] = Tk.Button(self.window, command=self.event_save, text='Apply')
        self.buttons['apply'].grid(row=10,column=2,sticky=N+E+W+S,padx=5,pady=10)
        self.createToolTip(self.buttons['apply'],'Apply the selected effects')

        # Screenshot Button
        self.buttons['screenshot'] = Tk.Button(self.window, command=self.event_screenshot, text='Screenshot')
        self.buttons['screenshot'].grid(row=10, sticky=N+E+W+S, pady=10)
        self.createToolTip(self.buttons['screenshot'],'Save a screenshot')
    
    #import an image and store it as the virtual background
    def event_import(self):
        filename = tkFileDialog.askopenfilename(title='Import Background Image',filetypes=[('Images', ('.jpg','.gif','.png')),('all files', '.*')])
        if filename != "":
            self.imp = Image.open(filename)
        
    #take a snapshot of the current background for effect Background
    def event_reference(self):
        self.bg = self.video.getBackground()

    def event_disable(self):
        print 'restore real background'

    def event_screenshot(self):
        filename = tkFileDialog.asksaveasfilename(title='Save Screenshot Image')
	self.video.getImage().save(filename,"JPEG")
	
    
    def event_save(self):
        pass
        # print str_var_a.get(), str_var_b.get()
    #     print str_var_c.get(), str_var_d.get(), str_var_e.get(), str_var_f.get()
    
    def event_clicked(self, event):
        if self.str_var_g.get() != "None":
            print 'paste ', self.str_var_g.get(), ' at ', event.x, event.y

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
            if current_effect_class().get_name() == "DynamicDecoration":
                pil_frame = current_effect_class().process_image(frame_raw, self.effects_loader.get_options())
            else:
                 pil_frame = current_effect_class().process_image(pil_frame, self.effects_loader.get_options())
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
