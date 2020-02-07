# -*- coding: utf-8 -*-
import scrapy
import json
from articles.items import SkyNewsEconomicArticles


class SkynewsTechSpider(scrapy.Spider):
    name = 'skynews_tech'
    tech = "https://www.skynewsarabia.com/technology/"
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["title", "article_content", "tags"],
    }
    scrape_this_link = ""
    
    start_urls = [scrape_this_link.format()]

    def parse(self, response):
        articles = json.loads(response.text)
        # to get the link for each article we need to combine both the id and the urlFriendlySuffix in one link
        for article in range(0, len(articles["contentItems"])):
            article_id = articles["contentItems"][article]["id"]
            article_url = articles["contentItems"][article]["urlFriendlySuffix"]
            relative_link = article_id + "-" + article_url
            full_link = self.tech + relative_link
            yield scrapy.Request(url=full_link, callback=self.parse_details)

    @staticmethod
    def parse_details(response):
        list_content = []
        tech = SkyNewsEconomicArticles() # have no time to change me to tech
        tech["title"] = response.css("div.sna_content_head_cont h1.sna_content_heading::text").extract_first() \
            .strip()
        for i in response.css("div.article-body div#firstBodyDiv > p:nth-child(n+1)"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            tech["article_content"] = list_content
            tech["tags"] = response.css("div.article-tags.noprint div a h2::text").extract()
        if tech["article_content"] and len(tech["tags"]) >= 2:  # we need more than 2 tags at least!
            yield tech
