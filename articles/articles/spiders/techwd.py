# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime, timedelta
from articles.items import ArticlesItem
import requests


class HiamagtestingSpider(scrapy.Spider):
    name = 'techwd'
    main_path = 'https://www.tech-wd.com/wd/{0}/{1}/{2}/'# 0 = year, 1 = month, 2 = day
    allowed_domains = ['tech-wd.com']
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["title", "article_content", "tags"]
    }
    # today is 2019/04/24 ! let's start scraping!
    # Last Date to be Scrapped 2008/03/25/ I checked that manually xD
    # End Date 2011/10/03
    year_counter = 2019
    month_counter = 4
    day_counter = 25
    start_date = "{0}/{1}/{2}".format(year_counter, month_counter, day_counter)
    start_urls = [main_path.format(year_counter, month_counter, day_counter)]

    def parse(self, response):
        # get all the links and send them to the parse_details func to scrape their content!
        urls = response.css("h3.thumb-title a::attr(href)").extract()
        for url in urls:
            if url:
                yield scrapy.Request(url=url, callback=self.parse_details)

        self.decrease_one_day(self.start_date)
        # temp_date = "/".join(self.decrease_one_day(self.start_date))
        next_page = self.main_path.format(self.year_counter, self.month_counter, self.day_counter)

        if next_page and self.year_counter >= 2009:
            check_response = requests.get(next_page)
            if check_response.status_code == 200:  # to avoid being redirected 25/12/2018
                # if not self.year_counter <= str(2008) and not self.month_counter <= str(3) and not self.day_counter <= str(25):
                yield scrapy.Request(url=next_page, callback=self.parse)
            elif check_response.status_code != 200:
                self.decrease_one_day(self.start_date)
                next_page = self.main_path.format(self.year_counter, self.month_counter, self.day_counter)
                yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_details(self, response):
        article = ArticlesItem()
        list_content = []
        clear_space_list = []
        clear_line_list = []
        final_output = []
        article["title"] = response.css("h1.post-title.entry-title::text").extract_first().strip()
        for i in response.css("div.entry-content p"):
            list_content.append("".join(i.xpath('descendant-or-self::text()').extract()))
            clear_line_list = [i.replace("\n", " ") for i in list_content]
            clear_space_list = [i.replace("\xa0", "") for i in clear_line_list]
            final_output = list(filter(None, clear_space_list))

        article["article_content"] = final_output
        article["tags"] = response.css("span.tagcloud a::text").extract()
        if len(article["tags"]) >= 2 and article["article_content"]:
            yield article

    def decrease_one_day(self, date):
        start = date
        start = datetime.strptime(start, "%Y/%m/%d")
        end = start - timedelta(days=1)
        # delete time 00:00:00 and just keep the date
        new_date = str(end)
        new_date = new_date[:10]
        date_list = new_date.split("-")
        self.start_date = "/".join(date_list)
        self.year_counter = int(date_list[0])
        self.month_counter = int(date_list[1])
        self.day_counter = int(date_list[2])
        #return date_list