# -*- coding: utf-8 -*-
import scrapy
import json
from articles.items import CnnMiddleEastArticles


class SkyNewsMiddleEastSpider(scrapy.Spider):
    name = 'sky_news_middle_east'
    middle_east = "https://www.skynewsarabia.com/middle-east/"
    counter = 1
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["title", "article_content", "tags"],
    }
    token = "1569757712000"
    scrape_this_link = "https://api.skynewsarabia.com//rest/v2/latest.json?defaultSectionId=2&nextPageToken={0}&pageSize=20&types=ARTICLE"
    start_urls = [scrape_this_link.format(token)]

    def parse(self, response):
        articles = json.loads(response.text)

        # to get the link for each article we need to combine both the id and the urlFriendlySuffix in one link
        for article in range(0, len(articles["contentItems"])):
            article_id = articles["contentItems"][article]["id"]
            article_url = articles["contentItems"][article]["urlFriendlySuffix"]
            relative_link = article_id + "-" + article_url
            full_link = self.middle_east + relative_link
            yield scrapy.Request(url=full_link, callback=self.parse_details)

        self.token = articles["nextPageToken"]
        if self.token is not None:
            next_page = self.scrape_this_link.format(self.token)
            yield response.follow(url=next_page, callback=self.parse)


    def parse_details(self, response):
        list_content = []
        middle_east = CnnMiddleEastArticles()
        middle_east["title"] = response.css("div.sna_content_head_cont h1.sna_content_heading::text").extract_first() \
            .strip()
        for i in response.css("div.article-body div#firstBodyDiv > p:nth-child(n+1)"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            middle_east["article_content"] = list_content
            middle_east["tags"] = response.css("div.article-tags.noprint div a h2::text").extract()
        if middle_east["article_content"] and len(middle_east["tags"]) > 1:  # we need more than 2 tags at least!
            yield middle_east

