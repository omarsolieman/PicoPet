def load_image(filename):
    with open(filename, 'rb') as f:
        img = bytearray(f.read())
    img = bytearray(reversed(img))
    img_res = (128, 64)
    return img, img_res

def Happy():
    return load_image('EmotionsBMP/Happy.bmp')

def Glee():
    return load_image('EmotionsBMP/Glee.bmp')

def SadDown():
    return load_image('EmotionsBMP/SadDown.bmp')

def Neutral():
    return load_image('EmotionsBMP/Neutral.bmp')

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
    return load_image('EmotionsBMP/Worried.bmp')

