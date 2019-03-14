import base64
import random

import re
from io import BytesIO, StringIO
from time import sleep

import numpy as np
from PIL import Image
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from test.common.page import Page
import cv2


class JDLoginPage(Page):
    loc_account_login_button = (By.CSS_SELECTOR, 'div.login-tab-r')
    loc_account_input = (By.ID, "loginname")
    loc_password_input = (By.ID, 'nloginpwd')
    loc_login_button = (By.ID, 'loginsubmit')

    loc_slider_button=(By.CSS_SELECTOR,'div.JDJRV-slide-btn')
    loc_bg_image = (By.CSS_SELECTOR,'div.JDJRV-bigimg>img')
    loc_slider_image = (By.CSS_SELECTOR, 'div.JDJRV-smallimg>img')

    def login(self, account, psw):
        self.find_element(*self.loc_account_login_button).click()  #switxch to account login page
        self.find_element(*self.loc_account_input).send_keys(account) # send account
        self.find_element(*self.loc_password_input).send_keys(psw)#input password
        self.find_element(*self.loc_login_button).click()

    def sliding_vaildation(self):
        action=ActionChains(self.driver) #instantiate an action chains object

        image1=self.get_image('bg.png',*self.loc_bg_image)
        image2 = self.get_image('slider.png',*self.loc_slider_image)

        distance = self.get_distance('slider.png','bg.png')
        action.click_and_hold(self.find_element(*self.loc_slider_button)).perform()
        action.reset_actions()
        action.move_by_offset(distance,0).perform()

    def get_distance(self,slider_block, back_groung):

        block = cv2.imread(slider_block, 0)
        template = cv2.imread(back_groung, 0)
        w,h=block.shape[::-1]

        cv2.imwrite('block.jpg', block)
        cv2.imwrite('template.jpg', template)

        block = cv2.imread('block.jpg')
        block = cv2.cvtColor(block, cv2.COLOR_BGR2GRAY)
        block = abs(255 - block)

        cv2.imwrite('block.jpg', block)

        block = cv2.imread('block.jpg')
        template = cv2.imread('template.jpg')

        result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(result.argmax(), result.shape)

        return (y*278/360)

    def get_image(self,name,*args):
        base64data=re.sub('^data:image/png;base64,','',self.find_element(*args).get_attribute('src'))
        binary_data=base64.b64decode(base64data)
        image_data=BytesIO(binary_data)
        img=Image.open(image_data)
        img.save(name)
        return img

    def get_tracks(distance):
        '''
        本质来源于物理学中的加速度算距离： s = vt + 1/2 at^2
                                        v = v_0 + at

        在这里：总距离S= distance+20
                加速度：前3/5S加速度2，后半部分加速度是-3

        '''
        distance += 20  # 先滑过一点，最后再反着滑动回来
        v = 0
        t = 0.2
        forward_tracks = []

        current = 0
        mid = distance * 3 / 5
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3

            s = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            current += s
            forward_tracks.append(round(s))

        # 反着滑动到准确位置
        back_tracks = [-3, -3, -3, -2, -2, -1, -2, -1, -1, -1]  # 总共等于-10

        return {'forward_tracks': list(forward_tracks), 'back_tracks': back_tracks}


    def get_track7(self, distance):
            """
            根据偏移量和手动操作模拟计算移动轨迹
            :param distance: 偏移量
            :return: 移动轨迹
            """
            # 移动轨迹
            tracks = []
            # 当前位移
            current = 0
            # 减速阈值
            mid = distance * 4 / 5
            # 时间间隔
            t = 0.2
            # 初始速度
            v = 0

            while current < distance:
                if current < mid:
                    a = random.uniform(2, 5)
                else:
                    a = -(random.uniform(12.5, 13.5))
                v0 = v
                v = v0 + a * t
                x = v0 * t + 1 / 2 * a * t * t
                current += x

                if 0.6 < current - distance < 1:
                    x = x - 0.53
                    tracks.append(round(x, 2))

                elif 1 < current - distance < 1.5:
                    x = x - 1.4
                    tracks.append(round(x, 2))
                elif 1.5 < current - distance < 3:
                    x = x - 1.8
                    tracks.append(round(x, 2))

                else:
                    tracks.append(round(x, 2))

            print(tracks, sum(tracks))
            return tracks
