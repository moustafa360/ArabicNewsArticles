# -*- coding: utf-8 -*-
import scrapy
from articles.items import EconomicArticles


class RtSportsSpider(scrapy.Spider):
    name = 'cnbc_business'
    counter = 1
    allowed_domains = ['www.cnbcarabia.com']
    main_link = "https://www.cnbcarabia.com"
    scraped_link = "https://www.cnbcarabia.com/news/latest?page={0}"
    start_urls = [scraped_link.format(counter)]

    def parse(self, response):
        urls = response.css("div.blog-box-title a::attr(href)").extract()

        for temp_url in urls:
            temp_url = self.main_link + temp_url  # get the full link
            if temp_url:
                yield scrapy.Request(url=temp_url, callback=self.go_here)

        self.counter += 1
        next_page = self.scraped_link.format(self.counter)

        if self.counter <= 1400:
            yield scrapy.Request(url=next_page, callback=self.parse)

    @staticmethod
    def go_here(response):
        rt = EconomicArticles()
        list_content = []
        clear_space_list  = []
        clear_line_list = []
        final_output = []
        rt["title"] = response.css("div.article-title h1::text").extract_first()
        for i in response.css("div.article-content p"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            clear_line_list = [i.replace("\n", " ") for i in list_content]
            clear_space_list = [i.replace("\xa0", "") for i in clear_line_list]
            final_output = list(filter(None, clear_space_list))

        rt["article_content"] = final_output
        rt["tags"] = response.css("div.blog-box-tags a::text").extract()
        if rt["article_content"] and len(rt["tags"]) >= 1:
            yield rt
