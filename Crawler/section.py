#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
from bs4 import BeautifulSoup
class Section:
    def __init__(self, name):
        self.name = name
        self.content = None

class SectionImpl:
    @staticmethod
    def parse(page):
        soup = BeautifulSoup(page, 'lxml')
        name = soup.select('h1')[0].get_text()
        section = Section(re.sub(r'\s.*$', "", name))
        section.content = soup.select('div .contson')[0].prettify()
        return section