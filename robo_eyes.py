from machine import Pin, I2C
import utime
import math

class RoboEyes:
    def __init__(self, oled, width=128, height=64):
        """
        Initialize RoboEyes with an SSD1306 OLED display instance and display dimensions.
        """
        self.oled = oled
        self.width = width
        self.height = height

        # Define basic eye dimensions and positions
        self.eye_width = 36
        self.eye_height = 36
        self.space_between = 10
        self.base_left_x = (width - (2 * self.eye_width + self.space_between)) // 2
        self.base_left_y = (height - self.eye_height) // 2
        self.left_x = self.base_left_x
        self.left_y = self.base_left_y
        self.right_x = self.left_x + self.eye_width + self.space_between
        self.right_y = self.left_y

        # Default animation state
        self.current_emotion = "neutral"
        self.blink_state = 1.0  # 1.0 = fully open, 0 = fully closed

        # Define emotion parameters. Feel free to tweak these values.
        self.emotion_states = {
            "neutral": {
                "eye_height": self.eye_height,
                "eye_width": self.eye_width,
                "top_lid": 0,
                "bottom_lid": 0,
                "radius": 6,
                "offset_x": 0,
                "offset_y": 0
            },
            "happy": {
                "eye_height": int(self.eye_height * 0.6),
                "eye_width": self.eye_width,
                "arc": True,
                "radius": 8,
                "offset_x": 0,
                "offset_y": 0
            },
            "sad": {
                "eye_height": int(self.eye_height * 0.7),
                "eye_width": self.eye_width,
                "top_lid": int(self.eye_height * 0.3),
                "bottom_lid": 0,
                "radius": 6,
                "curve_up": True,
                "curve_down": True,
                "offset_x": 0,
                "offset_y": 5
            },
            "angry": {
                "eye_height": int(self.eye_height * 0.7),
                "eye_width": self.eye_width,
                "top_lid": int(self.eye_height * 0.4),
                "bottom_lid": 0,
                "radius": 4,
                "slant": True,
                "offset_x": 0,
                "offset_y": -3
            },
            "tired": {
                "eye_height": int(self.eye_height * 0.4),
                "eye_width": self.eye_width,
                "top_lid": int(self.eye_height * 0.6),
                "bottom_lid": 0,
                "radius": 6,
                "offset_x": 0,
                "offset_y": 3
            },
            "heart_eyes": {
                "eye_height": self.eye_height,
                "eye_width": self.eye_width,
                "special": "heart",
                "radius": 0,
                "offset_x": 0,
                "offset_y": 0
            },
            "look_left": {
                "eye_height": self.eye_height,
                "eye_width": self.eye_width,
                "radius": 6,
                "offset_x": -8,
                "offset_y": 0
            },
            "look_right": {
                "eye_height": self.eye_height,
                "eye_width": self.eye_width,
                "radius": 6,
                "offset_x": 8,
                "offset_y": 0
            },
            "look_up": {
                "eye_height": self.eye_height,
                "eye_width": self.eye_width,
                "radius": 6,
                "offset_x": 0,
                "offset_y": -8
            },
            "look_down": {
                "eye_height": self.eye_height,
                "eye_width": self.eye_width,
                "radius": 6,
                "offset_x": 0,
                "offset_y": 8
            },
            "suspicious": {
                "eye_height": int(self.eye_height * 0.7),
                "eye_width": self.eye_width,
                "radius": 6,
                "offset_x": -5,
                "offset_y": -3,
                "slant": True
            },
            "confused": {
                "eye_height": self.eye_height,
                "eye_width": self.eye_width,
                "radius": 6,
                "offset_x": 5,
                "offset_y": -4,
                "squint": True
            },
            "excited": {
                "eye_height": int(self.eye_height * 1.2),
                "eye_width": int(self.eye_width * 1.2),
                "radius": 5,
                "offset_x": 0,
                "offset_y": 0,
                "sparkle": True
            },
            "sleepy": {
                "eye_height": int(self.eye_height * 0.3),
                "eye_width": self.eye_width,
                "radius": 4,
                "offset_x": 0,
                "offset_y": 4,
                "zzz": True
            }
        }

    # ---------------- Drawing Utility Functions ----------------

    def _draw_arc(self, x, y, width, height, thickness=4):
        """
        Draws a thick arc representing a 'happy' curved eyelid.
        """
        # Draw an arc along the bottom edge of the eye
        for t in range(thickness):
            for i in range(width):
                # Calculate relative x in [-1, 1]
                relative_x = (i - width / 2) / (width / 2)
                if abs(relative_x) <= 1:
                    # Use a circular formula to determine arc height
                    try:
                        arc_y = int(height * (1 - math.sqrt(1 - relative_x**2)))
                    except ValueError:
                        arc_y = 0
                    y_pos = y + arc_y + t
                    if 0 <= y_pos < self.height:
                        self.oled.pixel(x + i, y_pos, 1)

    def _draw_circle_points(self, cx, cy, radius):
        """
        Draws a filled circle centered at (cx, cy) using a midpoint circle algorithm.
        """
        cx = int(cx)
        cy = int(cy)
        radius = int(radius)
        x = radius
        y = 0
        d = 1 - radius

        while x >= y:
            # Draw horizontal lines between symmetric points
            self.oled.hline(cx - x, cy + y, 2 * x + 1, 1)
            self.oled.hline(cx - x, cy - y, 2 * x + 1, 1)
            self.oled.hline(cx - y, cy + x, 2 * y + 1, 1)
            self.oled.hline(cx - y, cy - x, 2 * y + 1, 1)

            y += 1
            if d < 0:
                d += 2 * y + 1
            else:
                x -= 1
                d += 2 * (y - x) + 1

    def _draw_heart_eye(self, x, y):
        """
        Draws a heart shape inside the designated eye region.
        """
        # Define dimensions relative to the eye area
        heart_width = int(self.eye_width * 0.8)
        heart_height = int(self.eye_height * 0.8)
        center_x = x + self.eye_width // 2
        center_y = y + self.eye_height // 2

        # Draw the two circular lobes
        radius = heart_width // 4
        for dx in range(-radius, radius):
            for dy in range(-radius, radius):
                if dx * dx + dy * dy <= radius * radius:
                    self.oled.pixel(center_x - radius + dx, center_y - radius // 2 + dy, 1)
                    self.oled.pixel(center_x + radius + dx, center_y - radius // 2 + dy, 1)

        # Draw the bottom triangle (or curved shape) of the heart
        for i in range(heart_height // 2):
            line_width = int(heart_width * (1 - (i / (heart_height / 2))) ** 0.5)
            start = center_x - line_width // 2
            self.oled.hline(start, center_y + i, line_width, 1)

    def _draw_sparkle_eye(self, x, y, width, height):
        """
        Draws an excited eye with a central circle and a sparkle cross.
        """
        cx = x + width // 2
        cy = y + height // 2
        # Main circular iris/pupil
        self._draw_circle_points(cx, cy, min(width, height) // 3)

        # Draw sparkle (a simple cross)
        sparkle_size = 3
        self.oled.line(cx - sparkle_size, cy, cx + sparkle_size, cy, 1)
        self.oled.line(cx, cy - sparkle_size, cx, cy + sparkle_size, 1)

    def _draw_sleepy_eye(self, x, y, width, height, left):
        """
        Draws a sleepy eye as a thin horizontal line. Optionally, add 'zzz' on one side.
        """
        # Draw the eyelid as a thin line
        self.oled.fill_rect(x, y + height // 2, width, 2, 1)

        # Optionally add "Zzz" on the right eye (when left==False)
        if not left:
            z_height = 8
            z_width = 6
            z_x = x + width + 5
            z_y = y - 10
            # Draw three consecutive Z's, scaling them smaller
            for _ in range(3):
                # Draw the top horizontal line of Z
                self.oled.hline(z_x, z_y, z_width, 1)
                # Draw the diagonal line of Z
                self.oled.line(z_x + z_width, z_y, z_x, z_y + z_height, 1)
                # Draw the bottom horizontal line of Z
                self.oled.hline(z_x, z_y + z_height, z_width, 1)
                # Adjust for the next Z
                z_x += 4
                z_y -= 4
                z_width = int(z_width * 0.7)
                z_height = int(z_height * 0.7)

    # ---------------- Main Eye Drawing Function ----------------

    def draw_eye(self, x, y, state, left=True):
        """
        Draws a single eye at the specified (x,y) location using the current emotion parameters.
        """
        emotion = self.emotion_states.get(self.current_emotion, self.emotion_states["neutral"])
        base_height = int(emotion.get("eye_height", self.eye_height))
        width = int(emotion.get("eye_width", self.eye_width))
        radius = int(emotion.get("radius", 6))

        # Calculate blink-induced lid closures
        blink_amount = 1.0 - self.blink_state
        top_lid_height = int(base_height * blink_amount / 2)
        bottom_lid_height = int(base_height * blink_amount / 2)

        # Adjust eye drawing height and vertical offset
        effective_height = base_height - top_lid_height - bottom_lid_height
        y_draw = y + top_lid_height  # Shift down after applying top lid

        # Apply any emotion-specific offsets
        x_draw = int(x + emotion.get("offset_x", 0))
        y_draw = int(y_draw + emotion.get("offset_y", 0))

        # Handle special drawing modes (heart, sparkle, sleepy, arc)
        if emotion.get("special") == "heart":
            self._draw_heart_eye(x_draw, y)
            return
        elif emotion.get("sparkle"):
            self._draw_sparkle_eye(x_draw, y, width, base_height)
            return
        elif emotion.get("zzz"):
            self._draw_sleepy_eye(x_draw, y, width, base_height, left)
            return
        elif emotion.get("arc"):
            self._draw_arc(x_draw, y, width, base_height)
            return

        # Draw the basic eye shape with rounded corners
        if effective_height > radius * 2:
            # Draw corner arcs
            self._draw_circle_points(x_draw + radius, y_draw + radius, radius)
            self._draw_circle_points(x_draw + width - radius, y_draw + radius, radius)
            self._draw_circle_points(x_draw + radius, y_draw + effective_height - radius, radius)
            self._draw_circle_points(x_draw + width - radius, y_draw + effective_height - radius, radius)

            # Draw rectangular parts connecting the arcs
            self.oled.fill_rect(x_draw + radius, y_draw, width - 2 * radius, effective_height, 1)
            self.oled.fill_rect(x_draw, y_draw + radius, width, effective_height - 2 * radius, 1)
        else:
            # If very closed (or during blink), just draw a rectangle
            self.oled.fill_rect(x_draw, y_draw, width, effective_height, 1)

        # Additional emotion modifications
        if emotion.get("slant"):
            # Create a slant effect by erasing part of the eye
            slant_pixels = int(effective_height * 0.4)
            if left:
                for i in range(width):
                    erase = int(slant_pixels * (i / width))
                    if erase > 0:
                        self.oled.vline(x_draw + i, y_draw, erase, 0)
            else:
                for i in range(width):
                    erase = int(slant_pixels * (1 - i / width))
                    if erase > 0:
                        self.oled.vline(x_draw + i, y_draw, erase, 0)

        if emotion.get("curve_up") and emotion.get("curve_down"):
            # Subtly remove pixels to simulate a curved (sad) eye shape
            curve_height = int(effective_height * 0.3)
            for i in range(width):
                # Curve factor: highest in the center
                factor = 1 - ((i - width/2) ** 2) / ((width/2) ** 2)
                factor = max(0, min(1, factor))
                top_curve = int(curve_height * factor)
                bottom_curve = int(curve_height * 0.7 * factor)
                if top_curve > 0:
                    self.oled.vline(x_draw + i, y_draw, top_curve, 0)
                if bottom_curve > 0:
                    self.oled.vline(x_draw + i, y_draw + effective_height - bottom_curve, bottom_curve, 0)

    # ---------------- Public API Methods ----------------

    def draw(self):
        """
        Clears the display and redraws both eyes in the current state.
        """
        self.oled.fill(0)
        self.draw_eye(self.left_x, self.left_y, self.current_emotion, left=True)
        self.draw_eye(self.right_x, self.right_y, self.current_emotion, left=False)
        self.oled.show()

    def set_emotion(self, emotion):
        """
        Sets the current emotion and redraws the eyes.
        """
        if emotion in self.emotion_states:
            self.current_emotion = emotion
            self.blink_state = 1.0  # Reset blink (fully open)
            self.draw()

    def blink(self):
        """
        Executes a smooth blink animation by adjusting the blink_state.
        """
        steps = 8
        # Close the eyes gradually
        for i in range(steps):
            self.blink_state = 1 - (i / steps)
            self.draw()
            utime.sleep(0.02)
        # Open the eyes gradually
        for i in range(steps):
            self.blink_state = i / steps
            self.draw()
            utime.sleep(0.02)

    def sequence(self, emotions, delays):
        """
        Plays a sequence of emotions. 'emotions' is a list of emotion names,
        and 'delays' is a list of times (in seconds) to wait after each emotion.
        """
        if len(emotions) != len(delays):
            raise ValueError("Number of emotions must match number of delays")
        for emotion, delay in zip(emotions, delays):
            self.set_emotion(emotion)
            utime.sleep(delay)
