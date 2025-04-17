# care_system.py
import utime

class PetCare:
    def __init__(self):
        # Initialize pet stats (0-100 scale)
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.last_feed_time = utime.ticks_ms()
        self.last_play_time = utime.ticks_ms()
        self.last_pet_time = utime.ticks_ms()
        
        # Decay rates (points per second)
        self.HUNGER_DECAY = 0.05
        self.HAPPINESS_DECAY = 0.03
        self.ENERGY_DECAY = 0.02
        
        # Thresholds for different states
        self.LOW_THRESHOLD = 30
        self.HIGH_THRESHOLD = 70
        
    def update_stats(self):
        current_time = utime.ticks_ms()
        
        # Calculate time differences in seconds
        time_since_feed = utime.ticks_diff(current_time, self.last_feed_time) / 1000
        time_since_play = utime.ticks_diff(current_time, self.last_play_time) / 1000
        time_since_pet = utime.ticks_diff(current_time, self.last_pet_time) / 1000
        
        # Update stats based on decay rates
        self.hunger = max(0, min(100, self.hunger - (time_since_feed * self.HUNGER_DECAY)))
        self.happiness = max(0, min(100, self.happiness - (time_since_pet * self.HAPPINESS_DECAY)))
        self.energy = max(0, min(100, self.energy - (time_since_play * self.ENERGY_DECAY)))
        
    def feed(self):
        if self.hunger < 90:  # Prevent overfeeding
            self.hunger += 20
            self.happiness += 5
            self.last_feed_time = utime.ticks_ms()
            return "happy"
        return "unimpressed"
    
    def play(self):
        if self.energy > 20:  # Need some energy to play
            self.energy -= 10
            self.happiness += 15
            self.hunger -= 5
            self.last_play_time = utime.ticks_ms()
            return "glee"
        return "tired"
    
    def pet(self):
        self.happiness += 10
        self.last_pet_time = utime.ticks_ms()
        return "heart_eyes"
    
    def get_emotional_state(self):
        self.update_stats()
        
        # Check for critical states first
        if self.hunger < self.LOW_THRESHOLD:
            return "sad"
        if self.energy < self.LOW_THRESHOLD:
            return "tired"
        if self.happiness < self.LOW_THRESHOLD:
            return "annoyed"
            
        # Check for positive states
        if (self.hunger > self.HIGH_THRESHOLD and 
            self.happiness > self.HIGH_THRESHOLD and 
            self.energy > self.HIGH_THRESHOLD):
            return "glee"
            
        # Default state
        return "neutral"
        
    def get_stats(self):
        self.update_stats()
        return {
            "Hunger": self.hunger,
            "Happiness": self.happiness,
            "Energy": self.energy
        }