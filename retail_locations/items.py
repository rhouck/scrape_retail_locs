# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RetailLocationsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    business_name = scrapy.Field()
    street_address = scrapy.Field()
    address_locality = scrapy.Field()
    address_region = scrapy.Field()
    postal_code = scrapy.Field()
