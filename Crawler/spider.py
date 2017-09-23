#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib3
from multiprocessing import Pool
from book import BookImpl
from chapter import ChapterImpl
from section import SectionImpl


class Spider:
    def __init__(self, start_urls):
        self.start_urls = start_urls
        self.http = urllib3.PoolManager()
    
    def multi_proc(self):
        books = list()
        p = Pool(processes=6)
        for start_url in self.start_urls:
            page = get_page(start_url)
            books.extend(BookImpl.parse(page))
        for book in books:
            p.apply_async(crawl, (book,))
        p.close()
        p.join()


def crawl(book):
    page = get_page(book.chapter_start_url)
    book.chapters = ChapterImpl.parse(page)
    for chapter in book.chapters:
        for section_url in chapter.section_urls:
            page = get_page(section_url)
            section = SectionImpl.parse(page)
            chapter.sections.append(section)
    book.download_logo()
    book.save_to_html()
    book.html_to_pdf()


def get_page(url):
    """
    #python 2
    return urllib2.urlopen(url).read()
    """
    """
    #python 3
    #import urllib.request
    return urllib.request.urlopen(url).read()
    """
    http = urllib3.PoolManager()
    return  http.request('GET', url).data


if __name__=="__main__":
    spider = Spider(['http://so.gushiwen.org/guwen/'])
    spider.multi_proc()
