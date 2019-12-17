# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from w3lib.http import basic_auth_header
from etsy_miner.items import EtsyMinerItem
from pymongo import MongoClient
import hashlib
import os
from copy import deepcopy as copy

port = ''
pswd = ''
usr = ''
client = MongoClient(host='localhost', port=port, username=usr,password=pswd)
db = client['etsy']

products_db = db.products

class EtsySpider(scrapy.Spider):
    name = 'etsy'
    handle_httpstatus_list = [401]
    max_depth = 23

    allowed_domains = ['etsy.com']
    # allowed_domains = ['torproject.org']

    # start_urls = ['https://www.etsy.com/c/clothing-and-shoes?ref=catnav-10923']
    # start_urls = ['https://www.etsy.com/search?q=ring&ref=pagination&page=1']
    # start_urls = {
    #     'https://www.etsy.com/c/accessories/hair-accessories/headbands?ref=pagination&explicit=1&page=1':'Headbands & Turbans',
    #     # 'https://www.etsy.com/c/clothing-and-shoes?ref=pagination&page=1': 'Clothing & Shoes',
    # }
    start_urls = {
    # 'https://www.etsy.com/c/clothing-and-shoes?ref=pagination&page=1': 'Clothing & Shoes',
	'https://www.etsy.com/c/accessories/baby-accessories/baby-carriers-and-wraps?ref=pagination&page=1': 'Baby Carriers & Wraps',
	'https://www.etsy.com/c/accessories/baby-accessories/childrens-photo-props?ref=pagination&page=1' : "Children's Photo Props",
	'https://www.etsy.com/c/accessories/belts-and-suspenders/belt-buckles?ref=pagination&page=1' : 'Belt Buckles',
	'https://www.etsy.com/c/accessories/belts-and-suspenders/belts?ref=pagination&page=1' : 'Belts', 
	'https://www.etsy.com/c/accessories/belts-and-suspenders/suspenders?ref=pagination&page=1' : 'Suspenders', 
	'https://www.etsy.com/c/weddings/accessories/bouquets-and-corsages/bouquets?ref=pagination&page=1' : 'Bouquets',
	'https://www.etsy.com/c/accessories/bouquets-and-corsages/corsages?ref=pagination&page=1' : 'Corsages',
	'https://www.etsy.com/c/accessories/costume-accessories/capes?ref=pagination&page=1' : 'Capes', 
	'https://www.etsy.com/c/accessories/costume-accessories/costume-goggles?ref=pagination&page=1' : 'Costume Goggles',
	'https://www.etsy.com/c/accessories/costume-accessories/costume-hats-and-headpieces?ref=pagination&page=1' : 'Costume Hats & Headpieces', 
	'https://www.etsy.com/c/accessories/costume-accessories/costume-tails-and-ears?ref=pagination&page=1' : 'Costume Tails & Ears',
	'https://www.etsy.com/c/accessories/costume-accessories/costume-weapons?ref=pagination&page=1' : 'Costume Weapons',
	'https://www.etsy.com/c/accessories/costume-accessories/facial-hair?ref=pagination&page=1' : 'Facial Hair',
	'https://www.etsy.com/c/accessories/costume-accessories/masks-and-prosthetics?ref=pagination&page=1' : 'Masks & Prosthetics',
	'https://www.etsy.com/c/accessories/costume-accessories/wands?ref=pagination&page=1' : 'Wands', 
	'https://www.etsy.com/c/accessories/costume-accessories/wings?ref=pagination&page=1' : 'Wings',
	'https://www.etsy.com/c/accessories/gloves-and-mittens/arm-warmers?ref=pagination&page=1': 'Arm Warmers',
	'https://www.etsy.com/c/accessories/gloves-and-mittens/costume-gloves?ref=pagination&page=1': 'Costume Gloves',
	'https://www.etsy.com/c/accessories/gloves-and-mittens/driving-gloves?ref=pagination&page=1': 'Driving Gloves',
	'https://www.etsy.com/c/accessories/gloves-and-mittens/evening-and-formal-gloves?ref=pagination&page=1' : 'Evening & Formal Gloves', 
	'https://www.etsy.com/c/accessories/gloves-and-mittens/gardening-and-work-gloves?ref=pagination&page=1' : 'Gardening & Work Gloves', 
	'https://www.etsy.com/c/accessories/gloves-and-mittens/mittens-and-muffs?ref=pagination&page=1' : 'Mittens & Muffs',
	'https://www.etsy.com/c/accessories/gloves-and-mittens/sports-gloves?ref=pagination&page=1' : 'Sports Gloves',
	'https://www.etsy.com/c/accessories/gloves-and-mittens/winter-gloves?ref=pagination&page=1' : 'Winter Gloves',
	'https://www.etsy.com/c/accessories/hair-accessories/barrettes-and-clips?ref=pagination&page=1' : 'Barrettes & Clips', 
	'https://www.etsy.com/c/accessories/hair-accessories/bun-holders-and-makers?ref=pagination&page=1' : 'Bun Holders & Makers',
	'https://www.etsy.com/c/accessories/hair-accessories/decorative-combs?ref=pagination&page=1' : 'Decorative Combs',
	'https://www.etsy.com/c/jewelry/body-jewelry/hair-jewelry?ref=pagination&page=1' : 'Hair Jewelry',
	'https://www.etsy.com/c/accessories/hair-accessories/hair-picks?ref=pagination&page=1' : 'Hair Picks',
	'https://www.etsy.com/c/accessories/hair-accessories/hair-pins?ref=pagination&page=1' : 'Hair Pins',
	'https://www.etsy.com/c/accessories/hair-accessories/ties-and-elastics?ref=pagination&page=1': 'Ties & Elastics',
	'https://www.etsy.com/c/accessories/hair-accessories/wreaths-and-tiaras?ref=pagination&page=1' : 'Wreaths & Tiaras',
	'https://www.etsy.com/c/accessories/hand-fans?ref=pagination&page=1' : 'Hand Fans',
	'https://www.etsy.com/c/accessories/hats-and-caps/baseball-and-trucker-caps?ref=pagination&page=1' : 'Baseball & Trucker Caps',
	'https://www.etsy.com/c/accessories/hats-and-caps/berets-and-tams?ref=pagination&page=1' : 'Berets & Tams',
	'https://www.etsy.com/c/accessories/hats-and-caps/boaters-and-panama-hats?ref=pagination&page=1' : 'Boaters & Panama Hats',
	'https://www.etsy.com/c/accessories/hats-and-caps/bucket-hats?ref=pagination&page=1' : 'Bucket Hats',
	'https://www.etsy.com/c/accessories/hats-and-caps/cowboy-hats?ref=pagination&page=1' : 'Cowboy Hats',
	'https://www.etsy.com/c/accessories/hats-and-caps/earmuffs-and-ear-warmers?ref=pagination&page=1' : 'Earmuffs & Ear Warmers',
	'https://www.etsy.com/c/accessories/hair-accessories/fascinators-and-mini-hats?ref=pagination&page=1' : 'Fascinators & Mini Hats', 
	'https://www.etsy.com/c/accessories/hair-accessories/fedoras?ref=pagination&page=1' : 'Fedoras', 
	'https://www.etsy.com/c/accessories/hats-and-caps/formal-hats?ref=pagination&page=1' : 'Formal Hats',
	'https://www.etsy.com/c/accessories/hats-and-caps/hat-pins-and-stick-pins?ref=pagination&page=1' : 'Hat Pins & Stick Pins',
	'https://www.etsy.com/c/accessories/hats-and-caps/helmets/military-helmets?ref=pagination&page=1' : 'Military Helmets',
	'https://www.etsy.com/c/accessories/hats-and-caps/helmets/motorcycle-helmets?ref=pagination&page=1' : 'Motorcycle Helmets',
	'https://www.etsy.com/c/accessories/hats-and-caps/helmets/sports-helmets?ref=pagination&page=1' : 'Sports Helmets',
	'https://www.etsy.com/c/accessories/hats-and-caps/slouchy-hats?ref=pagination&page=1' : 'Slouchy Hats',
    'https://www.etsy.com/c/accessories/hair-accessories/headbands?ref=pagination&page=1':'Headbands & Turbans'
    }

    # start_urls = ['https://www.etsy.com/listing/556374294/fast-shipping-12-pieces-gold-angel-key?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sr_gallery-1-2&frs=1&col=1']
    # start_urls = ['https://check.torproject.org/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'category': copy(self.start_urls[url])})

    def __default__(self, val, defaut_val):
        return val if val else defaut_val

    def __safe_strip__(self, val, index=0):
        if val:
            return val[index].strip()
        else:
            return False

    def __safe_map__(self, num, func):
        try:
            num = func(num)
        except:
            pass
            
        return num

    def pretty_print(self, d):
        print('\n' * 2, 'dictionary starts here')
        for k in d:
            print(f'k: {k}, d[k]:{d[k]}')

        print('\n' * 2)



    def page_parse(self, response):

        link = response.url

        product_id = link.split("/")[4]

        
        title = response.xpath('//*[@id="listing-page-cart"]/div[1]/div[2]/h1/text()').extract()[0].strip()
        img_link = response.xpath('//*[@id="content"]/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/ul/li[1]/img/@src').extract()

        found = False
        tries = 0

        usr = response.xpath('//*[@id="listing-page-cart"]/div[1]/div[1]/a[1]/text()').extract()

        while (not found) and (tries < 100):
            try:
                price = response.xpath(f'//*[@id="listing-page-cart"]/div[1]/div[{tries}]/p/span[1]/text()').extract()[0].strip() 

                #For future work
                currency = ['$']
                has_currency = False
                for c in currency:
                    if c in price:
                        price = price.replace(c, '')
                        has_currency = True

                if not has_currency:
                    continue

                if '+' in price:
                    price = price.replace('+', '')
                    has_higher = True
                
                found = True

            except:
                tries += 1
        
        has_higher = False
        

        is_handmade = response.xpath('//*[@id="listing-page-cart"]/div[2]/div[1]/p/text()').extract()


        #Ratings
        product_score = response.xpath('//*[@id="listing-page-cart"]/div[1]/div[1]/a[2]/div/span/input[2]/@value').extract()

        num_ratings = response.xpath('//*[@id="listing-page-cart"]/div[1]/div[1]/a[2]/span[1]/text()').extract()
        
        best_seller = response.xpath('//*[@id="listing-page-cart"]/div[1]/div[3]/span/div/span[2]/text()').extract()


        is_handmade = self.__safe_strip__(is_handmade)
        product_score = self.__safe_strip__(product_score)
        num_ratings = self.__safe_strip__(num_ratings)
        best_seller = self.__safe_strip__(best_seller)
        usr = self.__safe_strip__(usr)

        try:
            num_ratings = num_ratings[1:-1]
        except:
            pass

        price = self.__safe_map__(price, float)
        num_ratings = self.__safe_map__(num_ratings, int)
        product_score = self.__safe_map__(product_score, int)

        comment_idx = 0
        link_id = 0

        recent_comments = {}

        comment = response.xpath(f'//*[@id="review-preview-toggle-{comment_idx}"]/div/text()').extract()
        comment_item = response.xpath(f'//*[@id="reviews"]/div/ul/li[{link_id}]/div[1]/div[2]/a/div[2]/div/span').extract()


        while comment:
            comment = comment[0].strip()
            if comment_item:
                comment_item = comment_item[0].strip()
            
            same_item = False
            if comment_item == link:
                same_item = True
            
            recent_comments[str(comment_idx)] = {'comment': comment, 'same_item':same_item}

            comment_idx += 1
            link_id += 1

            comment = response.xpath(f'//*[@id="review-preview-toggle-{comment_idx}"]/div/text()').extract()
            comment_item = response.xpath(f'//*[@id="reviews"]/div/ul/li[{link_id}]/div[1]/div[2]/a/div[2]/div/span').extract()

        if not best_seller:
            best_seller = False
        else:
            best_seller = True

        stupid_scrapy_name = f"/home/winston/mb2/data/full/{hashlib.sha1(img_link[0].encode()).hexdigest()}.jpg"

        item_data = {
            'title': title,
            'price': price,
            'username': usr,
            'has_higher': has_higher,
            'num_ratings': num_ratings,
            '_id': product_id,
            'product_score': product_score,
            'best_seller': best_seller,
            'comments': recent_comments,
            'link': link,
            'image': img_link[0],
            'category': response.meta['category'],
            'image_path': stupid_scrapy_name
            }
        
        # self.pretty_print(item_data)
        try:
            products_db.insert(item_data)
        except:
            pass

        yield EtsyMinerItem(title=title, image_urls=img_link, image_path=product_id)




    def parse(self, response):
        count = 1

        link = response.xpath(f'//*[@id="content"]/div/div[1]/div/div[3]/div[2]/div[2]/div[2]/div/ul/li[{count}]/div/a/@href').extract_first()

        link_list = response.url.split('=')
        curr_num = link_list.pop()
        page_num = int(curr_num)

        # try:
        #     yield scrapy.Request(link, callback=self.page_parse, meta={'category': response.meta['category']})
        # except:
        #     pass
        # Will when full crawler is done

        if page_num <= self.max_depth:
            while link:
                yield scrapy.Request(link, callback=self.page_parse, meta={'category': response.meta['category']})
                count +=1
                link = response.xpath(f'//*[@id="content"]/div/div[1]/div/div[3]/div[2]/div[2]/div[2]/div/ul/li[{count}]/div/a/@href').extract_first()

            # print('\n'*6, response.url ,'\n'*6 )
            # print('\n'*6, f'{response.url[:-1]}{page_num+1}', '\n' *6)

            link_list.append(str(page_num+1))

            next_page = '='.join(link_list)

            yield scrapy.Request(next_page, callback=self.parse, meta={'category': response.meta['category']})
        