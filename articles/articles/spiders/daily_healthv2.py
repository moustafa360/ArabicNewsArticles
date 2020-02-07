# -*- coding: utf-8 -*-
import scrapy
from articles.items import ArticlesItem


class DailyHealthv2Spider(scrapy.Spider):
    name = 'daily_healthv2'
    allowed_domains = ['news.dailymedicalinfo.com']
    counter = 1
    scraped_link = "https://news.dailymedicalinfo.com/page/{}/"
    start_urls = [scraped_link.format(counter)]

    custom_settings = {
        'FEED_EXPORT_FIELDS': ["article_content", "tags"],
    }

    def parse(self, response):
        urls = response.css("a.post-thumbnail::attr(href)").extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_details)
        print("First Debugger")
        self.counter += 1
        next_page = self.scraped_link.format(self.counter)

        if self.counter <= 214:

            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_details(self, response):
        article = ArticlesItem()
        list_content = []
        my_article = ""
        article["title"] = response.css("h1.dmi-title::text").extract_first()
        for i in response.css("div.dmi-entry-content p::text").extract():
            if len(i) > 20:
                my_article += i
        article["article_content"] = my_article.replace("\xa0", "")
        article["tags"] = "صحة"
        my_article = ""
        if len(article["article_content"]) > 20:
            yield article
