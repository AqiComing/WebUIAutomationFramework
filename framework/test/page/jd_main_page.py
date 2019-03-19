from selenium.webdriver.common.by import By
from test.common.page import Page

# 封装的百度首页

class JDMainPage(Page):
    loc_jd_logo = (By.CSS_SELECTOR, 'div.logo_tit')
    loc_search_input=(By.CSS_SELECTOR,'input.text')
    loc_search_button = (By.CSS_SELECTOR, 'button.button')
    loc_goods_item =(By.CSS_SELECTOR,'li.gl-item')

    def search(self,goods_name):
        self.find_element(*self.loc_search_input).send_keys(goods_name)
        self.find_element(*self.loc_search_button).click()
        self.switch_to_window()
        self.find_elements(*self.loc_goods_item)[1].click()


