import time
from test.page.jd_main_page import JDMainPage
from test.test_base import TestBase
from utils.config import Config
from utils.log import logger  # 引入日志模块
from utils.file_reader import ExcelReader  # 引入xls读取模块
from test.page.baidu_result_page import BaiDuMainPage, BaiDuResultPage

class TestBaiDu(TestBase):
    main_page=None
    Goods_Name=Config().get('goods')

    def setUp(self):
        self.main_page = JDMainPage(TestBase.portal)

    def tearDown(self):
        self.main_page.save_screen_shot()
        self.main_page.quit()  # 清理退出

    def test_openJD(self):
        # 1.verify main page title
        self.assertIn('京东(JD.COM)',self.main_page.title,'Main page title is incorrect')
        # 2.Search goods
        self.main_page.search(self.Goods_Name)
        self.main_page.switch_to_window()


    def test_search(self):
        datas = ExcelReader(self.excel).data
        for d in datas:
            with self.subTest(data=d):
                self.sub_setUp()
                self.page.search(d['search'])
                time.sleep(2)
                self.page = BaiDuResultPage(self.page)  # 页面跳转到result page
                links = self.page.result_links
                for link in links:
                    logger.info(link.text)
                self.sub_tearDown()


# if __name__ == '__main__':
#     #unittest.main()
#
#     report = REPORT_PATH + '\\report.html'
#     print(report)
#     with open(report, 'wb') as f:
#         runner = HTMLTestRunner(f, verbosity=2, title='栾鹏全栈', description='修改html报告')
#         runner.run(TestBaiDu('test_search'))

    # e = Email(title='百度搜索测试报告',
    #           message='这是今天的测试报告，请查收！',
    #           receiver='...',
    #           server='...',
    #           sender='...',
    #           password='...',
    #           path=report
    #           )
    # e.send()