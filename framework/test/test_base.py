from unittest import TestCase
from utils.config import Config, DRIVER_PATH, DATA_PATH, REPORT_PATH
from test.page.login_page import JDLoginPage

class TestBase(TestCase):
    URL = Config().get('local_url')
    Account=Config().get('account')
    Psw=Config().get('password')
    portal=None

    def setUp(self):
        self.sign_in()


    def sign_in(self):
        self.page = JDLoginPage.get(self.URL, maximize_window=False)
        self.page.login(self.Account,self.Psw)


