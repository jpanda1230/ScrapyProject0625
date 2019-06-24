# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class CommunityItem(scrapy.Item):
     # REQUIRED FIELDS

    title = Field()
    datefrom = Field()
    starttime = Field()
    eventwebsite = Field()
    description = Field()
    id = Field()  # This field should be located in every and each scraper! Just insert it and leave it empty = ""!
    organization = Field()  # This field should contain the name of the organization that is hosting the event! CAN BE HARD-CODED!
    location =Field()
    address = Field()
    city = Field()
    state = Field()

    pass

