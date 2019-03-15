import base64
import random

import re
from io import BytesIO
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
        sleep(2)
        image1=self.get_image('bg.png',*self.loc_bg_image)
        image2 = self.get_image('slider.png',*self.loc_slider_image)
        distance = self.get_distance('slider.png','bg.png')
        slider_button = self.find_element(*self.loc_slider_button)

        tracks= self.get_tracks(distance)

        action = ActionChains(self.driver)
        ActionChains(self.driver).click_and_hold(slider_button).perform()
        x=0
        for track in tracks:
            ActionChains(self.driver).move_by_offset(xoffset=track,yoffset=0).perform()
            x+=track

        ActionChains(self.driver).move_by_offset(xoffset=-3, yoffset=0).perform()
        sleep(1)
        ActionChains(self.driver).move_by_offset(xoffset=-5, yoffset=0).perform()
        sleep(1)
        ActionChains(self.driver).move_by_offset(xoffset=-3, yoffset=0).perform()
        sleep(1)
        ActionChains(self.driver).move_by_offset(xoffset=distance+10-x, yoffset=0).perform()
        sleep(1)
        ActionChains(self.driver).release(on_element=slider_button).perform()

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
        # file = open(name, 'wb')
        # file.write(binary_data)
        # file.close()
        image_data=BytesIO(binary_data)
        image_data.seek(0)
        img=Image.open(image_data)
        img.save(name)
        return img


    def get_tracks(self,distance):

         # s = vt + 1/2 at^2
         #    v = v_0 + at

        distance+=20
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
            forward_tracks.append(int(round(s)))

        a= sum(forward_tracks)
        # 反着滑动到准确位置
        random.shuffle(forward_tracks)
        back_tracks = [ -1, -3,-1, -2, -2, -1]  # 总共等于-10
        for i in back_tracks:
            forward_tracks.append(int(i))
        b = sum(forward_tracks)
        return forward_tracks