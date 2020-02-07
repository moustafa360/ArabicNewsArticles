# -*- coding: utf-8 -*-
import scrapy
import json
from articles.items import CnnSportArticles


class SkyNewsSportsSpider(scrapy.Spider):
    name = 'sky_news_sports'

    sport = "https://www.skynewsarabia.com/sport/"
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["article_content", "tags"],
    }

    first_token = "1569690751000"
    scrape_this_link = "https://api.skynewsarabia.com//rest/v2/latest.json?defaultSectionId=6&nextPageToken={}&pageSize=20&types=ARTICLE"
    start_urls = [scrape_this_link.format(first_token)]
    urls = []

    def parse(self, response):
        articles = json.loads(response.text)

        # to get the link for each article we need to combine both the id and the urlFriendlySuffix in one link
        for article in range(0, len(articles["contentItems"])):
            article_id = articles["contentItems"][article]["id"]
            article_url = articles["contentItems"][article]["urlFriendlySuffix"]
            relative_link = article_id + "-" + article_url
            full_link = self.sport + relative_link
            self.urls.append(full_link)

        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_details)

        self.urls = []

        self.first_token = articles["nextPageToken"]
        if self.first_token is not None:
            next_page = self.scrape_this_link.format(self.first_token)
            yield response.follow(url=next_page, callback=self.parse)

    def parse_details(self, response):
        list_content = []
        sports = CnnSportArticles()
        # sports["title"] = response.css("div.sna_content_head_cont h1.sna_content_heading::text").extract_first() \
        #     .strip()
        for i in response.css("div.article-body div#firstBodyDiv > p:nth-child(n+1)"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            sports["article_content"] = list_content
            sports["tags"] = response.css("div.article-tags.noprint div a h2::text").extract()
        if sports["article_content"] and len(sports["tags"]) >= 1:  # we need more than 2 tags at least!
            yield sports
