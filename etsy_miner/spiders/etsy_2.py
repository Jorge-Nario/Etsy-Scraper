# -*- coding: utf-8 -*-
import scrapy


class EtsySpider(scrapy.Spider):
    name = 'etsy2'
    allowed_domains = ['etsy.com']
    start_urls = ['https://www.etsy.com/listing/735065856/snowflake-quilt-paper-pattern-by-modern?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=scrapy&ref=sr_gallery-1-11&cns=1']
    start_urls = ['https://www.etsy.com/search?q=quilt&ref=pagination&page=1']
# response.xpath('//*[@id="content"]/div/div[1]/div/div/div[3]/div[2]/div[3]/div/ul/li[11]/div/a')


    def parse(self, response):
        page = response.url.split("/")[-2]
        link = response.xpath('//*[@id="content"]/div/div[1]/div/div/div[3]/div[2]/div[3]/div/ul/li[8]/div/a/@href').extract()[0]

        #after link
        name = response.xpath('//*[@id="listing-page-cart"]/div[1]/div[2]/h1/text()')[0].extract().strip()
        
        yield {
            'name':name
        }
