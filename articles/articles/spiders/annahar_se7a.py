# -*- coding: utf-8 -*-
import scrapy
from articles.items import ArticlesItem


class AnnaharSe7aSpider(scrapy.Spider):
    name = 'annahar_se7a'
    counter = 1
    scraped_link = "https://www.annahar.com/section/{}/89-%D8%B5%D8%AD%D8%A9" # max = 203
    main_link = "https://www.annahar.com"
    start_urls = [scraped_link.format(counter)]

    custom_settings = {
        'FEED_EXPORT_FIELDS': ["article_content", "tags"],
    }

    def parse(self, response):
        urls = response.xpath('//div[@class="ias-list"]//a/@href').extract()
        for url in urls:
            article_url = self.main_link + url

            yield scrapy.Request(url=article_url, callback=self.parse_details, dont_filter=True)

        self.counter += 1
        next_page = self.scraped_link.format(self.counter)

        if self.counter <= 203:
            yield scrapy.Request(url=next_page, callback=self.parse, dont_filter=True)

    def parse_details(self, response):
        article = ArticlesItem()
        my_article = ""
        for i in response.css("div#readspeaker_maincontent p::text").extract():
            my_article += i
        article["article_content"] = my_article.replace("\n", "")
        article["tags"] = "صحة"
        my_article = ""
        yield article
