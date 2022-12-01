import os
import time

from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings

from googleRegister.spiders.gmail import GmailAutoRegisterSpider

if __name__ == '__main__':
    single_start_time = int(round(time.time() * 1000))
    os.environ['SCRAPY_SETTINGS_MODULE'] = f'settings'
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    data = range(3)
    print(data)
    runner.crawl(GmailAutoRegisterSpider, data=data)
    deferred = runner.join()
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()
