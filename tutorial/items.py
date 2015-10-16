# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field


class DmozItem(Item):
    title = Field()
    link = Field()
    desc = Field()


class RedditThread(Item):
    title = Field()
    url = Field()
    votes = Field()
    author = Field()
    text = Field()
    type = Field()


class RedditComment(Item):
    text = Field()
    url = Field()
    votes = Field()
    author = Field()
    type = Field()
    hyperlink = Field()

