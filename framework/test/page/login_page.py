import base64
import random

import re
from io import BytesIO, StringIO
from PIL import Image
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from test.common.page import Page


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
        self.find_element(*self.loc_slider_button).click()
        image2 = self.get_image('slider.png',*self.loc_slider_image)
        distance = self.get_gaps(image1, image2)
        action.click_and_hold(self.find_element(*self.loc_slider_button)).perform()
        action.reset_actions()
        action.move_by_offset(distance,0).perform()

    def get_gaps(self, image1,image2):
        left = 45
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self,image1,image2,x,y):
        pix1=image1.load()[x,y]
        pix2 =image2.load()[x,y]

        threshold =60
        if (abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold) and abs(
                pix1[2] - pix2[2] < threshold)):
            return True
        else:
            return False

    # def merge_image(image_file, location_list):
    #     """
    #      拼接图片
    #     :param image_file:
    #     :param location_list:
    #     :return:
    #     """
    #     im = Image.open(image_file)
    #     im.save('code.jpg')
    #     new_im = Image.new('RGB', (260, 116))
    #     # 把无序的图片 切成52张小图片
    #     im_list_upper = []
    #     im_list_down = []
    #     # print(location_list)
    #     for location in location_list:
    #         # print(location['y'])
    #         if location['y'] == -58:  # 上半边
    #             im_list_upper.append(im.crop((abs(location['x']), 58, abs(location['x']) + 10, 116)))
    #         if location['y'] == 0:  # 下半边
    #             im_list_down.append(im.crop((abs(location['x']), 0, abs(location['x']) + 10, 58)))
    #
    #     x_offset = 0
    #     for im in im_list_upper:
    #         new_im.paste(im, (x_offset, 0))  # 把小图片放到 新的空白图片上
    #         x_offset += im.size[0]
    #
    #     x_offset = 0
    #     for im in im_list_down:
    #         new_im.paste(im, (x_offset, 58))
    #         x_offset += im.size[0]
    #     new_im.show()
    #     return new_im

    # def get_image(self, *args):
    #     '''
    #     下载无序的图片  然后进行拼接 获得完整的图片
    #     :param driver:
    #     :param div_path:
    #     :return:
    #     '''
    #     time.sleep(2)
    #     background_images = self.find_element(*args)
    #     location_list = []
    #     for background_image in background_images:
    #         location = {}
    #         result = re.findall('background-image: url\("(.*?)"\); background-position: (.*?)px (.*?)px;',
    #                             background_image.get_attribute('style'))
    #         # print(result)
    #         location['x'] = int(result[0][1])
    #         location['y'] = int(result[0][2])
    #
    #         image_url = result[0][0]
    #         location_list.append(location)
    #
    #     print('==================================')
    #     image_url = image_url.replace('webp', 'jpg')
    #     # '替换url http://static.geetest.com/pictures/gt/579066de6/579066de6.webp'
    #     image_result = requests.get(image_url).content
    #     # with open('1.jpg','wb') as f:
    #     #     f.write(image_result)
    #     image_file = BytesIO(image_result)  # 是一张无序的图片
    #     image = self.merge_image(image_file, location_list)
    #base
    #     return image
    def get_image(self,name,*args):
        base64data=re.sub('^data:image/png;base64,','',self.find_element(*args).get_attribute('src'))
        binary_data=base64.b64decode(base64data)
        image_data=BytesIO(binary_data)
        img=Image.open(image_data)
        img.save(name)
        return img

    # def get_image(self, names,*args,):
    #     img = self.driver.find_element(*args)
    #     time.sleep(2)
    #     location = img.location
    #     size = img.size
    #
    #     left = location['x']
    #     top = location['y']
    #     right = left + size['width']
    #     bottom = top + size['height']
    #
    #     page_snap_obj = self.get_snap(names)
    #     image_obj = page_snap_obj.crop((left, top, right, bottom))
    #     # image_obj.show()
    #     return image_obj

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
