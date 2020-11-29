import time

import cv2
import numpy as np
import pyscreenshot

import win32api
import win32con


class GameAction:
    @staticmethod
    def click(**kwargs):
        win32api.SetCursorPos([kwargs['x'], kwargs['y']])  # set mouse cursor location
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)  # click action
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    @staticmethod
    def click_padding_5(**kwargs):
        win32api.SetCursorPos([kwargs['x']+5, kwargs['y']+5])  # set mouse cursor location
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)  # click action
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    @staticmethod
    def sleep_500ms(**kwargs):
        time.sleep(0.5)

    @staticmethod
    def sleep_1000ms(**kwargs):
        time.sleep(1)

    @staticmethod
    def sleep_1500ms(**kwargs):
        time.sleep(1.5)

    @staticmethod
    def sleep_2000ms(**kwargs):
        time.sleep(2)

    @staticmethod
    def sleep_5000ms(**kwargs):
        time.sleep(5)

class GameEngine:
    threshold = 0       # ignore
    steps = None
    is_debug = False
    left_x = 0
    left_y = 0
    retry = 0
    client = 0

    def __init__(self, steps, threshold=0.7, client=1, retry=200, is_debug=False):
        self.steps = steps
        self.threshold = threshold
        self.left_x = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        self.left_y = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        self.is_debug = is_debug
        self.client = client
        self.retry = retry

    @staticmethod
    def get_screen_img():
        return np.array(pyscreenshot.grab())

    def match(self, img, sub_img, threshold):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        w, h = sub_img.shape[::-1]

        result = cv2.matchTemplate(img_gray, sub_img, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)

        rs = [x for x in zip(*loc[::-1])]
        if self.is_debug and len(rs) != 0 and self.client > len(rs):
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
            cv2.imshow('show match', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return rs

    def amend(self, pt):
        x, y = pt
        return (x + self.left_x, y + self.left_y)

    def run(self):
        retry = 0

        for step in self.steps:
            print("step: {0}".format(step['step_name']))
            img = cv2.imread(step['img'], 0)

            while True:
                screen = self.get_screen_img()
                points = self.match(screen, img, step['threshold'])

                if len(points) == 0:
                    retry += 1
                    if retry > self.retry:
                        raise Exception('max retry: {0}'.format(self.retry))
                    if retry % 5 == 0:
                        print('retry: {0}'.format(retry))

                    time.sleep(1)
                    continue

                if len(points) < self.client:
                    raise Exception("client num error! actual：{0}, expect: {1}, detail: {2}".format(
                        len(points),
                        self.client,
                        ','.join(str(p) for p in points)))

                for pt in points:
                    x, y = self.amend(pt)

                    for action in step['actions']:
                        kwargs ={'x': x, 'y':y}
                        action(**kwargs)

                retry = 0
                break
