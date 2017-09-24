#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import codecs
import pdfkit
import urllib.request
import os
from my_sql import BookDB

class Book :
    def __init__(self, title):
        self.title = title
        self.introduce = None
        self.logo = None
        self.chapter_start_url = None
        self.chapters = list()
        self.logo_local_path = None
        self.book_start_html = '''
            <!DOCTYPE html>
                <html>
                    <head>
                        <meta charset="UTF-8">
                        <title></title>
                        <link rel="stylesheet" href="css/skin.css" />
                    </head>
                    <body>
                        <div class="main3">
                            <div class="left" style="width:1000px;">
                                <div class="sons">
                                    <div class="cont" style=" margin-top:15px;">
            '''
        self.book_end_html = '''
                                    </div>
                                </div>
                            </div>
                        </div>
                    </body>
                </html>
            '''

    def save_to_html(self):
        with codecs.open('./output/html/%s.html'%self.title, 'a', 'utf-8') as f:
            f.write(self.book_start_html)
            for chapter in self.chapters:
                if chapter.name:
                    f.write('<h1>%s</h1>'%chapter.name)
                for section in chapter.sections:
                    f.write('<h2>%s</h2>'%section.name)
                    f.write(section.content)
            f.write(self.book_end_html)
    
    def html_to_pdf(self):
        pdfkit.from_file('./output/html/%s.html'%self.title, './output/pdf/%s.pdf'%self.title)
    
    def download_logo(self):
        self.logo_local_path = './output/img/%s'%(os.path.split(self.logo)[1])
        urllib.request.urlretrieve(self.logo, self.logo_local_path)

    def upload_to_db(self):
        db = BookDB()
        db.insert(self.title, self.introduce, self.logo_local_path)


class BookImpl :
    @staticmethod
    def parse(page):
        books = list()
        soup = BeautifulSoup(page, 'lxml')
        divs = soup.select('div .cont')
        for div in divs:
            if ''.join(div.parent['class']) == 'sonspic':
                title = div.select('b')[0].get_text()
                book = Book(title)
                book.chapter_start_url = "http://so.gushiwen.org%s"%(div.select('p > a')[0]['href'])
                book.logo = div.select('img')[0]['src']
                book.introduce = div.select('p[style]')[0].get_text()
                
                books.append(book)
        return books
    