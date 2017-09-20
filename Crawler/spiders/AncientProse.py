# -*- coding: utf-8 -*-
import scrapy


class AncientproseSpider(scrapy.Spider):
    name = 'AncientProse'
    allowed_domains = ['so.gushiwen.org']
    start_urls = ['http://so.gushiwen.org/']

    def parse(self, response):
        pass
