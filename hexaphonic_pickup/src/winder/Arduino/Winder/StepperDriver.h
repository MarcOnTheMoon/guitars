/*****************************************************************************************************
 * Control stepper motor driver (such as TB6600)
 *****************************************************************************************************
 * Author: Marc Hensel, http://www.haw-hamburg.de/marc-hensel
 * Project: https://github.com/MarcOnTheMoon/guitars
 * Copyright: 2024, Marc Hensel
 * Version: 2024.09.13
 * License: CC BY-NC-SA 4.0, see https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en
 *****************************************************************************************************/

#pragma once

/*****************************************************************************************************
 * Data types
 *****************************************************************************************************/

enum MotorDirection {CLOCKWISE, COUNTER_CLOCKWISE};

/*****************************************************************************************************
 * Class
 *****************************************************************************************************/

class StepperDriver
{
  /* Attributes */
  private:
    const int ENABLE_PIN;
    const int DIR_PIN;
    const int PULSE_PIN;
   
  /* Methods */
  public:
	  StepperDriver(int enablePin, int dirPin, int pulsePin);
    void setEnabled(bool isEnabled);
    void setDirection(MotorDirection dir);
    void moveStep(int durationMicros = 500);
};
