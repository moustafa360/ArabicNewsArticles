# -*- coding: utf-8 -*-
import scrapy
from articles.items import ArticlesItem

class ThemenatechSpider(scrapy.Spider):
    name = 'themenatech'
    allowed_domains = ['themenatech.com']
    counter = 1
    scraped_link = "https://www.themenatech.com/category/أخبار-التقنية/page/{}/"
    start_urls = [scraped_link.format(counter)]

    def parse(self, response):
        urls = response.css("article h2.title a::attr(href)").extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_details)

        self.counter += 1
        next_page = self.scraped_link.format(self.counter)
        if self.counter <= 1496:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_details(self, response):
        article = ArticlesItem()
        list_content, final_output = [], []
        article["title"] = response.css("h1.single-post-title span.post-title::text").extract_first()
        for i in response.css("div.entry-content p"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            clear_line_list = [i.replace("\n", " ") for i in list_content]
            clear_space_list = [i.replace("\xa0", "") for i in clear_line_list]
            final_output = list(filter(None, clear_space_list))
        article["article_content"] = final_output
        article["tags"] = [i.strip() for i in response.css("div.entry-terms a::text").extract()]
        if len(article["article_content"]) > 5 and len(article["tags"]) >= 1:
            yield article
