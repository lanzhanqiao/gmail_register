# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GoogleregisterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    email = scrapy.Field()
    password = scrapy.Field()
    is_check_phone = scrapy.Field()
