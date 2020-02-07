# -*- coding: utf-8 -*-
import scrapy
import json
from articles.items import ArticlesItem


class CnnArabiaHealthSpider(scrapy.Spider):
    counter = 0
    name = 'cnn_arabia_health'
    allowed_domains = ['arabic.cnn.com']
    queryId = "queryId=e6e34965a2a7b4908b069ca0360aef987abd2187:SectionLoadMore"
    id = "%22%3A7%2C%22"  # A7! 1 is the id for health section in the website
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

        if next_link and self.counter <= 2210:  # 5470
            yield scrapy.Request(url=next_link, callback=self.parse)

    def parse_details(self, response):
        var = ArticlesItem()
        list_content = []
        final_output = []
        var["title"] = response.css("h1._2JPm2UuC56::text").extract_first().strip()
        for i in response.css("div.clearfix.wysiwyg._2A-9LYJ7eK p:nth-child(n+2)"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            final_output = [i.replace("\n", " ") for i in list_content]

        var["article_content"] = final_output
        var["tags"] = [i.strip() for i in response.css("ul.AsCeVPiOdE li a::text").extract()]
        if len(var["tags"]) >= 1 and var["article_content"]:  # do not save any article that has neither tag nor content!
            yield var