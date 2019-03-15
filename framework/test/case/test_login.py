import unittest
from time import sleep

from test.page.baidu_main_page import BaiDuMainPage
from test.page.login_page import JDLoginPage
from utils.config import Config, DRIVER_PATH, DATA_PATH, REPORT_PATH

class TestLogin(unittest.TestCase):
    URL = Config().get('local_url')
    Account = Config().get('account')
    Psw = Config().get('password')

    def sub_setUp(self):
        # 初始页面是main page，传入浏览器类型打开浏览器
        self.page = JDLoginPage().get(self.URL, maximize_window=False)

    def test_login(self):
        self.page = JDLoginPage().get(self.URL, maximize_window=False)
        self.page.login(self.Account, self.Psw)
        self.page.sliding_vaildation()
        sleep(3)

if __name__ == '__main__':
        unittest.main()
