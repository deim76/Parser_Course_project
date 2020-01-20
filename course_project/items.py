# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseProjectItem(scrapy.Item):
    _id = scrapy.Field()
    person_a = scrapy.Field()
    person_b = scrapy.Field()
    chain = scrapy.Field()
