from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf, sys
import Emotions  # import the image files
import time
from imu import MPU6050

# Constants for the OLED display resolution
PIX_RES_X = 128
PIX_RES_Y = 64

# Initialize I2C on I2C1 (GPIO 26/27) with a frequency of 200000
i2c_dev = I2C(1, scl=Pin(27), sda=Pin(26), freq=200000)

# Get I2C address in hex format
i2c_addr = [hex(ii) for ii in i2c_dev.scan()]

# Check if any I2C device is found
if not i2c_addr:
    print('No I2C Display Found')
    sys.exit()
else:
    print(f"I2C Address      : {i2c_addr[0]}")
    print(f"I2C Configuration: {i2c_dev}")

# Initialize the OLED controller
oled = SSD1306_I2C(PIX_RES_X, PIX_RES_Y, i2c_dev)

# Create an MPU6050 object
imu = MPU6050(i2c_dev)

# Initialize the image to be displayed as neutral
buffer, img_res = Emotions.Neutral()

# Main loop to update the display based on the gyroscope data
while True:
    # Check if shaking is detected
    if abs(imu.gyro.x) > 20 or abs(imu.gyro.y) > 20 or abs(imu.gyro.z) > 20:
        buffer, img_res = Emotions.Glee()
    else:
        buffer, img_res = Emotions.Neutral()
    
    # Create a frame buffer object and display the image
    fb = framebuf.FrameBuffer(buffer, img_res[0], img_res[1], framebuf.MONO_HMSB)
    oled.fill(0)
    oled.blit(fb, 0, 0)
    oled.show()

    # Sleep for a short time before the next update
    time.sleep(0.1)
