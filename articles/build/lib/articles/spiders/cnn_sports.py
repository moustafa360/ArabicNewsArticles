# -*- coding: utf-8 -*-
import scrapy
import json
from articles.items import CnnSportArticles


class CnnSportsSpider(scrapy.Spider):
    counter = 0
    article_type = ""
    name = 'cnn_sports'
    allowed_domains = ['arabic.cnn.com']
    # https://arabic.cnn.com/graphql?queryId=c619e745d8b76a562f7539e71ed926def50910cd:SectionLoadMore&variables=%7B%22id%22%3A5%2C%22offset%22%3A0%2C%22limit%22%3A20%7D
    queryId = "queryId=c619e745d8b76a562f7539e71ed926def50910cd:SectionLoadMore"
    id = "%22%3A5%2C%22"  # A5! 5 is the id for sport section in the website
    offset = "%22%3A{0}%2C%22l".format(counter)  # A0! start from the first one
    limit = "%22%3A10%7D"  # A20! scrape 20 articles
    api_url = "https://arabic.cnn.com/graphql?{0}&variables=%7B%22id{1}offset{2}limit{3}"
    start_urls = [
        api_url.format(
            queryId, id, offset, limit
        ),
    ]
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["title", "article_content", "tags"],
    }
    # this list has some of the articles that have weird structure
    blocked_list = [
        "/sport/article/2018/10/03/egypt-federation-hazem-emam",
        "/sport/article/2018/09/10/iraq-algeria-saddam-hussein"
    ]

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
                if relative_link in self.blocked_list:
                    break
                yield scrapy.Request(url=response.urljoin(relative_link), callback=self.parse_details)

        self.counter += 10
        next_list = "%22%3A{0}%2C%22l".format(self.counter)
        next_link = self.api_url.format (
            self.queryId, self.id, next_list, self.limit
        )
        if next_link and self.counter <= 810:
            yield scrapy.Request(url=next_link, callback=self.parse)

    def parse_details(self, response):
        let = CnnSportArticles()
        let["title"] = response.css("h1._2JPm2UuC56::text").extract_first().strip()
        temp = [i.rstrip() for i in response.css("div.wysiwyg p:not(div.first-child)::text").extract()]
        if len(temp) != 1:  # if it has "" only!
            let["article_content"] = self.clear_input(temp)

        elif not let["article_content"]:
            temp = [i.rstrip()for i in response.css("div.wysiwyg p:not(:first-child)  > strong > "
                        "span > span > span > span > span > span > span > span::text").extract()]
            let["article_content"] = self.clear_input(temp)
        elif not let["article_content"]:
            temp = [i.rstrip() for i in response.css("div.wysiwyg p:not(:first-child) > span "
                                                    "> span > span > span > span > span > span > span::text").extract()]
            let["article_content"] = self.clear_input(temp)

        elif not let["article_content"]:
            temp = [i.rstrip() for i in response.css("div.clearfix.wysiwyg._2A-9LYJ7eK p::text").extract()]
            let["article_content"] = self.clear_input(temp)
        else:
            let["article_content"] = "you did not cover this case."

        let["tags"] = [i.strip() for i in response.css("ul.AsCeVPiOdE li a::text").extract()]
        if let["tags"] and let["article_content"]:  # do not scrape the article that has neither tag nor content!
            yield let

    @staticmethod
    def clear_input(my_list):
        for i in range(0, len(my_list)):
            if "\n" in my_list:
                my_list[i].replace("\n", " ")
        return my_list
