import cv
import Image
import ImageTk
import numpy
import Tkinter as Tk

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
    
    def __init__(self):
        self.window = Tk.Tk()
        self.init_gui()
    
    def run(self):
        self.window.mainloop()
    
    def init_gui(self):
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
        


class VideoLabel(Tk.Label):
    capture = None
    photo_image = None
    
    def __init__(self, *args, **kwarg):
        Tk.Label.__init__(self, *args, **kwarg)
        global CAMERAINDEX
        self.capture = cv.CaptureFromCAM(CAMERAINDEX)
        self.update()
    
    def getImage(self):
        frame = cv.QueryFrame(self.capture)
        pil_frame = Image.fromstring("RGB", cv.GetSize(frame), frame.tostring())
        data = numpy.asarray(pil_frame)
        data = numpy.fliplr(data)
        pil_frame = Image.fromarray(data)
        self.photo_image = ImageTk.PhotoImage(pil_frame)
        
    def update(self):
        self.getImage()
        self.config(image = self.photo_image)
        self.grid()
        self.after(5, self.update)


if __name__ == "__main__":
    kamera = Kamera()
    kamera.run()