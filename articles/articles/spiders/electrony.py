# -*- coding: utf-8 -*-
import scrapy
from articles.items import ArticlesItem


class ElectronySpider(scrapy.Spider):
    name = 'electrony'
    allowed_domains = ['electrony.net']
    counter = 1
    scraped_link = "https://www.electrony.net/page/{}/"
    start_urls = [scraped_link.format(counter)]

    def parse(self, response):
        urls = response.css("div#content article div.ft-bpost a::attr(href)").extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_details)

        self.counter += 1
        next_page = self.scraped_link.format(self.counter)
        if self.counter <= 3794:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_details(self, response):
        article = ArticlesItem()
        list_content = []
        my_article = ""
        article["title"] = response.css("h1.ft-ptitle::text").extract_first()
        for i in response.css("section.ft-entry p::text").extract():
            if len(i) > 20:
                my_article += i
        article["article_content"] = my_article.replace("\xa0", "")
        article["tags"] = [i.strip() for i in response.css("div.ft-ptags a::text").extract()]
        my_article = ""
        if len(article["article_content"]) > 20 and len(article["tags"]) >= 1:
            yield article
