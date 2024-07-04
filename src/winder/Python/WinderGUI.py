"""
GUI used by winder device of coils for hexaphonic guitar pickups.

@author: Marc Hensel
@contact: http://www.haw-hamburg.de/marc-hensel
@copyright: 2024
@version: 2024.07.04
@license: CC BY-NC-SA 4.0, see https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en
"""
import tkinter as tk
import webbrowser
from PIL import ImageTk, Image

class WinderGUI():

    # ========== Constructor ==================================================

    def __init__(self, parentApp):
        # Set parent app
        self.parentApp = parentApp
        
        # GUI root frame and variables
        root = tk.Tk()
        root.title('Pickup Winder')
        self.__counter = 0                          # Count full rotations
        self.__enableValue = tk.BooleanVar()       # State of the checkbox "Stepper motor enabled"

        # Create left (counter, stepper, and info) and right (speed control) GUI frames
        leftFrame = tk.Frame(root)
        self.__addCounterFrame(parent=leftFrame, padding=10)
        self.__addStepperMotorFrame(parent=leftFrame, padding=10)
        self.__addInfoFrame(parent=leftFrame, padding=10)
        self.__addImage(parent=leftFrame, dy=16)        
        rightFrame = self.__createRightFrame(parent=root, padding=10)

        # Layout and start GUI
        leftFrame.pack(side='left', anchor='n', padx=5, pady=5)
        rightFrame.pack(side='left', padx=5, pady=5)
        root.mainloop()
        
    # -------------------------------------------------------------------------
    
    def __addCounterFrame(self, parent, padding):
        # Create widgets
        frame = tk.LabelFrame(parent, text='Counter', padx=padding, pady=padding)
        self.__counterLabel = tk.Label(frame, text='0', width=5, height=1, background='black', foreground='white', font=('Arial', '53'))
        resetButton = tk.Button(frame, text='Reset', width=10, command=self.__onResetCounter)
        
        # Layout widgets
        self.__counterLabel.pack()
        resetButton.pack()
        frame.pack(side='top')
        
    # -------------------------------------------------------------------------
    
    def __addStepperMotorFrame(self, parent, padding):
        frame = tk.LabelFrame(parent, text='Stepper motor', padx=padding, pady=padding)
        self.__enableCheckbox = tk.Checkbutton(frame, text='Enable', variable=self.__enableValue, command=self.__onEnableStepper)
        self.__enableCheckbox.pack(anchor='w')
        frame.pack(side='top', anchor='w', fill='x')
        
    # -------------------------------------------------------------------------
    
    def __addInfoFrame(self, parent, padding):
        frame = tk.LabelFrame(parent, text='Info', padx=padding, pady=padding)
        linkLabel = tk.Label(frame, text='Project on GitHub', anchor='w', font=('Artial 9'), fg="blue", cursor="hand2")
        linkLabel.bind("<Button-1>", lambda e: self.__onLink("https://github.com/MarcOnTheMoon/hexaphonic_guitar"))
        linkLabel.pack(side='top', anchor='w')
        frame.pack(side='top', anchor='w', fill='x')
        
    # -------------------------------------------------------------------------
    
    def __addImage(self, parent, dy=16):
        # Image does not show if not stored as attribute using 'self.'
        self.image = ImageTk.PhotoImage(Image.open("images/HAW-160x50.png"))
        canvas = tk.Canvas(parent, width=self.image.width(), height=self.image.height() + dy)
        canvas.create_image(0, dy, anchor='nw', image=self.image)
        canvas.pack(side='top', anchor='w')
        
    # -------------------------------------------------------------------------
    
    def __createRightFrame(self, parent, padding):
        frame = tk.LabelFrame(parent, text='Speed [rps]', padx=padding, pady=padding)
        speedScale = tk.Scale(frame, width=100, length=400, from_=50, to=0, resolution=1, tickinterval=10, activebackground='red', command=self.__onSpeed)
        speedScale.pack()
        return frame
    
    # ========== Callback methods =============================================

    def __onResetCounter(self):
        self.__counter = 2534
        self.__counterLabel.config(text = str(self.__counter))
        print('Counter reset')

    # -------------------------------------------------------------------------
    
    def __onEnableStepper(self):
        if self.parentApp != None:
            self.parentApp.enableMotor(isEnabled=self.__enableValue.get())
        else:
            print('Enable stepper: {} (no app connected)'.format(self.__enableValue.get()))

    # -------------------------------------------------------------------------
    
    def __onSpeed(self, value):
        if self.parentApp != None:
            self.parentApp.setSpeed(revsPerSec=int(value))
        else:
            print('Set speed: {} (no app connected)'.format(value))

    # -------------------------------------------------------------------------
    
    def __onLink(self, url):
        webbrowser.open_new(url)
    
# -----------------------------------------------------------------------------
# Main (sample)
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    gui = WinderGUI(parentApp=None)
