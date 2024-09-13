/*****************************************************************************************************
 * Control stepper motor
 *****************************************************************************************************
 * Author: Marc Hensel, http://www.haw-hamburg.de/marc-hensel
 * Project: https://github.com/MarcOnTheMoon/hexaphonic_pickup
 * Copyright: 2024, Marc Hensel
 * Version: 2024.07.05
 * License: CC BY-NC-SA 4.0, see https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en
 *****************************************************************************************************/

#include "StepperMotor.h"
#include <Arduino.h>

/*****************************************************************************************************
 * Constructor
 *****************************************************************************************************/

/**! Initialize object.
 * 
 * @param enablePin [in] Arduino port connecting to motor driver's "Enable"
 * @param dirPin [in] Arduino port connecting to motor driver's "Direction"
 * @param pulsePin [in] Arduino port connecting to motor driver's "Pulse"
 */
StepperMotor::StepperMotor(int enablePin, int dirPin, int pulsePin,int stepsPerRevolution)
  : driver(enablePin, dirPin, pulsePin), STEPS_PER_REV(stepsPerRevolution) {
}

/*****************************************************************************************************
 * Getter
 *****************************************************************************************************/

/**! Get status of driver's enable port.
 * 
 * @return True if motor is enabled, else false.
 */
bool StepperMotor::getEnabled() {
  return isEnabled;
}

/*****************************************************************************************************
 * Setter
 *****************************************************************************************************/

/**! Set driver's enable port.
 * 
 * @param isEnabled [in] Set enable port to HIGH if true, else LOW
 */
void StepperMotor::setEnabled(bool isEnabled) {
  this->isEnabled = isEnabled;
  driver.setEnabled(isEnabled);
}

/* --------------------------------------------------------------------------------------------------*/

/**! Set driver's direction of motor rotation.
 * 
 * @param dir [in] Set rotation to CLOCKWISE or COUNTER_CLOCKWISE
 */
void StepperMotor::setDirection(MotorDirection dir) {
  driver.setDirection(dir);
}

/* --------------------------------------------------------------------------------------------------*/

/**! Set the target speed.
 * 
 * @param targetRevsPerSec [in] Target speed in revolutions per second [rps]
 */
void StepperMotor::setTargetSpeed(double targetRevsPerSec) {
  targetSpeedRevsPerSec = targetRevsPerSec;
}

/*****************************************************************************************************
 * Move motor(s)
 *****************************************************************************************************/

/**! Move by a specific number of steps.
 * 
 * @param numberSteps [in] Number of steps to move
 * 
 * @return Number of steps moved (being 0 if speed is 0)
 */
int StepperMotor::moveSteps(int numberSteps) {
  int stepsMoved = 0;

  // Adapt speed (accelerate toward target speed)
  adaptSpeed();

  // Move steps (if speed is not zero)
  if (speedRevsPerSec > 0.5) {
    unsigned long stepsPerSec = speedRevsPerSec * STEPS_PER_REV;
    unsigned long durationMicros =  1000000 / stepsPerSec;
  
    for (int i = 0; i < numberSteps; i++)
      driver.moveStep(durationMicros);
    stepsMoved = numberSteps;
  }

  return stepsMoved;
}

/* --------------------------------------------------------------------------------------------------*/

/**! Accelerate current speed toward target speed.
 */
void StepperMotor::adaptSpeed() {
  double deltaSpeed = targetSpeedRevsPerSec - speedRevsPerSec;
  
  if (abs(deltaSpeed) < 0.25) {
    speedRevsPerSec = targetSpeedRevsPerSec;
  } else {
    speedRevsPerSec += deltaSpeed / 5;
  }
}
