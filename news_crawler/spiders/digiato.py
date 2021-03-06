# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class DigiatoSpider(scrapy.Spider):
    name = 'digiato'
    allowed_domains = ['digiato.com']
    start_urls = ['https://digiato.com/topic/mobile/',
                  #   'https://digiato.com/topic/business/',
                  #   'https://digiato.com/topic/game/',
                  #   'https://digiato.com/topic/science/',
                  ]
    labels = ['mobile', 'business', 'game', 'science']

    def parse(self, response):
        label = self.find_label(response.url)
        articles = response.css('article a')
        unique_links = []
        for article in articles:
            link = article.css('a::attr(href)').get()
            title = article.css('a::text').get()
            if title is not ' ' and link not in unique_links:
                unique_links.append(link)
                yield {
                    'title': title,
                    'url': link,
                    'label': label,
                    'source': self.name,
                }

        next_page = response.css('.next-page > a::attr(href)').get()
        if next_page:
            print(f'found next page. crawling {next_page}')
            yield Request(
                url=next_page,
                callback=self.parse,
            )

    def find_label(self, url):
        for label in self.labels:
            if label in url:
                return label
        return 'unknown'
