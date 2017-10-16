# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZiroomItem(scrapy.Item):

    name = scrapy.Field()
    price = scrapy.Field()
    district = scrapy.Field()
    area = scrapy.Field()
    details = scrapy.Field()
    url = scrapy.Field()
    # name = scrapy.Field()
    pass
