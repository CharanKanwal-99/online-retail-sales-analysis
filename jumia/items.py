# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JumiaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    crawled_at = scrapy.Field()
    name = scrapy.Field()
    href = scrapy.Field()
    data_id = scrapy.Field()
    brand = scrapy.Field()
    name2 = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    discount = scrapy.Field()
    votes = scrapy.Field()
    stars = scrapy.Field()
    image_url = scrapy.Field()
    official_store = scrapy.Field()
    inform = scrapy.Field()
