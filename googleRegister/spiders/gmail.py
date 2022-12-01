import json

from scrapy import Selector, Spider, Request

from googleRegister.items import GoogleregisterItem


class GmailAutoRegisterSpider(Spider):
    name = 'gmailAutoRegister'
    base_url = 'https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp'
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    def __init__(self, data=None, pn=None, *args, **kwargs):
        self.data = data

    def start_requests(self):
        nums = self.data
        for index in nums:
            yield Request(url=self.base_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print("wordpress selenium parse")
        print(self.name + ":" + "response text:" + response.text)
        s = response.text.replace("'", "\"")
        print("处理后的数据:" + s)
        result = json.loads(s)
        email_item = GoogleregisterItem()
        email_item['first_name'] = result['first_name']
        email_item['last_name'] = result['last_name']
        email_item['email'] = result['email']
        email_item['password'] = result['password']
        return email_item
