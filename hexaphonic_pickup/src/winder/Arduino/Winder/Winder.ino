/*****************************************************************************************************
 * Hexaphonic pickup winder machine
 *****************************************************************************************************
 * Author: Marc Hensel, http://www.haw-hamburg.de/marc-hensel
 * Project: https://github.com/MarcOnTheMoon/guitars
 * Copyright: 2024, Marc Hensel
 * Version: 2024.09.13
 * License: CC BY-NC-SA 4.0, see https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en
 *****************************************************************************************************
 * Board:
 * - Arduino Uno R3
 * 
 * Modules:
 * - None
 *****************************************************************************************************/

#include "SerialCom.h"
#include "StepperMotor.h"

/*****************************************************************************************************
 * Constants
 *****************************************************************************************************/

// Stepper motor
#define STEPPER_ENA_PIN 2
#define STEPPER_DIR_PIN 3
#define STEPPER_PUL_PIN 4
#define STEPS_PER_REVOLUTION 200  // 360° / (1.8° per step) = 200 steps

// Commands in communication with Python script
#define ENABLE_STEPPER        'E'   // Set "Enable" of motor driver to hight
#define DISABLE_STEPPER       'e'   // Set "Enable" of motor driver to low
#define DIR_CLOCKWISE         'D'   // Set "Direction" of motor driver to clockwise
#define DIR_COUNTER_CLOCKWISE 'd'   // Set "Direction" of motor driver to counter-clockwise
#define SET_SPEED_RPS         'S'   // Set motor speed (rotations per second send as next unsigned char)
#define GET_REV_COUNT         'C'   // Get count of full revolutions the motor has moved
#define RESET_REV_COUNT       'R'   // Reset counter of full revolutions the motor has moved
#define SEND_OK               '>'   // Request acqknowledge

/*****************************************************************************************************
 * Global variables
 *****************************************************************************************************/

// Serial communication (e.g., with Python script on connected Laptop)
SerialCom serialCom(Serial);

// Stepper motor (set to "not enabled" in driver's constructor)
StepperMotor motor(STEPPER_ENA_PIN, STEPPER_DIR_PIN, STEPPER_PUL_PIN, STEPS_PER_REVOLUTION);
unsigned long stepCount = 0;

/*****************************************************************************************************
 * Standard methods
 *****************************************************************************************************/

/**! Initialize program.
 * 
 * - The stepper motor is initialized with status "not enabled" as global variable.
 * - Serial communication using Arduino's "Serial" object is done using the global variable "serialCom".
 */
void setup() {
  // USB connection to Python script
  Serial.begin(38400);       // Make sure baud rate matches Python script
}

/* --------------------------------------------------------------------------------------------------*/

/**! Main loop. */
void loop() {
  // Receive and process commands
  while (serialCom.hasNext()) {
    processCommand(serialCom.getNext());
  }

  // Move stepper motor
  if (motor.getEnabled())
    stepCount += motor.moveSteps(10);
}

/*****************************************************************************************************
 * Receive and process commands
 *****************************************************************************************************/

/**! Process commands received via "serialCom".
 * 
 * @param command [in] Command (see Commands.h for mapping)
 */
void processCommand(char command) {
  switch (command) {
    // Get or restet count of full revolutions the motor has done
    case GET_REV_COUNT:
      Serial.println((unsigned long)(stepCount / STEPS_PER_REVOLUTION));
      break;
    case RESET_REV_COUNT:
      stepCount = 0;
      break;

    // Set enabled pin of stepper driver
    case ENABLE_STEPPER:
      motor.setEnabled(true);
      break;
    case DISABLE_STEPPER:
      motor.setEnabled(false);
      break;

    // Set stepper turning direction
    case DIR_CLOCKWISE:
      motor.setDirection(MotorDirection::CLOCKWISE);
      break;
    case DIR_COUNTER_CLOCKWISE:
      motor.setDirection(MotorDirection::COUNTER_CLOCKWISE);
      break;
      
    // Set stepper motor speed
    case SET_SPEED_RPS:
      motor.setTargetSpeed(serialReceiveNextValue());
      break;

    // Send acqknowledge
    case SEND_OK:
      Serial.println("ok");
      break;
  }
}

/* --------------------------------------------------------------------------------------------------*/

/**! Wait for and get next value sent over serial communication.
 * 
 * @return Next received value
 */
int serialReceiveNextValue(void) {
  // Wait for next sent byte
  while (serialCom.hasNext() == false) {
    // NOP
  }

  return (int)serialCom.getNext();
}
