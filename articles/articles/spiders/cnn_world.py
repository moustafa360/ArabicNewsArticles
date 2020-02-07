# -*- coding: utf-8 -*-
import scrapy
import json
from articles.items import CnnMiddleEastArticles


class CnnWorldSpider(scrapy.Spider):
    counter = 0
    name = 'cnn_world'
    allowed_domains = ['arabic.cnn.com']
    queryId = "queryId=c619e745d8b76a562f7539e71ed926def50910cd:SectionLoadMore"
    id = "%22%3A51%2C%22"  # A51! 51 is the id for world section in the website
    offset = "%22%3A{0}%2C%22l".format(counter)  # A0! start from the first one
    limit = "%22%3A10%7D"  # A20! scrape 20 articles
    api_url = "https://arabic.cnn.com/graphql?{0}&variables=%7B%22id{1}offset{2}limit{3}"
    start_urls = [
        api_url.format(
            queryId, id, offset, limit
        ),
    ]
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["title", "summary", "article_content"],
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

        if next_link and self.counter <= 17313: # 16510
            yield scrapy.Request(url=next_link, callback=self.parse)

    def parse_details(self, response):
        var = CnnMiddleEastArticles()
        list_content, final_output = [], []

        var["title"] = response.css("h1._2JPm2UuC56::text").extract_first().strip()
        summary = response.css("div.clearfix.wysiwyg._2A-9LYJ7eK p strong::text").extract_first().replace("\n", " ")
        if summary is None:
            summary = response.css("div.clearfix.wysiwyg._2A-9LYJ7eK p strong span::text").extract_first().replace("\n", " ")
        summary = summary.partition("(CNN)")[2] if "(CNN)" in summary else summary
        var["summary"] = summary
        for i in response.css("div.clearfix.wysiwyg._2A-9LYJ7eK p:nth-child(n+2)"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            temp1 = [i.replace("\n", " ") for i in list_content]
            temp2 = [i.replace("\r", " ") for i in temp1]
            final_output = [i.replace("\xa0", " ") for i in temp2]
        var["article_content"] = final_output
        yield var
