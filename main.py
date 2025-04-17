from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import utime
import sys
from robo_eyes import RoboEyes
from care_system import PetCare
from button import Button
import random

# Constants
PIX_RES_X = 128
PIX_RES_Y = 64
I2C_FREQ = 200000
SCL_PIN = 27
SDA_PIN = 26
TOUCH_PIN_1 = 16    # Left - Feed
TOUCH_PIN_2 = 17    # Up - Play
TOUCH_PIN_3 = 18    # Right - Pet
DEBOUNCE_TIME = 200  # milliseconds

# Timing constants for sequences
EMOTION_DELAY = 0.4  # Time for each emotion in a sequence
BLINK_INTERVAL = 100  # Counter value for regular blinks
INACTIVITY_SLEEP = 60000  # 1 minute
INACTIVITY_SAD = 120000   # 2 minutes

# Emotional state mappings from pet care to RoboEyes emotions
EMOTION_MAP = {
    "neutral": ["neutral"],
    "happy": ["happy", "excited", "happy"],
    "sad": ["sad", "look_down", "sad"],
    "tired": ["tired", "sleepy"],
    "glee": ["excited", "happy", "excited"],
    "heart_eyes": ["heart_eyes", "happy"],
    "annoyed": ["angry", "suspicious", "angry"],
    "unimpressed": ["suspicious", "look_left", "look_right", "suspicious"]
}

# Interactive sequences
REACTION_SEQUENCES = {
    "feed": {
        "good": ["look_up", "excited", "happy", "neutral"],
        "bad": ["suspicious", "look_left", "unimpressed"]
    },
    "play": {
        "good": ["excited", "look_left", "look_right", "happy", "neutral"],
        "bad": ["tired", "sleepy", "sad"]
    },
    "pet": {
        "good": ["look_up", "heart_eyes", "happy", "neutral"],
        "bored": ["suspicious", "look_left", "unimpressed", "neutral"]
    },
    "idle": {
        "curious": ["look_left", "look_right", "look_up", "neutral"],
        "sleepy": ["tired", "sleepy", "look_down", "sleepy"],
        "bored": ["suspicious", "look_left", "unimpressed", "neutral"]
    }
}

# Startup sequence
STARTUP_SEQUENCE = [
    "neutral", "look_left", "look_right", "look_up", "look_down",
    "happy", "excited", "heart_eyes", "neutral"
]

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
    return oled

def init_buttons():
    return {
        'feed': Button(TOUCH_PIN_1),
        'play': Button(TOUCH_PIN_2),
        'pet': Button(TOUCH_PIN_3)
    }

def display_stats(oled, pet):
    """Display pet stats on the OLED"""
    oled.fill(0)
    stats = pet.get_stats()
    y_pos = 0
    for stat, value in stats.items():
        text = f"{stat}: {value:.1f}"
        oled.text(text, 0, y_pos)
        y_pos += 10
    oled.show()

def play_emotion_sequence(eyes, sequence, delay=EMOTION_DELAY):
    """Play a sequence of emotions with optional custom delay"""
    for emotion in sequence:
        eyes.set_emotion(emotion)
        utime.sleep(delay)
        if emotion != "neutral":  # Add natural blink after non-neutral emotions
            if random.randint(0, 2) == 0:  # 33% chance to blink
                eyes.blink()

def show_startup_animation(eyes):
    """Display startup sequence to show the system is working"""
    play_emotion_sequence(eyes, STARTUP_SEQUENCE, 0.3)

def main():
    # Initialize random seed using current time
    random.seed(utime.ticks_ms())
    
    # Initialize hardware
    oled = init_i2c_and_oled()
    buttons = init_buttons()
    
    # Initialize systems
    eyes = RoboEyes(oled)
    pet = PetCare()
    
    # Show startup sequence
    show_startup_animation(eyes)
    
    # State variables
    showing_stats = False
    blink_counter = 0
    last_activity_time = utime.ticks_ms()
    current_emotion = "neutral"
    idle_counter = 0

    while True:
        current_time = utime.ticks_ms()
        
        # Handle button inputs
        for action, button in buttons.items():
            result = button.update()
            if result == "LONG_PRESS":
                showing_stats = True
                break
            elif result == "SHORT_PRESS":
                if action == 'feed':
                    pet_state = pet.feed()
                    sequence = REACTION_SEQUENCES["feed"]["good"] if pet_state != "unimpressed" \
                             else REACTION_SEQUENCES["feed"]["bad"]
                    play_emotion_sequence(eyes, sequence)
                elif action == 'play':
                    pet_state = pet.play()
                    sequence = REACTION_SEQUENCES["play"]["good"] if pet_state != "tired" \
                             else REACTION_SEQUENCES["play"]["bad"]
                    play_emotion_sequence(eyes, sequence)
                elif action == 'pet':
                    pet_state = pet.pet()
                    sequence = REACTION_SEQUENCES["pet"]["good"] if pet_state == "heart_eyes" \
                             else REACTION_SEQUENCES["pet"]["bored"]
                    play_emotion_sequence(eyes, sequence)
                last_activity_time = current_time
                break
        
        # Check if we should exit stats display
        if showing_stats and all(not button.is_pressed() for button in buttons.values()):
            showing_stats = False
            eyes.set_emotion("neutral")
        
        # Regular state updates
        if not showing_stats:
            # Update emotional state based on pet care state
            pet_state = pet.get_emotional_state()
            new_emotion_sequence = EMOTION_MAP.get(pet_state, ["neutral"])
            
            # Only update emotion if it's different
            if new_emotion_sequence[0] != current_emotion:
                play_emotion_sequence(eyes, new_emotion_sequence)
                current_emotion = new_emotion_sequence[0]
            
            # Handle blinking
            blink_counter += 1
            if blink_counter >= BLINK_INTERVAL:
                eyes.blink()
                blink_counter = 0
            
            # Handle idle animations
            idle_counter += 1
            if idle_counter >= 300:  # Every ~15 seconds
                if random.randint(0, 2) == 0:  # 33% chance to show idle animation
                    idle_type = ["curious", "sleepy", "bored"][random.randint(0, 2)]
                    play_emotion_sequence(eyes, REACTION_SEQUENCES["idle"][idle_type])
                idle_counter = 0
        else:
            display_stats(oled, pet)
        
        # Handle inactivity
        inactivity_time = utime.ticks_diff(current_time, last_activity_time)
        if inactivity_time > INACTIVITY_SAD:  # After 2 minutes
            if current_emotion != "sad":
                play_emotion_sequence(eyes, ["look_down", "sad"])
                current_emotion = "sad"
        elif inactivity_time > INACTIVITY_SLEEP:  # After 1 minute
            if current_emotion != "sleepy":
                play_emotion_sequence(eyes, ["tired", "sleepy"])
                current_emotion = "sleepy"
        
        utime.sleep(0.05)  # 50ms delay for smooth operation

if __name__ == "__main__":
    main()
