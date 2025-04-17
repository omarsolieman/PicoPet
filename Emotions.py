def Blink():
    frames = [load_image(f'Animation/BlinkNeutral/{i:04d}.bmp') for i in range(1, 14)]
    return frames

def Glee():
    frames = [load_image(f'Animation/Glee/{i:04d}.bmp') for i in range(1, 15)]
    return frames

def SadDown():
    frames = [load_image(f'Animation/SadDown/{i:04d}.bmp') for i in range(1, 15)]
    return frames

def HeartEyes():
    frames = [load_image(f'Animation/HeartEyes/{i:04d}.bmp') for i in range(1, 22)]
    return frames

def Mad():
    frames = [load_image(f'Animation/Mad/{i:04d}.bmp') for i in range(1, 18)]
    return frames

def load_image(filename):
    with open(filename, 'rb') as f:
        img = bytearray(f.read())
    img = bytearray(reversed(img))
    img_res = (128, 64)
    return img, img_res

def Happy():
    return load_image('EmotionsBMP/Happy.bmp')

def Neutral():
    return load_image('EmotionsBMP/0001.bmp')

def BlinkDown():
    return load_image('EmotionsBMP/BlinkDown.bmp')

def Annoyed():
    return load_image('EmotionsBMP/Annoyed.bmp')

def Focused():
    return load_image('EmotionsBMP/Focused.bmp')

def SadUp():
    return load_image('EmotionsBMP/SadUp.bmp')

def Skeptic():
    return load_image('EmotionsBMP/Skeptic.bmp')

def Surprised():
    return load_image('EmotionsBMP/Surprised.bmp')

def Unimpressed():
    return load_image('EmotionsBMP/Unimpressed.bmp')

def Worried():
    return load_image('EmotionsBMP/Skeptic.bmp')

