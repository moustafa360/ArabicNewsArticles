# -*- coding: utf-8 -*-
import scrapy
from articles.items import ArticlesItem


class Youm7TechSpider(scrapy.Spider):
    name = 'youm7_tech'
    allowed_domains = ['youm7.com']
    main_link = "https://www.youm7.com"
    counter_ = 1
    scraped_link = "https://www.youm7.com/Section/علوم-و-تكنولوجيا/328/{0}"
    start_urls = [scraped_link.format(counter_)]

    def parse(self, response):
        urls = response.css("div.bigOneSec div h3 a::attr(href)").extract()
        for temp_url in urls:
            temp_url = self.main_link + temp_url  # get the full link
            if temp_url:
                yield scrapy.Request(url=temp_url, callback=self.parse_details)

        self.counter_ += 1
        next_page = self.scraped_link.format(self.counter_)

        if self.counter_ <= 1104:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_details(self, response):
        article = ArticlesItem()
        list_content = []
        clear_space_list = []
        clear_line_list = []
        final_output = []

        article["title"] = response.css("div.articleHeader h1::text").extract_first().strip()
        for i in response.css("div#articleBody p"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            for n in list_content:
                n = n.strip()
                clear_line_list.append(n)
            clear_space_list = [i.replace("\xa0", "") for i in clear_line_list]
            final_output = list(filter(None, clear_space_list))
        article["article_content"] = final_output
        article["tags"] = response.css("div.tags h3  a::text").extract()


        if article["article_content"] and len(article["tags"]) > 1:
            yield article
