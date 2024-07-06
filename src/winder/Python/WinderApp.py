"""
Control app for a hexaphonic pickup winder.

@author: Marc Hensel
@contact: http://www.haw-hamburg.de/marc-hensel
@copyright: 2024
@version: 2024.07.06
@license: CC BY-NC-SA 4.0, see https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en
"""
import time
import threading
from ArduinoCOM import ArduinoCOM
from WinderGUI import WinderGUI

class WinderApp():

    # =========================================================================
    # ========== Class constants ==============================================
    # =========================================================================

    # Command chars expected by the Arduino
    _commands = {
        'enableMotor':          'E',
        'disableMotor':         'D',
        'setSpeedRevsPerSec':   'S',
        'getRevCount':          'C',
        'resetRevCounter':      'R',
        'sendOk':               '>'
    }

    # =========================================================================
    # ========== Constructor ==================================================
    # =========================================================================

    def __init__(self, serialCOM=None):
        """
        Constructor.
        
        The contructor tries to connect to an Arduino using serial COM ports.
        If connection succeeds, it generates and runs the GUI.
        
        Parameters
        ----------
        serialCOM : int, optional
            Serial port Arduino is connected to (e.g., '3' for 'COM3').
            Tries to connect to ports 0 to 15, if argument is None. (Default: None)

        Returns
        -------
        None.

        """
        # Connect to Arduino (will reset Arduino => Runs setup())
        self.__threadLock = threading.Lock()
        self.__arduino = ArduinoCOM(serialCOM=serialCOM, baudRate=38_400)

        # Create and start GUI
        self.__gui = WinderGUI(parentApp=self)

    # =========================================================================
    # ========== Serial connection ============================================
    # =========================================================================

    def close(self, waitTimeSec=2.0):
        """
        Requests Arduino to stop and disable stepper motor and closes serial connection.

        Parameters
        ----------
        waitTimeSec : float
            Delay before stopping and disabling stepper [s] (Default: 2.0)

        Returns
        -------
        None.

        """
        time.sleep(waitTimeSec)
        print('\nClosing connection:')
        self.setSpeed(revsPerSec=0)
        self.enableMotor(False)
        time.sleep(1.0)             # Wait for Arduino to read buffer
        self.__arduino.close()

    # -------------------------------------------------------------------------

    def __sendWithReply(self, command, isRequestAck=True):
        """
        Send command to Arduino requesting and waiting for reply.

        Parameters
        ----------
        command : string
            Command string to send (typically chars from dictionary _command).

        Returns
        -------
        string
            Reply send by the Arduino (typically 'ok' when requesting ACK).

        """
        # Send command (and request for acknowledgement)
        if isRequestAck == True:
            self.__arduino.writeString(command + self._commands['sendOk'])
        else:
            self.__arduino.writeString(command)
            
        # Receive and return reply
        return self.__arduino.readLine()

    # =========================================================================
    # ========== Motor control ================================================
    # =========================================================================

    def enableMotor(self, isEnabled):
        """
        Enable or disable stepper motor.
        
        If the motor is enabled, current is flowing through it and it actively
        holds its position. When disabled, one can easily move the motor by
        hand.

        Parameters
        ----------
        isEnabled : boolean
            Enable stepper if True, else disable stepper.

        Returns
        -------
        None.

        """
        self.__threadLock.acquire()

        # Determine command
        if isEnabled:
            print('Enable motor', end=' ')
            command = self._commands['enableMotor']
        else:
            print('Disable motor', end=' ')
            command = self._commands['disableMotor']

        # Send command and print reply
        reply = self.__sendWithReply(command)
        print('... ' + reply)            
        self.__threadLock.release()

    # -------------------------------------------------------------------------
    
    def setSpeed(self, revsPerSec):
        """ Set stepper motor speed.
        
        Parameters
        ----------
        revsPerSec : int
            Motor speed [revolutions/sec].

        Returns
        -------
        None.

        """
        self.__threadLock.acquire()

        # Command + value
        print('Set speed [rps]: {}'.format(revsPerSec), end=' ')
        command = self._commands['setSpeedRevsPerSec']
        command += chr(revsPerSec)

        # Send command and print reply
        reply = self.__sendWithReply(command)
        print('... ' + reply)
        self.__threadLock.release()

    # =========================================================================
    # ========== Revolution counter ===========================================
    # =========================================================================

    def getRevCount(self):
        """ Get count of motor full revolutions from Arduino.
        
        Warning: Querying the rev count leads to a small pause in turning the
        stepper motor at the Arduino side. To run the stepper smoothly, do not
        use the query.

        Returns
        -------
        int
            Full revolutions since start or last counter reset.

        """
        self.__threadLock.acquire()

        # Determine and send command
        command = self._commands['getRevCount']
        reply = self.__sendWithReply(command, isRequestAck=False)
        
        # Return counter as value
        self.__threadLock.release()
        return int(reply)

    # -------------------------------------------------------------------------

    def resetRevCounter(self):
        """
        Reset the Arduino's step counter.
        
        Returns
        -------
        None.

        """
        self.__threadLock.acquire()

        # Determine command
        command = self._commands['resetRevCounter']
        print('Reset counter', end=' ')

        # Send command and print reply
        reply = self.__sendWithReply(command)
        print('... ' + reply)            
        self.__threadLock.release()
        
# -----------------------------------------------------------------------------
# Main (sample)
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    app = WinderApp()
    app.close()
