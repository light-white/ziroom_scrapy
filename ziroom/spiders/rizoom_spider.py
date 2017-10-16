# -*- coding: utf-8 -*-
import scrapy
import json
import copy
import re

from scrapy.selector import Selector
from scrapy.http import Request
from ziroom.items import ZiroomItem
from scrapy.spiders import Spider, Rule
from scrapy.linkextractors import LinkExtractor

class ZiroomSpider(Spider):

    name = 'ziroom'

    start_urls = [
        'http://www.ziroom.com/z/nl/z2.html',
    ]

    def parse(self, response):
        sel = Selector(response)
        nodes = sel.xpath(".//*[@class='clearfix zIndex6']//*[@class='clearfix filterList']/li/*[@class='tag']/a")

        for node in nodes:
            metadata = {}
            metadata['district'] = node.xpath('./text()').extract()[0]
            href = node.xpath('./@href').extract()[0]
            if href[0]!='h':
                href = 'http:'+href
            yield Request(
                url=href,
                callback=self.parse_district,
                meta={'userdata': metadata},
            )

    def parse_district(self, response):
        metadata = response.meta['userdata']
        sel = Selector(response)
        nodes = sel.xpath(".//*[@class='active2']/../../div[@class='con']/*/a")

        for node in nodes:
            m = copy.deepcopy(metadata)
            m['area'] = node.xpath('./text()').extract()[0]
            href = node.xpath('./@href').extract()[0]
            if href[0]!='h':
                href = 'http:'+href
            yield Request(
                url=href,
                callback=self.parse_area,
                meta={'userdata': m},
            )

    def parse_area(self, response):
        metadata = response.meta['userdata']
        sel = Selector(response)
        nodes = sel.xpath(".//*[@class='pages']/a[not(@class)]")

        for node in nodes:
            m = copy.deepcopy(metadata)
            href = node.xpath('./@href').extract()[0]
            if href[0]!='h':
                href = 'http:'+href
            yield Request(
                url=href,
                callback=self.parse_area_list,
                meta={'userdata': m},
            )

    def parse_area_list(self, response):
        metadata = response.meta['userdata']
        sel = Selector(response)
        nodes = sel.xpath(".//*[@id='houseList']/li/*[@class='img pr']/a")

        for node in nodes:
            m = copy.deepcopy(metadata)
            href = node.xpath('./@href').extract()[0]
            if href[0]!='h':
                href = 'http:'+href
            yield Request(
                url=href,
                callback=self.parse_room,
                meta={'userdata': m},
            )

    def parse_room(self, response):
        metadata = response.meta['userdata']
        sel = Selector(response)

        name = sel.xpath(".//*[@class='room_name']/h2/text()").extract()[0].replace(' ', '').replace('\n', '')
        price = sel.xpath(".//*[@id='room_price']/text()").extract()[0]
        details = {}
        detail_nodes = sel.xpath(".//*[@class='detail_room']/li[not(@class)]/text()").extract()
        for node in detail_nodes:
            node = node.replace(' ', '').replace('\n', '')
            if node:
                node = node.split('：')
                details[node[0]] = node[1]

        item = ZiroomItem()
        item['url'] = response.url
        item['name'] = name
        item['price'] = price
        item['district'] = metadata['district']
        item['area'] = metadata['area']
        item['details'] = details

        yield item
