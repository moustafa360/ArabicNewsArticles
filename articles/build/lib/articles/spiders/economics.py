# -*- coding: utf-8 -*-
import scrapy
import json
import re
from articles.items import EconomicArticles


class EconomicsSpider(scrapy.Spider):
    counter = 0
    name = 'middleeast'
    allowed_domains = ['arabic.cnn.com']
    queryId = "queryId=c619e745d8b76a562f7539e71ed926def50910cd:SectionLoadMore"
    id = "%22%3A4%2C%22"  # A4! 1 is the id for Economics section in the website
    offset = "%22%3A{0}%2C%22l".format(counter)  # A0! start from the first one
    limit = "%22%3A10%7D"  # A10! scrape 10 articles
    api_url = "https://arabic.cnn.com/graphql?{0}&variables=%7B%22id{1}offset{2}limit{3}"
    start_urls = [
        api_url.format(
            queryId, id, offset, limit
        ),
    ]
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["title", "article_content", "tags"],
    }

    def parse(self, response):
        data = json.loads(response.text)

        for i in range(10):
            try:
                article_type = data["data"]["list"]["items"][i]["__typename"]
                print(article_type)
            except Exception as e:
                article_type = ""
                print(str(i) + "error detected" + str(e) + "\n")
            if article_type == "NodeStory":
                relative_link = data["data"]["list"]["items"][i]["url"]["canonical"]
                if relative_link:
                    yield scrapy.Request(url=response.urljoin(relative_link), callback=self.parse_details)

        self.counter += 10
        next_list = "%22%3A{0}%2C%22l".format(self.counter)
        next_link = self.api_url.format(
            self.queryId, self.id, next_list, self.limit
        )
        if next_link and self.counter <= 5290:
            yield scrapy.Request(url=next_link, callback=self.parse)

    def parse_details(self, response):
        var = EconomicArticles()
        var["title"] = response.css("h1._2JPm2UuC56::text").extract_first().strip()
        # for the content of articles i will have to cover all the structure of the webpages

        try:
            temp = [i.rstrip() for i in response.css("div.wysiwyg p:not(div.first-child)::text").extract()]
            if len(temp) != 1:  # if it has "" only!
                var["article_content"] = self.clear_input(temp)

            elif not var["article_content"] and len(temp) != 1:
                temp = [i.rstrip() for i in response.css("div.wysiwyg p:not(:first-child) > strong > span > span > span"
                                                         " > span > span > span > span > span::text").extract()]
                var["article_content"] = self.clear_input(temp)

            elif not var["article_content"] and len(temp) != 1:
                temp = [i.rstrip() for i in
                        response.css("div.wysiwyg p:not(:first-child) > span > span > span > span > span > span > span "
                                     "> span::text").extract()]
                var["article_content"] = self.clear_input(temp)

            elif not var["article_content"] and len(temp) != 1:
                temp = [i.rstrip() for i in
                        response.css("div.wysiwyg p:not(:first-child)> span > span > span > span > span > "
                                     "span:nth-child(3) > span > span::text").extract()]
                var["article_content"] = self.clear_input(temp)

            elif not var["article_content"] and len(temp) != 1:
                temp = [i.rstrip() for i in
                        response.css("div.wysiwyg p:not(:first-child)> span > span > span > span > span > "
                                     "span:nth-child(2) > span > span::text").extract()]
                var["article_content"] = self.clear_input(temp)

            elif not var["article_content"] and len(temp) != 1:
                temp = [i.rstrip() for i in response.css("div.wysiwyg._2A-9LYJ7eK p::text").extract()]
                var["article_content"] = self.clear_input(temp)
            else:
                var["article_content"] = "you did not cover this case."

            var["tags"] = [i.strip() for i in response.css("ul.AsCeVPiOdE li a::text").extract()]
            if var["tags"] and var["article_content"]:  # do not save any article that has neither tag nor content!
                yield var

        except KeyError as e:
            print(e)

    @staticmethod
    def clear_input(my_list):
        """Clear all the inputs from having the "\n" in the context itself, using rstip is useless for this case"""
        for i in range(0, len(my_list)):
            if "\n" in my_list:
                del my_list  # I am seeking a good output for god sake!
        return my_list

