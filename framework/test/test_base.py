from unittest import TestCase

from test.page.jd_main_page import JDMainPage
from utils.config import Config, DRIVER_PATH, DATA_PATH, REPORT_PATH
from test.page.login_page import JDLoginPage

class TestBase(TestCase):
    URL = Config().get('local_url')
    Account=Config().get('account')
    Psw=Config().get('password')
    portal=None

    @classmethod
    def setUpClass(cls):
        if cls.portal==None:
            cls().sign_in()


    def sign_in(self):
        self.page = JDLoginPage().get(self.URL, maximize_window=False)
        self.page.login(self.Account,self.Psw)
        while self.page.is_slider_validation():
            self.page.sliding_vaildation()
        TestBase.portal=self.page




