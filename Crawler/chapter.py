#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
class Chapter:
    def __init__(self, name=None):
        self.name = name
        self.section_urls = list()
        self.sections = list()

class ChapterImpl:
    @staticmethod
    def parse(page):
        chapters = list()
        soup = BeautifulSoup(page, 'lxml')
        
        divs = soup.select('div .bookcont')
        
        for div in divs:
            if div.select('.bookMl'):
                chapter = Chapter(div.select('.bookMl')[0].get_text())
            else:
                chapter = Chapter()
            spans = div.select("span")
            for span in  spans:
                if span.select('a')[0].has_attr('href'):
                    url = "http://so.gushiwen.org%s"%(span.select('a')[0]['href'])
                    chapter.section_urls.append(url)

            chapters.append(chapter)
        return chapters
