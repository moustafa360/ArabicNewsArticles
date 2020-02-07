# -*- coding: utf-8 -*-
import scrapy
from articles.items import ArticlesItem


class RtSportsEspSpider(scrapy.Spider):
    name = 'rt_sports_esp'
    allowed_domains = ['arabic.rt.com']
    counter_ = 0
    scraped_link = "https://arabic.rt.com/listing/trend.53b3df9e611e9b8e648b45c9/noprepare/trend/10/{0}"
    main_link = "https://arabic.rt.com"
    start_urls = [scraped_link.format(counter_)]

    def parse(self, response):
        urls = response.css("a.heading::attr(href)").extract()
        for temp_url in urls:
            temp_url = self.main_link + temp_url  # get the full link
            if temp_url:
                yield scrapy.Request(url=temp_url, callback=self.parse_details)

        self.counter_ += 1
        next_page = self.scraped_link.format(self.counter_)

        if self.counter_ <= 99:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_details(self, response):
        article = ArticlesItem()
        list_content = []
        clear_space_list = []
        clear_line_list = []
        final_output = []
        article["title"] = response.css("div.article h1.heading::text").extract_first()
        for i in response.css("div.text.js-text.js-mediator-article p:not(:first-child):not(:last-child)"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            clear_line_list = [i.replace("\n", " ") for i in list_content]
            clear_space_list = [i.replace("\xa0", "") for i in clear_line_list]
            final_output = list(filter(None, clear_space_list))
            if len(final_output) > 2:
                del final_output[-1]
        article["article_content"] = final_output
        article["tags"] = response.css("div.news-tags.news-tags_article a::text").extract()
        if article["article_content"] and len(article["tags"]) > 1:
            yield article