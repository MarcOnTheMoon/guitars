/*****************************************************************************************************
 * Communication via serial interface.
 *****************************************************************************************************
 * Author: Marc Hensel, http://www.haw-hamburg.de/marc-hensel
 * Project: https://github.com/MarcOnTheMoon/guitars
 * Copyright: 2024, Marc Hensel
 * Version: 2024.09.13
 * License: CC BY-NC-SA 4.0, see https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en
 *****************************************************************************************************
 * Implementation notes:
 * - Method hasNext() is the only public method that reads data from the serial connection into the
 *   class-internal read buffer. Be aware that it will only try to receive data from the serial
 *   connection when the class-internal read buffer is empty.
 * - Method getNext() returns and removes values the class-internal read buffer. By calling hasNext()
 *   it triggers receiving new data from the serial connection when the internal read buffer is empty.
 *****************************************************************************************************/

#include "SerialCom.h"
#include <Arduino.h>

/*****************************************************************************************************
 * Public methods
 *****************************************************************************************************/

/**! Initialize object.
 * 
 * @param serial [in] Serial connection to read data from (typically the Arduino object "Serial")
 */
SerialCom::SerialCom(HardwareSerial& serial) : serial(serial) {
  bufferReadIndex = 0;
  bufferLastIndex = 0;
}

/* --------------------------------------------------------------------------------------------------*/

/**! Checks whether there is a received char available.
 * 
 * The method checks if there are still values in the read buffer. Only if the read buffer is empty,
 * it checks if new data has been sent over the serial connection.
 * 
 * @return True if a char value has been transmitted, else false
 */
bool SerialCom::hasNext(void) {
  // Empty buffer => Receive data from serial connection
  if (bufferLastIndex == 0) {
    receiveData();
  }

  return (bufferReadIndex < bufferLastIndex);
}

/* --------------------------------------------------------------------------------------------------*/

/**! Get the next received char value.
 * 
 * To prevent deadlocks, the method is not blocking, i.e., it will return a value even if there is no
 * further received char in the buffer. Call hasNext() before to check, if a received value exists.
 * 
 * The method removes and return values from the read buffer. By calling hasNext() it triggers
 * receiving new data from the serial connection, if the read buffer is empty.
 * 
 * @return The next received value or 0
 */
char SerialCom::getNext(void) {
  char value = 0;

  // Buffer not empty
  if (hasNext()) {
    // Get next value
    value = readBuffer[bufferReadIndex++];

    // Reset indices if buffer is empty
    if (bufferReadIndex == bufferLastIndex) {
      bufferReadIndex = 0;
      bufferLastIndex = 0;
    }
  }
  
  return value;
}

/*****************************************************************************************************
 * Private methods
 *****************************************************************************************************/

/**! Receive characters via the serial interface.
 */
void SerialCom::receiveData(void) {
  while ((serial.available() > 0) && (bufferLastIndex < bufferSize)) {
    readBuffer[bufferLastIndex++] = (char)serial.read();
    delay(3);
  }
}
