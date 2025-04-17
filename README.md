# PicoPet
An Open Source Desktop pet based on the raspberry pi pico and micropython
# PicoPet - Raspberry Pi Pico W Digital Pet

![PicoPet Emotion Example](placeholder.png) A cute and interactive digital desktop pet powered by a Raspberry Pi Pico W. PicoPet uses an OLED display to show various emotions and animations, reacting to movement via an accelerometer and interactions through capacitive touch buttons.

## Features

* **Expressive Emotions:** Displays a wide range of emotions and animations on a 0.96" SSD1306 OLED screen.
* **Movement Interaction:** Detects movement and shaking using an MPU6050 accelerometer/gyroscope to trigger reactions.
* **Pet Care System (V2):** Simulates pet needs with internal stats for Hunger, Happiness, and Energy that decay over time.
* **Capacitive Touch Interaction (V2):** Feed, play with, or pet your PicoPet using three capacitive touch buttons. Hold a button to view its current stats.
* **Complex Animations (V2):** Utilizes the `robo_eyes.py` module for more dynamic and detailed eye animations.
* **(Optional) Web File Uploader:** Includes a simple web server to upload new animation files over WiFi.
* **MicroPython Powered:** Runs on MicroPython for the Raspberry Pi Pico W.

## Hardware Requirements

* Raspberry Pi Pico W
* MPU6050 Accelerometer/Gyroscope Module
* SSD1306 0.96 inch I2C OLED Display (128x64 pixels)
* 3x Capacitive Touch Sensor Modules (e.g., TTP223) - *Required for V2 interaction*
* Breadboard and Jumper Wires

## Software Requirements

* MicroPython firmware for Raspberry Pi Pico W.
* Project Files:
    * `main.py`
    * `robo_eyes.py`
    * `care_system.py`
    * `Emotions.py`
    * `imu.py`
    * `ssd1306.py`
    * `vector3d.py`
    * `button.py`
* Animation/Emotion Image Files (`.bmp` format)

## Installation & Setup

1.  **Flash MicroPython:** Install the latest MicroPython firmware onto your Raspberry Pi Pico W.
2.  **Wiring:** Connect the components to the Pico W according to the pins defined in `V2/main.py`:
    * **OLED (I2C):** SDA -> GP26, SCL -> GP27, VCC -> 3.3V, GND -> GND
    * **MPU6050 (I2C):** SDA -> GP26, SCL -> GP27, VCC -> 3.3V, GND -> GND (Shared I2C pins with OLED)
    * **Capacitive Buttons:**
        * Feed Button -> GP16
        * Play Button -> GP17
        * Pet Button -> GP18
        * (Connect VCC and GND for buttons as required by your modules)
3.  **Upload Files:** Copy all the required `.py` files listed above to the root directory of your Pico W's filesystem using an IDE like Thonny.
4.  **Create Directories:** Create the necessary directories on the Pico W:
    * `/Animation/` (and subdirectories like `/Animation/BlinkNeutral/`, `/Animation/Glee/` etc. as needed by `V2/Emotions.py`)
    * `/EmotionsBMP/` (if using static BMPs)
    * `/Web/` (if using the file uploader)
5.  **Upload Assets:** Upload your `.bmp` animation frames/emotion images into the corresponding `/Animation/` subdirectories or `/EmotionsBMP/` directory. Ensure filenames match those referenced in `V2/Emotions.py`. Upload `index.html` and `style.css` to `/Web/` if using the uploader.
6.  **(Optional) Configure WiFi:** If using `fileUpload.py`, edit the file to include your WiFi SSID and password. You might also need to update the hardcoded IP address in `fileUpload.py` and `Web/index.html`.

## Usage

1.  **Power On:** Connect the Raspberry Pi Pico W to a power source.
2.  **Boot Sequence:** PicoPet will run its startup animation.
3.  **Interaction:**
    * **Movement:** Gently shake or move the PicoPet to see its reaction.
    * **Buttons (V2):**
        * Tap Left Button (GP16): Feed the pet.
        * Tap Up Button (GP17): Play with the pet.
        * Tap Right Button (GP18): Pet the pet.
        * Hold any Button: Display the pet's current stats (Hunger, Happiness, Energy).
    * **Idle Behavior:** The pet will show idle animations and blink occasionally. Its mood will change based on its care stats and inactivity time.
4.  **(Optional) File Upload:** If `fileUpload.py` is running, navigate to the Pico W's IP address in a web browser to upload new animation folders/files.

## License

Based on the included `imu.py` driver, this project is likely intended to be under the **MIT License**. Please confirm and add a LICENSE file if desired.
