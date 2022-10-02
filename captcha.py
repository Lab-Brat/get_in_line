import cv2
import numpy as np
from twocaptcha import TwoCaptcha
import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def get_color_codes(image):
    return np.unique(image)

class Captcha:
    def __init__(self, image_path, write):
        self.write = write
        self.image = image_path
        self.key   = 'data/_2captcha_api_key'

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

    def _solve_local(self, image_path, write=False):
        new_size = 4
        lower_thresh = 210
        matrix_size = (0, 0)
        sigma = 4

        image = cv2.imread(image_path)
        image = self._resize(image, new_size)
        image = cv2.GaussianBlur(image, matrix_size, sigma)
        bw_im = self._gray_to_blackwhite(image, lower_thresh)

        numbers = pytesseract.image_to_string(bw_im, config='--psm 6 tessedit_char_whitelist=0123456789')

        if write == True:
            cv2.imwrite(f'data/_captcha_processed/{image_path[8]}.jpeg', bw_im)

        return ''.join(c for c in numbers if c.isdigit())

    def _read_api_key(self):
        with open(self.key, 'r') as key:
            return key.readlines()[0]

    def _solve_2captcha(self, image_path):
        api_key = self._read_api_key()
        solver = TwoCaptcha(api_key)
        return solver.normal(image_path)['code']
    
    def solve(self, method='local'):
        if method == 'local':
            return self._solve_local(self.image, self.write)
        elif method == '2captcha':
            print('Starting communication with 2captcha servers...')
            return self._solve_2captcha(self.image)


if __name__ == '__main__':
    cap = Captcha(f'data/captcha/4.jpeg', write=True)
    print(cap.solve(method='2captcha'))
