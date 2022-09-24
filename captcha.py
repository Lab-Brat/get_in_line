import pytesseract
import cv2
import numpy as np
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def get_color_codes(image):
    return np.unique(image)

class Captcha:
    def __init__(self, image_path):
        self.digit = self.captcha_to_digit(image_path)

        # image processing parameters
        self.threshold = 230
        self.kernel_size = (0, 0)
        self.sigma = 2

    def _gray_to_blackwhite(self, image, write=False):
        gray_im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (thresh, bw_im) = cv2.threshold(gray_im, 230, 255, cv2.THRESH_BINARY)

        if write == True:
            cv2.imwrite('gr.jpeg', gray_im)
            cv2.imwrite('bw.jpeg', bw_im)

        return bw_im

    def captcha_to_digit(self, image_path):
        image_raw = cv2.imread(image_path)
        image = cv2.GaussianBlur(image_raw, (0, 0), 2)
        bw_im = self._gray_to_blackwhite(image)
        numbers = pytesseract.image_to_string(bw_im, config="tessedit_char_whitelist=0123456789")
        return ''.join(c for c in numbers if c.isdigit())
 

if __name__ == '__main__':
    for i in range(1,6):
        cap = Captcha(f'captcha/{i}.jpeg')
        print(cap.digit)
