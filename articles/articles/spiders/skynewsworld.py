# -*- coding: utf-8 -*-
import scrapy
import json
from articles.items import SkyNewsEconomicArticles

class SkynewsworldSpider(scrapy.Spider):
    name = 'skynewsworld'
    allowed_domains = ['skynewsarabia.com']
    name = 'sky_news_world'
    middle_east = "https://www.skynewsarabia.com/world/"
    counter = 7700
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["title", "article_content", "tags"],
    }
    allowed_domains = ['www.skynewsarabia.com']
    scrape_this_link = "https://api.skynewsarabia.com//rest/v2/search/text.json?deviceType=DESKTOP&from=&offset=0" \
                       "&pageSize={0}&q=%D8%A3+%D8%A8+%D8%AA+%D8%AB+%D8%AC+%D8%AD+%D8%AE+%D8%AF+%D8%B0+%D8%B1+%D8%B" \
                       "2+%D8%B3+%D8%B4+%D8%B5+%D8%B6+%D8%B7+%D8%B8+%D8%B9+%D8%BA+%D9%81+%D9%82+%D9%83+%D9%84+%D9%85" \
                       "+%D9%86+%D9%87%D9%80+%D9%88+%D9%8A&section=3&showEpisodes=true&sort=DATE&supportsInfographic" \
                       "=true&to=&type=ARTICLE"
    start_urls = [scrape_this_link.format(counter)]

    def parse(self, response):
        articles = json.loads(response.text)
        # to get the link for each article we need to combine both the id and the urlFriendlySuffix in one link
        for article in range(0, len(articles["contentItems"])):
            article_id = articles["contentItems"][article]["id"]
            article_url = articles["contentItems"][article]["urlFriendlySuffix"]
            relative_link = article_id + "-" + article_url
            full_link = self.middle_east + relative_link
            yield scrapy.Request(url=full_link, callback=self.parse_details)


    @staticmethod
    def parse_details(response):
        list_content = []
        world = SkyNewsEconomicArticles()
        world["title"] = response.css("div.sna_content_head_cont h1.sna_content_heading::text").extract_first() \
            .strip()
        for i in response.css("div.article-body div#firstBodyDiv > p:nth-child(n+1)"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            world["article_content"] = list_content
            world["tags"] = response.css("div.article-tags.noprint div a h2::text").extract()
        if world["article_content"] and len(world["tags"]) >= 2:  # we need more than 2 tags at least!
            yield world