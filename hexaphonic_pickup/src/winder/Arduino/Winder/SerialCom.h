/*****************************************************************************************************
 * Communication via serial interface.
 *****************************************************************************************************
 * Author: Marc Hensel, http://www.haw-hamburg.de/marc-hensel
 * Project: https://github.com/MarcOnTheMoon/guitars
 * Copyright: 2024, Marc Hensel
 * Version: 2024.09.13
 * License: CC BY-NC-SA 4.0, see https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en
 *****************************************************************************************************/

#pragma once
#include <Arduino.h>

class SerialCom {
  /* Attributes */
  private:
    HardwareSerial& serial;
    const int bufferSize = 32;
    char readBuffer[32];
    int bufferReadIndex;
    int bufferLastIndex;

  /* Public methods */
  public:
    // Public methods
    SerialCom(HardwareSerial& serial);
    bool hasNext(void);
    char getNext(void);
    
  /* Private methods */
  private:
    void receiveData(void);

};
