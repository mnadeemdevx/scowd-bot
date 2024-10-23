from captcha.image import ImageCaptcha
import random


def generate_captcha():
    image = ImageCaptcha(width=180, height=60)
    captcha_text = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=5))
    captcha_image = image.generate(captcha_text)
    return captcha_text, captcha_image
