# -*- coding: utf-8 -*-
import scrapy
import json
from articles.items import SkyNewsEconomicArticles


class SkyNewsSportsSpider(scrapy.Spider):
    """this script can scrape up to 4153 articles from the economics category from the sky news arabic website"""
    name = 'sky_news_economic'
    business = "https://www.skynewsarabia.com/business/"
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["title", "article_content", "tags"],
    }
    token = "1569574621000"
    scrape_this_link = "https://api.skynewsarabia.com//rest/v2/latest.json?defaultSectionId=4&nextPageToken={0}&pageSize=20&types=ARTICLE"
    start_urls = [scrape_this_link.format(token)]

    def parse(self, response):
        articles = json.loads(response.text)
        # to get the link for each article we need to combine both the id and the urlFriendlySuffix in one link
        for article in range(0, len(articles["contentItems"])):
            article_id = articles["contentItems"][article]["id"]
            article_url = articles["contentItems"][article]["urlFriendlySuffix"]
            relative_link = article_id + "-" + article_url
            full_link = self.business + relative_link
            yield scrapy.Request(url=full_link, callback=self.parse_details)

        self.token = articles["nextPageToken"]
        if self.token is not None:
            next_page = self.scrape_this_link.format(self.token)
            yield response.follow(url=next_page, callback=self.parse)

    @staticmethod
    def parse_details(response):
        list_content = []
        economics = SkyNewsEconomicArticles()
        economics["title"] = response.css("div.sna_content_head_cont h1.sna_content_heading::text").extract_first()\
            .strip()
        for i in response.css("div.article-body div#firstBodyDiv > p:nth-child(n+1)"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
        economics["article_content"] = list_content
        economics["tags"] = response.css("div.article-tags.noprint div a h2::text").extract()
        if economics["article_content"] and len(economics["tags"]) >= 2:  # we need more than 2 tags at least!
            yield economics
