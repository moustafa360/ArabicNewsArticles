# -*- coding: utf-8 -*-
import scrapy
from articles.items import ArticlesItem


class AnnaharSe7a3amehSpider(scrapy.Spider):
    name = 'annahar_se7a_3ameh'
    counter = 1
    scraped_link = "https://www.annahar.com/section/{}/93-%D9%86%D8%B5%D8%A7%D8%A6%D8%AD"  # max =
    main_link = "https://www.annahar.com"
    start_urls = [scraped_link.format(counter)]

    def parse(self, response):
        urls = response.xpath('//div[@class="ias-list"]//a/@href').extract()
        for url in urls:
            article_url = self.main_link + url
            yield scrapy.Request(url=article_url, callback=self.parse_details, dont_filter=True)
        print("First Commect")
        self.counter += 1
        next_page = self.scraped_link.format(self.counter)

        if self.counter <= 70:

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
