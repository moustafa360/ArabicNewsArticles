# -*- coding: utf-8 -*-
import scrapy
from articles.items import ArticlesItem


class Youm7SportsSpider(scrapy.Spider):
    name = 'youm7_sports'
    allowed_domains = ['youm7.com']
    main_link = "https://www.youm7.com"
    counter_ = 1
    scraped_link = "https://www.youm7.com/Section/كرة-عالمية/332/{0}"
    start_urls = [scraped_link.format(counter_)]

    def parse(self, response):
        urls = response.css("div.bigOneSec div h3 a::attr(href)").extract()
        for temp_url in urls:
            temp_url = self.main_link + temp_url  # get the full link
            if temp_url:
                yield scrapy.Request(url=temp_url, callback=self.parse_details)

        self.counter_ += 1
        next_page = self.scraped_link.format(self.counter_)

        if self.counter_ <= 3139:
            yield scrapy.Request(url=next_page, callback=self.parse)

    @staticmethod
    def clean_articles(article_list_content):
        special_characters = ["\r", "\n", "\t", "\xa0"]
        cleared_list = []
        for i in article_list_content:
            for x in special_characters:
                if x in i:
                    i = i.replace(x, "")
            cleared_list.append(i.strip())
        return cleared_list

    def parse_details(self, response):
        article = ArticlesItem()
        list_content = []
        clear_line_list = []
        final_output = []

        article["title"] = response.css("div.articleHeader h1::text").extract_first().strip()
        for i in response.css("div#articleBody p"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            for _ in list_content:
                clear_line_list = self.clean_articles(list_content)
            final_output = list(filter(None, clear_line_list))
        article["article_content"] = final_output
        article["tags"] = response.css("div.tags h3  a::text").extract()

        if article["article_content"] and len(article["tags"]) > 1:
            yield article