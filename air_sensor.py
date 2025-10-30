import time
import sys
# Import smbus2 for I2C and the corrected DFRobot library file
from smbus2 import SMBus
from dfrobot_airqualitysensor import DFRobot_AirQualitySensor 

# --- I2C/Sensor Constants ---
I2C_ADDRESS = 0x19
I2C_BUS_NUMBER = 1 

# Particle constants for the library methods
PARTICLE_PM1_0_STANDARD = 0
PARTICLE_PM2_5_STANDARD = 1
PARTICLE_PM10_STANDARD  = 2

# Initialize Sensor Object
particle = DFRobot_AirQualitySensor(I2C_BUS_NUMBER, I2C_ADDRESS) 


def setup():
    print("Initializing sensor via I2C...")
    
    # 1. Set mode to continuous reporting (Active Mode)
    try:
        particle.set_active_mode() 
        print("Sensor set to Active Mode.")
    except Exception as e:
        print(f"I2C Communication Error during setup: {e}")
        sys.exit()

    # 2. Check for communication by reading the firmware version
    version = particle.gain_version()  
    print(f"Sensor Firmware Version: {version}")

    print("Sensor setup complete! Reading data...")
    time.sleep(5) 


def loop():
    while True:
        try:
            # Note: Using the corrected Python method names (lowercase/underscores)
            PM2_5 = particle.gain_particle_concentration_ugm3(PARTICLE_PM2_5_STANDARD)
            PM1_0 = particle.gain_particle_concentration_ugm3(PARTICLE_PM1_0_STANDARD)
            PM10 = particle.gain_particle_concentration_ugm3(PARTICLE_PM10_STANDARD)
            
            print("\n--- Air Quality Reading (ug/m3) ---")
            print(f"PM2.5 concentration: {PM2_5}")
            print(f"PM1.0 concentration: {PM1_0}")
            print(f"PM10 concentration: {PM10}")
            print("-" * 35)

        except Exception as e:
            print(f"Error reading sensor data: {e}. Retrying...")
            
        time.sleep(2)

if __name__ == "__main__":
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit()
