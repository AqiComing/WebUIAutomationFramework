import time
from tkinter import Image

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from test.common.page import Page

class JDLoginPage(Page):
    loc_account_login_button = (By.CSS_SELECTOR, 'div.login-tab-r')
    loc_account_input = (By.ID, "loginname")
    loc_password_input = (By.ID, 'nloginpwd')
    loc_login_button = (By.ID, 'loginsubmit')

    loc_slider_button=(By.CSS_SELECTOR,'div.JDJRV-slide-btn')
    loc_bg_image = (By.CSS_SELECTOR, 'div.JDJRV-bigimg>img')
    loc_slider_image = (By.CSS_SELECTOR, 'div.JDJRV-smallimg>img')

    def login(self, account, psw):
        self.find_element(*self.loc_account_login_button).click()  #switxch to account login page
        self.find_element(*self.loc_account_input).send_keys(account) # send account
        self.find_element(*self.loc_password_input).send_keys(psw)#input password
        self.find_element(*self.loc_login_button).click()

    def sliding_vaildation(self):
        action=ActionChains(self.driver) #instantiate an action chains object

        image1=self.get_image("small.png",*self.loc_bg_image)

        image2 = self.get_image("big.png",*self.loc_slider_button)
        distance=self.get_distance(image1,image2)
        action.click_and_hold(self.find_element(*self.loc_slider_button)).perform()
        action.reset_actions()
        action.move_by_offset(distance,0).perform()

    def get_snap(self, names):
        self.driver.save_screenshot(names)
        page_snap_obj = Image.open(names)
        return page_snap_obj

    def get_image(self, names,*args,):
        img = self.driver.find_element(*args)
        time.sleep(2)
        location = img.location
        size = img.size

        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']

        page_snap_obj = self.get_snap(names)
        image_obj = page_snap_obj.crop((left, top, right, bottom))
        # image_obj.show()
        return image_obj

    def get_distance(self,image1,image2):
        threshold = 50
        for i in range(0, image1.size[0]):  # 260
            for j in range(0, image1.size[1]):  # 160
                pixel1 = image1.getpixel((i, j))
                pixel2 = image2.getpixel((i, j))
                res_R = abs(pixel1[0] - pixel2[0])  # 计算RGB差
                res_G = abs(pixel1[1] - pixel2[1])  # 计算RGB差
                res_B = abs(pixel1[2] - pixel2[2])  # 计算RGB差
                if res_R > threshold and res_G > threshold and res_B > threshold:
                    return i

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