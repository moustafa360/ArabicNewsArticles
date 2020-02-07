# -*- coding: utf-8 -*-
import scrapy
import json
from articles.items import CnnSportArticles


class MasrawyBusinessSpider(scrapy.Spider):
    name = 'masrawy_business'
    allowed_domains = ['masrawy.com']
    main_link = "https://www.masrawy.com"
    page_index = 1
    business = 'https://www.masrawy.com/listing/SectionMore?categoryId=206&pageIndex={}&hashTag=SectionMore'

    custom_settings = {
        'FEED_EXPORT_FIELDS': ["article_content", "tags"],
    }

    start_urls = [business.format(page_index)]

    def parse(self, response):
        urls = response.css("li.mix a::attr(href)").extract()
        for temp_url in urls:
            temp_url = self.main_link + temp_url  # get the full link
            if temp_url:
                yield scrapy.Request(url=temp_url, callback=self.parse_details)

        self.page_index += 1
        next_page = self.business.format(self.page_index)

        if self.page_index <= 297:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_details(self, response):
        var = CnnSportArticles()
        list_content, final_output = [], []
        for i in response.css("div.ArticleDetails"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            clear_line_list = [i.replace("\n", " ") for i in list_content]
            clear_space_list = [i.replace("\xa0", "") for i in clear_line_list]
            final_output = list(filter(None, clear_space_list))
        var["article_content"] = final_output
        var["tags"] = response.css("div.articleDiv div.keywordsDiv a::text").extract()
        if var["article_content"] and len(var["tags"]) > 1:
            yield var