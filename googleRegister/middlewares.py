# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import time
from logging import getLogger
import random

import scrapy.http
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse, TextResponse
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from googleRegister.settings import IP_PROXY, SYS_OS
import os


def generate_random_number(randomLength=8):
    randomStr = ""
    baseStr = '0123456789'
    length = len(baseStr) - 1
    for i in range(randomLength):
        randomStr += baseStr[random.randint(0, length)]
    return randomStr


def generate_random_str(randomLength=8, number=True):
    randomStr = ""
    baseStr = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz'
    if number:
        baseStr = baseStr + "0123456789"
    length = len(baseStr) - 1
    for i in range(randomLength):
        randomStr += baseStr[random.randint(0, length)]
    return randomStr


def generate_first_name():
    firstNameArr = [
        "Degan",
        "Bottorff",
        "Selim",
        "Drago",
        "Roselin",
        "Lere",
        "Gier",
        "Nancy",
        "Vigrass",
        "Teena",
        "Pepe",
        "Lei",
        "Yang",
        "Zhao",
        "Yu",
        "kemplin",
        "Mirick",
        "Fanger",
        "Valorie",
        "Wurster",
        "Paylor",
        "Beldock",
        "Edi",
        "Mor",
        "Minna",
        "zela",
        "Meetze",
        "Bartus",
        "Lan",
        "Li",
        "Chen",
        "Lin",
        "Peng",
        "Wu",
    ]
    return firstNameArr[random.randint(0, len(firstNameArr) - 1)]


def generate_last_name():
    lastName = generate_random_str(random.randint(5, 9), False)
    if random.randint(1, 100) > (100 - 10):
        lastName = lastName + generate_random_str(random.randint(3, 6), False)
    return lastName.lower()


def generate_email_address():
    easterEgg = [
        "Love",
        "1314",
        "Lucky",
        "520",
        "1314520"
    ]
    emailAddress = generate_random_str(random.randint(6, 10), False)
    specialRandom = random.randint(1, 30)
    if specialRandom > 29:
        numbersTotal = random.randint(7, 10)
    elif specialRandom > 20:
        numbersTotal = random.randint(5, 8)
    elif specialRandom > 5:
        numbersTotal = random.randint(3, 6)
    else:
        numbersTotal = 0
    if numbersTotal > 0:
        insertLen = random.randint(0, len(emailAddress) - 1)
        insertChar = generate_random_number(numbersTotal)
        emailAddress = emailAddress[:insertLen] + insertChar + emailAddress[insertLen:]
    easterEggNumber = random.randint(1, 100)
    combinations = None
    if numbersTotal < 3 and (easterEggNumber == 66 or easterEggNumber == 88):
        # 触发彩蛋
        key = random.randint(0, len(easterEgg) - 1)
        combinations = easterEgg[key]
    if combinations:
        emailAddress = emailAddress + combinations
    return emailAddress.capitalize()


def generate_password():
    password = generate_random_str(random.randint(8, 15))
    specialSymbols = [
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "_",
        "!",
    ]
    specialRandom = random.randint(1, 30)
    if specialRandom > 29:
        specialTotal = 3
    elif specialRandom > 20:
        specialTotal = 2
    elif specialRandom > 5:
        specialTotal = 1
    else:
        specialTotal = 0
    for index in range(specialTotal):
        insertLen = random.randint(0, len(password) - 1)
        insertChar = specialSymbols[random.randint(0, len(specialSymbols) - 1)]
        password = password[:insertLen] + insertChar + password[insertLen:]
    return password


if __name__ == '__main__':
    passWd = generate_password()
    print(passWd)


class GoogleregisterSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class GoogleregisterDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self, timeout=None):
        self.crawl_count = 0
        self.rnd_int = 1
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("no-sandbox")
        self.option.add_argument("disable-gpu")
        self.option.add_argument("disable-dev-shm-usage")
        # self.option.add_experimental_option('prefs', prefs)
        self.option.add_argument('ignore-certificate-errors')
        # 防止selenuim被检测 start
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.option.add_experimental_option('useAutomationExtension', False)
        self.option.add_argument('--disable-blink-features=AutomationControlled')
        # 防止selenuim被检测 end
        # self.option.add_extension(get_chrome_proxy_extension("lum-auth-token:s3REwpSdThvEpmapxLmmtCTKWKwkbQLc@pmgr-customer-hl_6af9cb4a.zproxy.lum-superproxy.io:24000"))
        self.browser = None
        self.wait = None
        # self.browser.set_window_size(1400, 700)
        # self.browser.set_page_load_timeout(self.timeout)

    def __del__(self):
        print("del")
        if self.browser:
            self.browser.quit()
            self.browser = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        emailAddress = generate_email_address()
        # emailAddress = "zhanqiaolan985"

        print("邮箱:" + emailAddress)
        # check request upper limit
        if self.rnd_int < self.crawl_count:
            if self.browser is not None:
                self.browser.quit()
            self.browser = None
        if self.browser is None:
            self.rnd_int = random.randint(1, 2)
            d = webdriver.DesiredCapabilities.CHROME.copy()
            d['loggingPrefs'] = {'performance': 'ALL', 'server': 'ALL', 'enableNetwork': True}
            my_proxy = None
            if IP_PROXY:
                my_proxy = '127.0.0.1:24000'
            if my_proxy:
                d['proxy'] = {
                    'proxyType': 'MANUAL',
                    'httpProxy': my_proxy,
                    'ftpProxy': my_proxy,
                    'sslProxy': my_proxy,
                    'noProxy': None,
                    'class': 'org.openqa.selenium.Proxy',
                    'autodetect': False}
            print("初始化(chushihua):", self.rnd_int)
            current_directory = os.path.dirname(os.path.abspath(__file__))
            if SYS_OS == 'mac':
                self.browser = webdriver.Chrome(current_directory + '/../chromedriver', options=self.option,
                                                desired_capabilities=d)
            else:
                self.browser = webdriver.Chrome(current_directory + '/../chromedriver_linux', options=self.option,
                                                desired_capabilities=d)
            self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                       Object.defineProperty(navigator, 'webdriver', {
                           get: () => undefined
                       })
                     """
            })
            self.wait = WebDriverWait(self.browser, self.timeout)
            self.crawl_count = 0
        self.crawl_count += 1

        try:
            self.logger.info('WebDriver is Starting ' + request.url)
            self.browser.get(request.url)
            # lastName
            lastName = generate_last_name()
            lastNameInput = WebDriverWait(self.browser, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='lastName']")))
            lastNameInput.send_keys(lastName)

            time.sleep(1)
            # firstName
            firstName = generate_first_name()
            firstNameInput = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='firstName']")))
            firstNameInput.send_keys(firstName)
            time.sleep(1)

            # email
            usernameInput = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='Username']")))
            usernameInput.send_keys(emailAddress)
            time.sleep(2)

            # password
            password = generate_password()
            passwordInput = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='Passwd']")))
            passwordInput.send_keys(password)
            time.sleep(1)

            # ConfirmPasswd
            confirmPasswdInput = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='ConfirmPasswd']")))
            confirmPasswdInput.send_keys(password)
            time.sleep(2)

            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='accountDetailsNext']/div/button"))).click()
            time.sleep(4)

            out = {
                "email": emailAddress + "@gmail.com",
                "first_name": firstName,
                "last_name": lastName,
                "password": password
            }
            print(str(out))
            return TextResponse(url=request.url, body=json.dumps(out), request=request,
                                encoding='utf-8',
                                status=200)
        except TimeoutException as e:
            return scrapy.http.Request(url=request.url, dont_filter=True)



