# -*- coding: utf-8 -*-
import scrapy
from articles.items import ArticlesItem


class SkynewsSpider(scrapy.Spider):
    name = 'skynews'
    allowed_domains = ['www.skynewsarabia.com']
    start_urls = ['https://www.skynewsarabia.com/sport/latest-news-%D8%A2%D8%AE%D8%B1-%D8%A7%D9%84%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1']
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["title", "article_summary", "article_content", "tags"],
    }

    # this function will be called automatically by Scrapy
    def parse(self, response):
        # get the urls of each article
        urls = response.css("a.item-wrapper::attr(href)").extract()
        # for each article make a request to get the text of that article
        for url in urls:
            # get the info of that article using the parse_details function
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_details)
        # go and get the link for the next article
        next_article = response.css("a.item-wrapper::attr(href)").get()
        if next_article:
            yield scrapy.Request(url=response.urljoin(next_article), callback=self.parse)

    def parse_details(self, response):
        vars = ArticlesItem()
        vars["title"] = response.css("h1.sna_content_heading::text").extract_first().strip()
        vars["article_summary"] = response.css("span.article-summary::text").extract_first().strip()
        vars["article_content"] = [i.strip() for i in response.css("div.article-body p::text").extract()]
        vars["tags"] = [i.strip() for i in response.css("div.article-tags h2.tags::text").extract()]
        yield vars