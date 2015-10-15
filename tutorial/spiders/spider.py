# Left off : Trim vulgar.txt so we get less false positives . . .
# implement parsing comment sections / text posts
# implement some way to analyze collected information / posts outside / inside of crawler

# Idea... scraper to find men's clothes, small
# Idea... scraper to cull images from /r/elitedangerous, best images each week compile them etc.
#         scraper to detect frequency of "vulgar" usernames in certain subreddit front pages
# Debug and figure out xpaths/css with shell

# import scrapy

from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tutorial.items import PicItem, RedditItem
from scrapy.http import Request

from tutorial.items import DmozItem  # From directory.[file.py] import class
from tutorial.spiders.filters import build_list, search_list

class DmozSpider(Spider):
    name = "dmoz" # Name of the spider . . . must be unique
    allowed_domains = ["dmoz.org"]
    start_urls = [ # Where the spider will begin crawling / first pages downloaded
        "http://www.dmoz.org/Computers/Programming/Languages/Python/",
    ]

    def parse(self, response): # Handles the main links on the directory page
        for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response): # called with the downloaded Response object of each start URL
        for sel in response.xpath('//ul/li'):  # For each selection element in the path //ul/li
            item = DmozItem() # From items.py, custom dict type used to store scrapy elements
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item
            # print '{ TITLE = %s }\n{ URL = %s }\n{ DESC = %s }\n\n'%(title, url, desc)


class redditSpider(CrawlSpider):  # http://doc.scrapy.org/en/1.0/topics/spiders.html#scrapy.spiders.CrawlSpider
    name = "reddits"
    allowed_domains = ["reddit.com"]
    start_urls = [
        "https://www.reddit.com/r/AskReddit/",
    ]

    # l = build_list('vulgar')

    rules = [
        Rule(LinkExtractor(
            allow=['/r/AskReddit/\?count=\d*&after=\w*']),  # Looks for next page with RE
            callback='parse_item',  # What do I do with this? --- pass to self.parse_item
            follow=True),  # Tells spider to continue after callback
    ]

    def parse_item(self, response):
        selector_list = response.css('div.thing') # Each individual little "box" with content

        for selector in selector_list:
            item = RedditItem()
            item['title'] = selector.xpath('div/p/a[@class="title may-blank "]/text()').extract()

            url = selector.xpath('a/@href').extract()

            # if url[0][0] == "/":
            #     item['url'] = "https://www.reddit.com" + url[0]
            # else:
            #     item['url'] = url

            item['author'] = selector.xpath('.//p[@class="tagline"]/a/text()').extract()
            item['votes'] = selector.xpath('.//div[@class="score unvoted"]/text()').extract()  # .// means:
            # item['votes'] = selector.css('div.score.unvoted::text').extract()                # Under div.thing, all div elements

            if search_list(item['author'][0], build_list('vulgar')):
                print "{ DING! - AUTHOR = %s | POST = %s | VOTES = %s }" % (item['author'][0], item['title'][0], item['votes'][0])

            yield item
