"""
Control for winder device of coils for hexaphonic guitar pickups.

@author: Marc Hensel
@contact: http://www.haw-hamburg.de/marc-hensel
@copyright: 2024
@version: 2024.07.04
@license: CC BY-NC-SA 4.0, see https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en
"""
import time
from ArduinoCOM import ArduinoCOM
from WinderGUI import WinderGUI

class WinderApp():

    # ========== Class constants ==============================================

    # Command chars expected by the Arduino
    _commands = {
        'enableMotor':          'E',
        'disableMotor':         'D',
        'setSpeedRevsPerSec':   'S',
        'sendOk':               '>'
    }

    # ========== Constructor ==================================================

    def __init__(self, serialCOM = None):
        # Connect to Arduino (will reset Arduino => Runs setup())
        self._arduino = ArduinoCOM(serialCOM=serialCOM)

        # Create and start GUI
        self.__gui = WinderGUI(parentApp=self)

    # ========== Serial connection ============================================

    def close(self, waitTimeSec=2.0):
        """
        Requests Arduino to disable stepper motor and closes serial connection.

        Parameters
        ----------
        waitTimeSec : float
            Delay before disabling stepper [s] (Default: 2.0)

        Returns
        -------
        None.

        """
        time.sleep(waitTimeSec)
        print('\nClosing connection:')
        self.setSpeed(revsPerSec=0)
        self.enableMotor(False)
        time.sleep(1.0)             # Wait for Arduino to read buffer
        self._arduino.close()

    # -------------------------------------------------------------------------

    def __sendWithAck(self, command):
        """
        Send command to Arduino requesting and waiting for reply.

        Parameters
        ----------
        command : string
            Command string to send (typically chars from dictionary _command).

        Returns
        -------
        string
            Reply send by the Arduino (typically 'ok').

        """
        self._arduino.writeString(command + self._commands['sendOk'])
        return self._arduino.readLine()

    # ========== Motor control ================================================

    def enableMotor(self, isEnabled):
        """
        Enable or disable stepper motor.

        Parameters
        ----------
        isEnabled : boolean
            Enable stepper if True, else disable steppers.

        Returns
        -------
        None.

        """
        # Determine command
        if isEnabled:
            print('Enable motor', end=' ')
            command = self._commands['enableMotor']
        else:
            print('Disable motor', end=' ')
            command = self._commands['disableMotor']

        # Send command and print reply
        reply = self.__sendWithAck(command)
        print('... ' + reply)            

    # -------------------------------------------------------------------------
    
    def setSpeed(self, revsPerSec):
        # Command + value
        print('Set speed [rps]: {}'.format(revsPerSec), end=' ')
        command = self._commands['setSpeedRevsPerSec']
        command += chr(revsPerSec)

        # Send command and print reply
        reply = self.__sendWithAck(command)
        print('... ' + reply)
        
# -----------------------------------------------------------------------------
# Main (sample)
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    app = WinderApp()
    app.close()
