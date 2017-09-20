import scrapy
from Crawler.items import AncientProseItem
from Crawler.books import Book
from Crawler.books import Chapter
from Crawler.books import Section

class AncientProseSpider(scrapy.Spider):
    name = 'AncientProse'
    allowed_domains = ['so.gushiwen.org']
    #url = 'http://so.gushiwen.org/guwen/Default.aspx?p='
    #start_urls = [url + str(i) for i in range(1,30)]
    start_urls = ['http://so.gushiwen.org/guwen/Default.aspx?p=1', 'http://so.gushiwen.org/guwen/Default.aspx?p=2']


    def parse(self, response):
        divs = response.xpath('//div[@class = "sonspic"]/div[@class = "cont"]')
        for div in divs:
            book = Book(''.join(div.xpath('.//b/text()').extract()))
            book.logo = ''.join(div.xpath('.//div[@class = "divimg"]/a/img/@src').extract())

            chapter_url = ''.join(div.xpath('.//div[@class = "divimg"]/a/@href').extract())
            if chapter_url:
                url = "http://so.gushiwen.org%s"%(chapter_url)
                yield scrapy.Request(url = url,meta={'book':book}, callback=self.chapter_parse)

    def chapter_parse(self, response):
        book = response.meta['book']
        divs = response.xpath('//div[@class = "bookcont"]')
        for div in divs:
            chapter_name = ''.join(div.xpath('.//div/strong/text()').extract())
            if chapter_name:
                chapter = Chapter(chapter_name)
            else:
                chapter = Chapter()
            book.chapters.append(chapter)
            spans = div.xpath('.//span')
            for span in spans:
                section = Section(''.join(span.xpath('.//a/text()').extract()))
                section_url = ''.join(span.xpath('.//a/@href').extract())
                chapter.sections.append(section)
                if section_url:
                    url = "http://so.gushiwen.org%s"%(section_url)
                    yield scrapy.Request(url = url,meta={'book':book, 'section':section}, callback=self.content_parse)

    def content_parse(self, response):
        item = AncientProseItem()
        item['book'] = response.meta['book']
        section = response.meta['section']
        section.content = ''.join(response.xpath('//div[@class = "contson"]').extract())
        return item
