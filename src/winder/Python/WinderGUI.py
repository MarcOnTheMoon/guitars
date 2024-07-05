"""
GUI of the control app for a hexaphonic pickup winder.

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

    # =========================================================================
    # ========== Constructor ==================================================
    # =========================================================================

    def __init__(self, parentApp):
        """
        Constructor.
        
        Parameters
        ----------
        parentApp : WinderApp
            Application object to use to process user input.

        Returns
        -------
        None.

        """
        # Set parent application object
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

        # Layout and start GUI loop
        leftFrame.pack(side='left', anchor='n', padx=5, pady=5)
        rightFrame.pack(side='left', padx=5, pady=5)
        root.mainloop()
        
    # -------------------------------------------------------------------------
    
    def __addCounterFrame(self, parent, padding):
        """
        Add a frame containing the counter display and reset.

        Parameters
        ----------
        parent : tkinter.Frame
            GUI object to place created frame in.
        padding : int
            Space (padding) inside the frame boarder.

        Returns
        -------
        None.

        """
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
        """
        Add a frame containing a stepper motor section to enable/disable the motor.

        Parameters
        ----------
        parent : tkinter.Frame
            GUI object to place created frame in.
        padding : int
            Space (padding) inside the frame boarder.

        Returns
        -------
        None.

        """
        frame = tk.LabelFrame(parent, text='Stepper motor', padx=padding, pady=padding)
        self.__enableCheckbox = tk.Checkbutton(frame, text='Enable', variable=self.__enableValue, command=self.__onEnableStepper)
        self.__enableCheckbox.pack(anchor='w')
        frame.pack(side='top', anchor='w', fill='x')
        
    # -------------------------------------------------------------------------
    
    def __addInfoFrame(self, parent, padding):
        """
        Add a frame containing a hyperlink to the project's GitHub repository.

        Parameters
        ----------
        parent : tkinter.Frame
            GUI object to place created frame in.
        padding : int
            Space (padding) inside the frame boarder.

        Returns
        -------
        None.

        """
        frame = tk.LabelFrame(parent, text='Info', padx=padding, pady=padding)
        linkLabel = tk.Label(frame, text='Project on GitHub', anchor='w', font=('Artial 9'), fg="blue", cursor="hand2")
        linkLabel.bind("<Button-1>", lambda e: self.__onLink("https://github.com/MarcOnTheMoon/hexaphonic_guitar"))
        linkLabel.pack(side='top', anchor='w')
        frame.pack(side='top', anchor='w', fill='x')
        
    # -------------------------------------------------------------------------
    
    def __addImage(self, parent, dy=16):
        """
        Add the HAW Hamburg logo as image.

        Parameters
        ----------
        parent : tkinter.Frame
            GUI object to place created frame in.
        padding : int
            Space (padding) inside the frame boarder.

        Returns
        -------
        None.

        """
        # Image does not show if not stored as attribute using 'self.'
        self.image = ImageTk.PhotoImage(Image.open("images/HAW-160x50.png"))
        canvas = tk.Canvas(parent, width=self.image.width(), height=self.image.height() + dy)
        canvas.create_image(0, dy, anchor='nw', image=self.image)
        canvas.pack(side='top', anchor='w')
        
    # -------------------------------------------------------------------------
    
    def __createRightFrame(self, parent, padding):
        """
        Create a frame containing a slider to set the stepper motor speed.

        Parameters
        ----------
        parent : tkinter.Frame
            GUI object to place created frame in.
        padding : int
            Space (padding) inside the frame boarder.

        Returns
        -------
        None.

        """
        frame = tk.LabelFrame(parent, text='Speed [rps]', padx=padding, pady=padding)
        speedScale = tk.Scale(frame, width=100, length=400, from_=50, to=0, resolution=1, tickinterval=10, activebackground='red', command=self.__onSpeed)
        speedScale.pack()
        return frame
    
    # =========================================================================
    # ========== Callback methods =============================================
    # =========================================================================

    def __onResetCounter(self):
        """ Button callback method to reset the counter to 0.

        Returns
        -------
        None.

        """        
        self.__counter = 0
        self.__counterLabel.config(text = str(self.__counter))
        if self.parentApp != None:
            self.parentApp.resetRevCounter()
        else:
            print('Counter reset (no app connected)')
        

    # -------------------------------------------------------------------------
    
    def __onEnableStepper(self):
        """ Checkbox callback method to enable/disable the stepper motor.

        Returns
        -------
        None.

        """        
        if self.parentApp != None:
            self.parentApp.enableMotor(isEnabled=self.__enableValue.get())
        else:
            print('Enable stepper: {} (no app connected)'.format(self.__enableValue.get()))

    # -------------------------------------------------------------------------
    
    def __onSpeed(self, value):
        """ Slider (scale) callback method to set the stepper motor's speed.

        Parameters
        ----------
        value : int
            New slider value (i.e., the target speed in revolutions per second).

        Returns
        -------
        None.

        """        
        if self.parentApp != None:
            self.parentApp.setSpeed(revsPerSec=int(value))
        else:
            print('Set speed: {} (no app connected)'.format(value))

    # -------------------------------------------------------------------------
    
    def __onLink(self, url):
        """ Hyperlink callback method to the GitHub page in a webbrowser.

        Parameters
        ----------
        url : string
            Internet URL to open in the browser.

        Returns
        -------
        None.

        """        
        webbrowser.open_new(url)
    
# -----------------------------------------------------------------------------
# Main (sample)
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    WinderGUI(parentApp=None)
