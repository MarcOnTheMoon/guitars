/*****************************************************************************************************
 * Control stepper motor driver (such as TB6600)
 *****************************************************************************************************
 * Author: Marc Hensel, http://www.haw-hamburg.de/marc-hensel
 * Project: https://github.com/MarcOnTheMoon/hexaphonic_pickup
 * Copyright: 2024, Marc Hensel
 * Version: 2024.07.05
 * License: CC BY-NC-SA 4.0, see https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en
 *****************************************************************************************************/

#include "StepperDriver.h"
#include <Arduino.h>

/*****************************************************************************************************
 * Constructor
 *****************************************************************************************************/

/**! Initialize with direction CLOCKWISE and motor disabled.
 * 
 * @param enablePin [in] Arduino port connecting to "Enable"
 * @param dirPin [in] Arduino port connecting to "Direction"
 * @param pulsePin [in] Arduino port connecting to "Pulse"
 */
StepperDriver::StepperDriver(int enablePin, int dirPin, int pulsePin) : ENABLE_PIN(enablePin), DIR_PIN(dirPin), PULSE_PIN(pulsePin) {
  // Direction and pulse
	pinMode(DIR_PIN, OUTPUT);
	pinMode(PULSE_PIN, OUTPUT);
  setDirection(MotorDirection::CLOCKWISE);
	digitalWrite(PULSE_PIN, LOW);

  // Enable (initially disabled)
	pinMode(ENABLE_PIN, OUTPUT);
  setEnabled(false);
}

/*****************************************************************************************************
 * Setter
 *****************************************************************************************************/

/**! Set enable port.
 * 
 * Assumes that the "ENA-" pin of the driver is connected to ground, hence, the arduino sets its port
 * to LOW for "enabled" and HIGH for "disabled".
 * 
 * @param isEnabled [in] Set enable port to LOW if true, else HIGH
 */
void StepperDriver::setEnabled(bool isEnabled) {
  digitalWrite(ENABLE_PIN, (isEnabled) ? LOW : HIGH);
}

/* --------------------------------------------------------------------------------------------------*/

/**! Set direction of motor rotation.
 * 
 * Assumes that the "DIR-" pin of the driver is connected to ground, hence, the arduino sets its port
 * to HIGH for clockwise and LOW for counter-clockwise rotation.
 * 
 * @param dir [in] Set rotation to CLOCKWISE or COUNTER_CLOCKWISE
 */
void StepperDriver::setDirection(MotorDirection dir) {
	digitalWrite(DIR_PIN, (dir == MotorDirection::CLOCKWISE) ? HIGH : LOW);
}

/*****************************************************************************************************
 * Move
 *****************************************************************************************************/

/**! Move motor by one step.
 * 
 * Sets the step pulse to HIGH and LOW for roughly half the targeted duration (durationMicros).
 * 
 * @param durationMicros [in] Overall approximal period for a step [microsecs]
 */
void StepperDriver::moveStep(int durationMicros) {
  unsigned long stopTimeMicros = micros() + durationMicros;
  
  digitalWrite(PULSE_PIN, HIGH);
  delayMicroseconds(durationMicros / 2);
  
  digitalWrite(PULSE_PIN, LOW);
  delayMicroseconds(max(stopTimeMicros - micros(), 0));
}
