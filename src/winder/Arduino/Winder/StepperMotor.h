/*****************************************************************************************************
 * Control stepper motor
 *****************************************************************************************************
 * Author: Marc Hensel, http://www.haw-hamburg.de/marc-hensel
 * Project: https://github.com/MarcOnTheMoon/hexaphonic_pickup
 * Copyright: 2024, Marc Hensel
 * Version: 2024.07.05
 * License: CC BY-NC-SA 4.0, see https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en
 *****************************************************************************************************/

#pragma once

#include "StepperDriver.h"
#include <Arduino.h>

class StepperMotor
{
  /* Attributes */
  private:
    StepperDriver driver;
    bool isEnabled = false;                 // Is stepper set to "enabled"?
    const int STEPS_PER_REV;                // Number of steps to rotate by 360°
    double speedRevsPerSec = 0.0;           // Current speed in revolutions per second [rps]
    double targetSpeedRevsPerSec = 0.0;     // Target speed in revolutions per second [rps]

  /* Public methods */
  public:
    StepperMotor(int enablePin, int dirPin, int pulsePin, int stepsPerRevolution);
    bool getEnabled();
    void setEnabled(bool isEnabled);
    void setDirection(MotorDirection dir);
    void setTargetSpeed(double targetRevsPerSec);
    int moveSteps(int numberSteps = 1);

  /* Private methods */
  private:
    void adaptSpeed();
};
