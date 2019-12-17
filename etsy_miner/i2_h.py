# # -*- coding: utf-8 -*-

# # Define here the models for your scraped items
# #
# # See documentation in:
# # https://doc.scrapy.org/en/latest/topics/items.html

# import scrapy
# from scrapy.pipelines.images import ImagesPipeline
# from urllib.parse import urlparse
# import os


# # 

# # class EtsyMinerItem(scrapy.Item):
# class EtsyMinerItem(ImagesPipeline):
#     # IMAGES_URLS_FIELD = 'field_name_for_your_images_urls'
#     # IMAGES_RESULT_FIELD = 'field_name_for_your_processed_images'
#     # title = scrapy.Field()
#     # image_urls = scrapy.Field()
#     # image_path = scrapy.Field()


#     def file_path(self, request, response, info):
#         return '/home/winston/mb2/data/full/' + 'yo.png'

#     # def image_key(self, url):
#     #     return self.image_path


#     # #Name download version
#     # def image_key(self, url):
#     #     image_guid = url.split('/')[-1]
#     #     return 'full/%s.jpg' % (image_guid)

#     # def get_media_requests(self, item, info):
#     #     yield Request(item['images'])

#     # def file_path(self, request, response=None, info=None):
#     #     print('\n '* 6, f'{self.image_path}.jpg')
#     #     return f'{self.image_path}.jpg'

#     # define the fields for your item here like:
#     # name = scrapy.Field()
