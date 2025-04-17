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
GYRO_THRESHOLD = 15
TIME_THRESHOLDS = {'glee': 30000, 'sad': 300000, 'annoyed': 180000}

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

# Display current time on OLED
def show_clock(oled):
    current_time = utime.localtime()
    formatted_time = "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5])
    oled.text(formatted_time, 0, 0)
    oled.show()

# Display image on OLED
def display_image(oled, buffer, img_res):
    fb = framebuf.FrameBuffer(buffer, img_res[0], img_res[1], framebuf.MONO_HMSB)
    oled.fill(0)
    oled.blit(fb, 0, 0)
    oled.show()

def main():
    oled, i2c_dev = init_i2c_and_oled()
    imu = MPU6050(i2c_dev)
    buffer, img_res = Emotions.Neutral()
    last_activity_time = utime.ticks_ms()
    is_sad_down = False
    is_glee = False

    while True:
        gyro = imu.gyro
        current_time = utime.ticks_ms()
        time_diff = utime.ticks_diff(current_time, last_activity_time)

        if abs(gyro.x) > GYRO_THRESHOLD or abs(gyro.y) > GYRO_THRESHOLD or abs(gyro.z) > GYRO_THRESHOLD:
            if is_sad_down:
                if time_diff < TIME_THRESHOLDS['annoyed']:
                    buffer, img_res = Emotions.Annoyed()
                else:
                    buffer, img_res = Emotions.Glee()
                is_sad_down = False
            else:
                buffer, img_res = Emotions.Glee()
                is_glee = True
            last_activity_time = current_time
        elif time_diff > TIME_THRESHOLDS['sad']:
            buffer, img_res = Emotions.SadDown()
            is_sad_down = True
            is_glee = False
            last_activity_time = current_time
        elif is_glee and time_diff > TIME_THRESHOLDS['glee']:
            buffer, img_res = Emotions.Neutral()
            is_glee = False

        display_image(oled, buffer, img_res)
        show_clock(oled)
        utime.sleep(0.1)

if __name__ == "__main__":
    main()
