# -*- coding: utf-8 -*-
import scrapy
from articles.items import CnnSportArticles

class Arab48TechSpider(scrapy.Spider):
    name = 'arab48_tech'
    counter = 1
    main_link = "https://www.arab48.com"
    link = "https://www.arab48.com/%D8%B9%D9%84%D9%88%D9%85-%D9%88%D8%AA%D9%83%D9%86%D9%88%D9%84%D9%88%D8%AC%D9%8A%D8%A7/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D9%84%D8%AA%D9%83%D9%86%D9%88%D9%84%D9%88%D8%AC%D9%8A%D8%A7?page={}"
    allowed_domains = ['arab48.com']
    start_urls = [link.format(0)]

    custom_settings = {
        'FEED_EXPORT_FIELDS': ["title", "article_content", "tags"],
    }

    def parse(self, response):
        urls = response.css("div.blockquote-box.clearfix a::attr(href)").extract()
        for url in urls:
            next_link = self.main_link + url
            if next_link:
                yield scrapy.Request(url=next_link, callback=self.parse_details)

        self.counter += 1
        next_page = self.link.format(self.counter)

        if next_page and self.counter <= 40:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_details(self, response):
        list_content= []
        clear_space_list = []

        cnbc = CnnSportArticles()
        cnbc["title"] = response.css("h1.blog-post-title::text").extract_first().strip()

        for i in response.css("div#articleText p:nth-child(n+2)"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            clear_line_list = [i.replace("\n", " ") for i in list_content]
            clear_space_list = [i.replace("\xa0", " ") for i in clear_line_list]

        for i in range(0, len(clear_space_list)):
            if "اقرأ" in clear_space_list[i]:
                del clear_space_list[i]

        cnbc["article_content"] = clear_space_list

        tags = response.css("div.articleTags div.tagDev a::text").extract()
        a = " , ".join(tags).replace("#", "")
        cnbc["tags"] = a
        if len(cnbc["tags"]) >= 2 and cnbc["article_content"]:
            yield cnbc
