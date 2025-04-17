from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import Emotions
from imu import MPU6050
import utime
import sys

# Constants
PIX_RES_X = 128
PIX_RES_Y = 64
I2C_FREQ = 200000
SCL_PIN = 27
SDA_PIN = 26
GYRO_THRESHOLD = 20
TIME_THRESHOLDS = {'glee': 50, 'sad': 3000, 'annoyed': 18000}

# Initialize I2C and OLED
def init_i2c_and_oled():
    i2c_dev = I2C(1, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=I2C_FREQ)
    i2c_addr = [hex(ii) for ii in i2c_dev.scan()]
    if not i2c_addr:
        print('No I2C Display Found')
        sys.exit()
    else:
        print(f"I2C Address      : {i2c_addr[0]}")
        print(f"I2C Configuration: {i2c_dev}")

    oled = SSD1306_I2C(PIX_RES_X, PIX_RES_Y, i2c_dev)
    return oled, i2c_dev


# Display image on OLED
def display_image(oled, buffer, img_res):
    fb = framebuf.FrameBuffer(buffer, img_res[0], img_res[1], framebuf.MONO_HMSB)
    oled.fill(0)
    oled.blit(fb, 0, 0)
    oled.show()

def display_anims(oled, frames, imu):
    for frame in frames:
        display_image(oled, frame[0], frame[1])
        utime.sleep(0.08)
        
def main():
    # Load animation frames
    animationBlink = Emotions.Blink()
    animationGlee = Emotions.Glee()
    animationSadDown = Emotions.SadDown()
    animationHeartEyes = Emotions.HeartEyes()
    animationMad = Emotions.Mad()
    oled, i2c_dev = init_i2c_and_oled()
    imu = MPU6050(i2c_dev)

    animations = [animationBlink, animationGlee, animationSadDown, animationHeartEyes, animationMad]

    while True:
        for animation in animations:
            display_anims(oled, animation, imu)
            utime.sleep(2)  # Sleep for 2 seconds between animations

if __name__ == "__main__":
    main()