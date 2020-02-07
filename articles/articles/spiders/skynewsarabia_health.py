# -*- coding: utf-8 -*-
import scrapy
import json
from articles.items import CnnSportArticles

class SkynewsarabiaHealthSpider(scrapy.Spider):
    name = 'skynewsarabia_health'
    allowed_domains = ['skynewsarabia.com']
    counter = 0 # max = 3012
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["article_content", "tags"],
    }
    technology = "https://www.skynewsarabia.com/technology/"
    api_link = "https://api.skynewsarabia.com//rest/v2/topic/774401/loadMore.json?contentType=ARTICLE&idsToExclude=1296439,1296416,1296294,1296303,1296241,1296210,1296065,1295674,1295402,1295127,1294320,1249425,1037210,986638,903289,883400&offset={}&pageSize=12"
    start_urls = [api_link.format(counter)]

    def parse(self, response):
        articles = json.loads(response.text)

        # to get the link for each article we need to combine both the id and the urlFriendlySuffix in one link
        for article in range(0, len(articles["contentItems"])):
            article_id = articles["contentItems"][article]["id"]
            article_url = articles["contentItems"][article]["urlFriendlySuffix"]
            relative_link = article_id + "-" + article_url
            full_link = self.technology + relative_link
            yield scrapy.Request(url=full_link, callback=self.parse_details)

        self.counter += 12
        if self.counter <= 3012:
            next_page = self.api_link.format(self.counter)
            yield response.follow(url=next_page, callback=self.parse)


    def parse_details(self, response):
        list_content = []
        middle_east = CnnSportArticles()
        middle_east["title"] = response.css("div.sna_content_head_cont h1.sna_content_heading::text").extract_first() \
            .strip()
        for i in response.css("div.article-body div#firstBodyDiv > p:nth-child(n+1)"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            middle_east["article_content"] = list_content
            middle_east["tags"] = response.css("div.article-tags.noprint div a h2::text").extract()
        if middle_east["article_content"] and len(middle_east["tags"]) > 1:  # we need more than 2 tags at least!
            yield middle_east

