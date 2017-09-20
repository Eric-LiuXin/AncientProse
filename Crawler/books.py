# -*- coding: utf-8 -*-

class Book:
    def __init__(self, title):
        self.title = title
        self.introduce = None
        self.logo = None
        self.chapters = list()

class Chapter:
    def __init__(self, name=None):
        self.name = name
        self.sections = list()

class Section:
    def __init__(self, name=None):
        self.name = name
        self.content = None
