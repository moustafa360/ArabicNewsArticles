# -*- coding: utf-8 -*-
import scrapy
import json
from articles.items import EconomicArticles


class BeinsportSpider(scrapy.Spider):
    name = 'beinsport'
    allowed_domains = ['beinsports.com']
    counter = 1
    link = 'https://www.beinsports.com/ar/news/{0}'
    start_urls = [link.format(counter)]

    custom_settings = {
        'FEED_EXPORT_FIELDS': ["title", "article_content", "tags"]
    }

    def parse(self, response):
        urls = response.css("div.content-gallery__content figcaption a::attr(href)").extract()

        for i in urls:
            yield scrapy.Request(url=i, callback=self.parse_details)

        self.counter += 1
        next_page = self.link.format(self.counter)
        yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_details(self, response):
        var = EconomicArticles()
        list_content = []
        final_output = []
        var["title"] = response.css("header.plrm h1::text").extract_first().strip()

        for i in response.css("div.plrm section p"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            clear_line_list = [i.replace("\n", " ") for i in list_content]
            clear_space_list = [i.replace("\xa0", " ") for i in clear_line_list]
            final_output = list(filter(None, clear_space_list))

        var["article_content"] = final_output
        var["tags"] = [i.strip() for i in response.css("div.plrm section a.article-tag::text").extract()]
        if len(var["tags"]) >= 1 and var["article_content"]:
            yield var