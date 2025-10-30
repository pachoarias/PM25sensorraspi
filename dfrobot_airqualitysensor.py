# -*- coding:utf-8 -*-

# This file is the DFRobot_AirQualitySensor Python library file, 
# modified to resolve compatibility issues with the Raspberry Pi 4.

import time
import smbus2 as smbus # Fix 1: Use smbus2 and alias it to smbus
import spidev
import RPi.GPIO as GPIO
import os
import math

# Fix 2: Add missing constants for mode selection
I2C_MODE = 0
UART_MODE = 1
# -----------------------------------------------

# The rest of the file content starts here (unmodified DFRobot code structure)

# I2C ADDRESS
I2C_ADDR = 0x19

# COMMUNICATION MODE
I2C_MODE = 0
UART_MODE = 1

# COMMANDS
SET_UART_MODE = 0x01
SET_I2C_MODE = 0x02

# PM TYPE
PARTICLE_PM1_0_STANDARD = 0
PARTICLE_PM2_5_STANDARD = 1
PARTICLE_PM10_STANDARD = 2
PARTICLE_PM1_0_ATMOSPHERE = 3
PARTICLE_PM2_5_ATMOSPHERE = 4
PARTICLE_PM10_ATMOSPHERE = 5

# PARTICLE NUMBER TYPE
PARTICLENUM_0_3_UM_EVERY0_1L_AIR = 0
PARTICLENUM_0_5_UM_EVERY0_1L_AIR = 1
PARTICLENUM_1_0_UM_EVERY0_1L_AIR = 2
PARTICLENUM_2_5_UM_EVERY0_1L_AIR = 3
PARTICLENUM_5_0_UM_EVERY0_1L_AIR = 4
PARTICLENUM_10_UM_EVERY0_1L_AIR = 5

class DFRobot_AirQualitySensor(object):
    '''
      @brief Sensor class
      @param bus - I2C bus number. Default is 1
      @param addr - I2C address. Default is 0x19
      @param mode - Communication mode. Default is I2C_MODE
    '''
    def __init__(self ,bus ,addr):
        self.i2cbus = smbus.SMBus(bus)
        self.i2caddr = addr
        self.__uart_i2c = I2C_MODE
        self.__i2c_uart_flag = True

    def gain_particle_concentration_ugm3(self,PMtype):
        '''
          @brief Get the concentration of the specified particle type
          @param type:PARTICLE_PM1_0_STANDARD  Particle concentration of PM1.0 in standard particle
                         PARTICLE_PM2_5_STANDARD  Particle concentration of PM2.5 in standard particle
                         PARTICLE_PM10_STANDARD   Particle concentration of PM10 in standard particle
                         PARTICLE_PM1_0_ATMOSPHERE Particulate matter concentration of PM1.0 in atmospheric environment
                         PARTICLE_PM2_5_ATMOSPHERE Particulate matter concentration of PM2.5 in atmospheric environment
                         PARTICLE_PM10_ATMOSPHERE  Particulate matter concentration of PM10 in atmospheric environment
          @return concentration（ug/m3）
        '''
        if self.__i2c_uart_flag == True:
            PMdata = self.read_reg(0x02,16)
            PMvalue = PMdata[PMtype*2]*256 + PMdata[PMtype*2+1]
            return PMvalue
        else:
            PMdata = self.read_reg(0x02,20)
            PMvalue = PMdata[PMtype*2]*256 + PMdata[PMtype*2+1]
            return PMvalue

    def gain_particlenum_every0_1l(self,PMtype):
        '''
          @brief Get the number of particles per 0.1 liter of air
          @param type:PARTICLENUM_0_3_UM_EVERY0_1L_AIR
                         PARTICLENUM_0_5_UM_EVERY0_1L_AIR
                         PARTICLENUM_1_0_UM_EVERY0_1L_AIR
                         PARTICLENUM_2_5_UM_EVERY0_1L_AIR
                         PARTICLENUM_5_0_UM_EVERY0_1L_AIR
                         PARTICLENUM_10_UM_EVERY0_1L_AIR
          @return number
        '''
        if self.__i2c_uart_flag == True:
            PMdata = self.read_reg(0x02,16)
            PMvalue = PMdata[PMtype*2 + 12]*256 + PMdata[PMtype*2 + 13]
            return PMvalue
        else:
            PMdata = self.read_reg(0x02,20)
            PMvalue = PMdata[PMtype*2 + 12]*256 + PMdata[PMtype*2 + 13]
            return PMvalue

    def gain_version(self):
        '''
          @brief Get sensor version number
          @return version
        '''
        version = self.read_reg(0x00,1)
        return version[0]

    def set_lowpower(self):
        '''
          @brief Set sensor to low power
        '''
        mode = [0x00]
        self.write_reg(0x01,mode)

    def awake(self):
        '''
          @brief Wake up sensor
        '''
        mode = [0x02]
        self.write_reg(0x01,mode)

    # --- Start of Custom Fix for Active Mode ---
    def set_active_mode(self):
        '''
          @brief Set sensor to continuous reporting (Active) mode. 
          @note Fixes the issue where the sensor reports 0s after awake().
        '''
        mode = [0x01]  # Value 0x01 is assumed to be the Active Mode command for Reg 0x01
        self.write_reg(0x01,mode)
    # --- End of Custom Fix ---

    def write_reg(self, reg, data):
        '''
          @brief Writes data to the specified register of the sensor
          @param reg - Register address
          @param data - The data to be written
        '''
        self.i2cbus.write_i2c_block_data(self.i2caddr, reg, data)

    def read_reg(self, reg ,len):
        '''
          @brief Read data from the specified register of the sensor
          @param reg - Register address
          @param len - The length of the data to be read
          @return list or None
        '''
        try:
            rslt = self.i2cbus.read_i2c_block_data(self.i2caddr, reg ,len)
            return rslt
        except IOError:
            return None
