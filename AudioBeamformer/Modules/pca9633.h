/**
 ****************************************************************
 @file    pca9633.h
 ****************************************************************
 @brief   This module offers a set of functions to handle the
          4-bit PWM LED-Driver on the I2C-Interface.
 ****************************************************************
 @author  Florian Baumgartner, HSR
 @version 1.0
 @date    2020-04-08
 @note    Functions are not reentrant and shall not be called in
          parallel from different execution contexts.
 ****************************************************************
 */
#ifndef HWO_PCA9633_H_
#define HWO_PCA9633_H_


//===============================================================
//includes
#include <stdint.h>
#include "../../GLOB_Types.h"
#include "../../HAL/hal_i2c.h"

#ifdef __cplusplus
extern "C"
{
#endif

//===============================================================
//defines

#define PCA9633_BASEADDR        0x60

#define PCA9633_MODE1           0x00    // mode register 1
#define PCA9633_MODE2           0x01    // mode register 2
#define PCA9633_PWM0            0x02    // PWM0 brightness control led0
#define PCA9633_PWM1            0x03    // PWM0 brightness control led0
#define PCA9633_PWM2            0x04    // PWM0 brightness control led0
#define PCA9633_PWM3            0x05    // PWM0 brightness control led0
#define PCA9633_GRPPWM          0x06    // group brightness (duty cycle)
#define PCA9633_GRPFREQ         0x07    // group frequency
#define PCA9633_LEDOUT          0x08    // LED output state
#define PCA9633_SUBADR1         0x09    // i2c bus sub address 1
#define PCA9633_SUBADR2         0x0A    // i2c bus sub address 1
#define PCA9633_SUBADR3         0x0B    // i2c bus sub address 1
#define PCA9633_ALLCALLADR      0x0C    // LED All Call i2c address

#define PCA9633_SLEEP           0x10    // bit 4, low power mode enable, RW
#define PCA9633_SUB1            0x08    // bit 3, PCA9633 responds to sub address 1
#define PCA9633_SUB2            0x04    // bit 2, PCA9633 responds to sub address 2
#define PCA9633_SUB3            0x02    // bit 1, PCA9633 responds to sub address 3
#define PCA9633_ALLCALL         0x01    // bit 0, PCA9633 responds to all call address

#define PCA9633_DMBLINK         0x20    // bit 5, group control dim or blink
#define PCA9633_INVRT           0x10    // bit 4, output logic invert (1=yes, 0=no)
#define PCA9633_OCH             0x08    // bit 3, 0=output change on stop, 1=output change on ACK
#define PCA9633_OUTDRV          0x04    // bit 2, output drivers 0=open drain, 1=totem poll - push pull
#define PCA9633_OUTNE1          0x02    // bit 1, 2 bits see page 13, 16 pin device only
#define PCA9633_OUTNE0          0x01    // bit 0, see above

//===========================================================
//typedefs

//===============================================================
//function prototypes
error_t pca9633_init (i2c_unit_t unit, uint8_t hw_address);
error_t pca9633_digitalWrite (uint8_t hw_address, uint8_t pin, uint8_t value);
error_t pca9633_setPwmValue (uint8_t hw_address, uint8_t pin, uint8_t value);


#ifdef __cplusplus
}
#endif

#endif /* HWO_PCA9633_H_ */
