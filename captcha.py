import pytesseract
import cv2
import numpy as np
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def get_color_codes(image):
    return np.unique(image)

class Captcha:
    def __init__(self, image_path, write):
        self.write = write
        self.digit = self.captcha_to_digit(image_path, write)

    def _resize(self, image, new_size):
        (h, w) = image.shape[:2]
        return cv2.resize(image, (w*new_size, h*new_size))

    def _gray_to_blackwhite(self, image, lower_thresh, write=False):
        gray_im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        bw_im = cv2.threshold(gray_im, lower_thresh, 255, cv2.THRESH_BINARY)[1]

        if write == True:
            cv2.imwrite('gr.jpeg', gray_im)
            cv2.imwrite('bw.jpeg', bw_im)

        return bw_im

    def captcha_to_digit(self, image_path, write=False):
        new_size = 5
        lower_thresh = 210
        matrix_size = (0, 0)
        sigma = 6.5

        image = cv2.imread(image_path)
        image = self._resize(image, new_size)
        image = cv2.GaussianBlur(image, matrix_size, sigma)
        bw_im = self._gray_to_blackwhite(image, lower_thresh)

        numbers = pytesseract.image_to_string(bw_im, lang='eng',
                config='--psm 6 tessedit_char_whitelist=0123456789')

        if write == True:
            cv2.imwrite(f'captcha_processed/{image_path[8]}.jpeg', bw_im)

        return ''.join(c for c in numbers if c.isdigit())


if __name__ == '__main__':
    for i in range(1,6):
        cap = Captcha(f'captcha/{i}.jpeg', write=True)
        print(cap.digit)
