import unittest
import os
import time
from macaca import WebDriver

desired_caps = {
    'platformName': 'android',
    'app': './app/android-app-bootstrap.zip',
    'reuse': 3
}

server_url = {
    'hostname': 'localhost',
    'port': 3456
}

def switch_to_webview(driver):
    contexts = driver.contexts
    driver.context = contexts[-1]
    return driver

def switch_to_native(driver):
    contexts = driver.contexts
    driver.context = contexts[0]
    return driver

class MacacaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver(desired_caps, server_url)
        cls.driver.init()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_01_login(self):
        self.driver \
            .element_by_xpath('//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.EditText[1]') \
            .send_keys('中文+Test+12345678')   \

        els = self.driver \
            .elements_by_class_name('android.widget.EditText')

        els[1].send_keys('111111')

        self.driver \
            .element_by_name('Login') \
            .click()

    def test_02_scroll_tableview(self):
        self.driver              \
            .element_by_name('HOME') \
            .click()

        self.driver             \
            .element_by_name('list') \
            .click() \
            .swipe(200, 420, 200, 10, 50)

    def test_03_webview(self):
        self.driver \
            .swipe(200, 400, 200, 100, 500) \
            .back() \
            .element_by_name('Webview') \
            .click()

        time.sleep(3)
        self.driver.save_screenshot('./webView.png') # save screen shot

        switch_to_webview(self.driver) \
            .element_by_id('pushView') \
            .tap()

        switch_to_webview(self.driver) \
            .element_by_id('popView') \
            .tap()

    def test_04_web(self):
        switch_to_native(self.driver) \
            .element_by_name('Baidu') \
            .tap()

        time.sleep(3)
        self.driver.save_screenshot("./baidu.png")

        switch_to_webview(self.driver) \
            .element_by_id('index-kw') \
            .send_keys('macaca')

        self.driver \
            .element_by_id('index-bn') \
            .tap()

    def test_05_logout(self):
        switch_to_native(self.driver) \
            .element_by_name('PERSONAL') \
            .click()

        self.driver.element_by_name('Logout') \
            .click()

if __name__ == '__main__':
    unittest.main()
