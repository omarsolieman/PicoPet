# button.py
from machine import Pin
import utime

class Button:
    def __init__(self, pin_num, long_press_time=1000, debounce_time=20):
        self.pin = Pin(pin_num, Pin.IN)
        self.long_press_time = long_press_time
        self.debounce_time = debounce_time
        self.last_state = False
        self.press_start = 0
        self.last_press_time = 0
        self.is_long_pressing = False
    
    def is_pressed(self):
        return self.pin.value()
    
    def update(self):
        current_time = utime.ticks_ms()
        current_state = self.pin.value()
        result = None
        
        # Button is currently pressed
        if current_state:
            # New press
            if not self.last_state:
                self.press_start = current_time
                self.last_press_time = current_time
            # Check for long press
            elif not self.is_long_pressing and \
                 utime.ticks_diff(current_time, self.press_start) >= self.long_press_time:
                self.is_long_pressing = True
                result = "LONG_PRESS"
        
        # Button was released
        elif self.last_state:
            press_duration = utime.ticks_diff(current_time, self.press_start)
            if press_duration < self.long_press_time and \
               not self.is_long_pressing and \
               utime.ticks_diff(current_time, self.last_press_time) >= self.debounce_time:
                result = "SHORT_PRESS"
            self.is_long_pressing = False
            self.press_start = 0
            self.last_press_time = current_time
            
        self.last_state = current_state
        return result