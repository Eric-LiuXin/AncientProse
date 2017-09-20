# -*- coding: utf-8 -*-

class CrawlerPipeline(object):
    def process_item(self, item, spider):
        book = item["book"]
        with open('./test.txt', 'a') as f:
            f.write(book.title + '\n')
            f.write("-----------\n")
        for chapter in book.chapters:
            if chapter.name:
                with open('./test.txt', 'a') as f:
                    f.write(chapter.name)
            for section in chapter.sections:
                with open('./test.txt', 'a') as f:
                    f.write(section.name)
                    if section.content:
                        f.write(section.content)
                    else:
                        f.write("********************\n")
        return item
