# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlesItem(scrapy.Item):
    title = scrapy.Field()
    article_summary = scrapy.Field()
    article_content = scrapy.Field()
    tags = scrapy.Field()


class CnnSportArticles(scrapy.Item):
    title = scrapy.Field()
    #article_summary = scrapy.Field()
    article_content = scrapy.Field()
    tags = scrapy.Field()


class CnnMiddleEastArticles(scrapy.Item):
    title = scrapy.Field()
    article_content = scrapy.Field()
    tags = scrapy.Field()


class EconomicArticles(scrapy.Item):
    title = scrapy.Field()
    article_content = scrapy.Field()
    tags = scrapy.Field()