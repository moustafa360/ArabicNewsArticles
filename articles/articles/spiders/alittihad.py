# -*- coding: utf-8 -*-
import scrapy
from articles.items import CnnSportArticles


class AlittihadSpider(scrapy.Spider):
    name = 'alittihad'
    counter = 1
    main_link = "https://www.alittihad.ae"
    allowed_domains = ['www.alittihad.ae']
    scraped_link = "https://www.alittihad.ae/Service/SectionNews.aspx?SectionID=51&pageSize=8&pageindex={0}"
    start_urls = [scraped_link.format(counter)]

    custom_settings = {
        'FEED_EXPORT_FIELDS': ["title", "article_content", "tags"],
    }

    def parse(self, response):
        urls = response.css("div.classic-grid-itm h3 a::attr(href)").extract()

        for url in urls:
            next_link = self.main_link + url
            if next_link:
                yield scrapy.Request(url= next_link, callback=self.parse_details)

        self.counter += 1
        next_page = self.scraped_link.format(self.counter)

        if next_page and self.counter <= 1818:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_details(self, response):
        cnbc = CnnSportArticles()
        list_content = []
        final_output = []
        cnbc["title"] = response.css("header h1::text").extract_first().strip()

        for i in response.css("div.article-content-editor p:nth-child(n+2)"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            clear_line_list = [i.replace("\n", " ") for i in list_content]
            clear_space_list = [i.replace("\xa0", " ") for i in clear_line_list]
            clear_rlm = [i.replace("\u200f", " ") for i in clear_space_list]
            final_output = list(filter(None, clear_rlm))

        cnbc["article_content"] = final_output
        cnbc["tags"] = response.css("div.article-tags a::text").extract()
        if len(cnbc["tags"]) > 2 and cnbc["article_content"]:
            yield cnbc