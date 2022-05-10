/**
 ****************************************************************
 @file    pca9633.c
 ****************************************************************
 @brief   This module offers a set of functions to handle the
          4-bit PWM LED-Driver on the I2C-Interface.
 ****************************************************************
 @author  Florian Baumgartner, HSR
 @version 1.0
 @date    2020-04-08
 @note    The PCA9633 ADC use the I2C-Slave base-address 0x62.
 To operate multiple PCA9633 on the same I2C-Bus, an additional
 Hardware-Address between [0..3] must be given.
 (Default w/o modification = 0)
 @note    Functions are not reentrant and shall not be called in
 parallel from different execution contexts.
 ****************************************************************
 */
/** @addtogroup HWO
 * @{
 */

/** @addtogroup DATA
 * @{
 */
#define HWO_PCA9633_C_

//===============================================================
//includes
#include "pca9633.h"

#include <stdint.h>
#include "../../GLOB_Types.h"

//===============================================================
//defines
#define PCA933_SLAVE_ADDR    (PCA9633_BASEADDR)   //!<I2C-Slave Base-Address

//===============================================================
//typedefs

//===============================================================
//variables
static i2c_unit_t i2c_interface;

static uint8_t outputState = 0x00;

//===============================================================
//function prototypes
static error_t writeRegister (i2c_unit_t unit, uint8_t hw_address, uint8_t reg, uint8_t data);

//===============================================================
//interrupt-handler

//===============================================================
//function implementation

/**
 *****************************************************************
 @brief   Initialize LED-Driver PCA9633.
 @param   unit        Selects which I2C-Interface should be used on MC [I2C_0, I2C_2, I2C_6, I2C_8]
 @param   hw_address  Additional Hardware-Address of the PCA9633       [0..3]
 @return  Error-Code
 @note    The I2C-Bus must be initialized directly thorough calls
 to the hal_i2c.c/.h module.
 ****************************************************************
 */
error_t pca9633_init (i2c_unit_t unit, uint8_t hw_address)
{
  error_t error = NO_ERROR;
  i2c_interface = unit;

  error |= writeRegister (i2c_interface, hw_address, PCA9633_LEDOUT, 0x00);  // All Outputs are fully off
  error |= writeRegister (i2c_interface, hw_address, PCA9633_MODE1, 0x00);   // set sleep = 0, turn on oscillator, disable allcall and subaddrs
  error |= writeRegister (i2c_interface, hw_address, PCA9633_MODE2, 0x14);   // Enable Push-Pull Outputs and invert PWM

  return (error);
}

/**
 *****************************************************************
 @brief   Changes the output to a static level
 @param   hw_address  Additional Hardware-Address of the PCA9633       [0..3]
 @param   pin         Selects the pin to change the output state       [0..3]
 @param   value       Selects the output state.                        [0..1]
 @return  Error-Code
 @note    The I2C-Bus must be initialized directly thorough calls
 to the hal_i2c.c/.h module.
 ****************************************************************
 */
error_t pca9633_digitalWrite (uint8_t hw_address, uint8_t pin, uint8_t value)
{
  error_t error = NO_ERROR;

  if (value) outputState = (outputState & ~(0x03 << (pin * 2))) | (0x01 << (pin * 2));  // Output fully on
  else outputState &= ~(0x03 << (pin * 2));                                             // Output fully off

  error |= writeRegister (i2c_interface, hw_address, PCA9633_LEDOUT, outputState);

  return (error);
}

/**
 *****************************************************************
 @brief   Changes the output to a 8-bit PWM value.
 @param   hw_address  Additional Hardware-Address of the PCA9633       [0..3]
 @param   pin         Selects the pin to change the output state       [0..3]
 @param   value       Selects the PWM value.                           [0..255]
 @return  Error-Code
 @note    The I2C-Bus must be initialized directly thorough calls
 to the hal_i2c.c/.h module.
 ****************************************************************
 */
error_t pca9633_setPwmValue (uint8_t hw_address, uint8_t pin, uint8_t value)
{
  error_t error = NO_ERROR;

  outputState = (outputState & ~(0x03 << (pin * 2))) | (0x02 << (pin * 2));             // Output in PWM mode

  error |= writeRegister (i2c_interface, hw_address, PCA9633_LEDOUT, outputState);
  error |= writeRegister (i2c_interface, hw_address, PCA9633_PWM0 + pin, value);

  return (error);
}



static error_t writeRegister (i2c_unit_t unit, uint8_t hw_address, uint8_t reg, uint8_t data)
{
  uint8_t slaveAddr = PCA933_SLAVE_ADDR | (hw_address & 0x0F);
  error_t error = NO_ERROR;
  uint8_t buf [2] = {reg, data};

  error = hal_i2c_write (unit, slaveAddr, buf, 2);

  return (error);
}


/**
 * @}
 */

/**
 * @}
 */
