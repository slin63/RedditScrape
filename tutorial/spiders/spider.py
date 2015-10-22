# Left off : Trim vulgar.txt so we get less false positives . . .
# implement parsing comment sections / text posts
# implement some way to analyze collected information / posts outside / inside of crawler
# Parse the .json or parse directly what we get here . . . .
# Calculate average # net votes per post per word in the text etc fun stats
# Implement matlab graphing for stat collection pipeline
# Launch from .py?
# Only scrape very first page . . .

# Idea... scraper to find men's clothes, small
# Idea... scraper to cull images from /r/elitedangerous, best images each week compile them etc.
#         scraper to detect frequency of "vulgar" usernames in certain subreddit front pages

# cool: https://www.reddit.com/r/dataisbeautiful/comments/3pckdc/swear_words_per_minute_on_reddit_during_a_college/

from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tutorial.items import RedditThread, RedditComment
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
        for href in response.css("ul.directory.dir-col > li > a::attr('href')"): #
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

    def __init__(self, current_subreddit='', *args, **kwargs):
        super(redditSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            "https://www.reddit.com/r/" + current_subreddit,
        ]

    allowed_domains = ["reddit.com"]
    # current_subreddit = "AskReddit"  # Caps sensitive . . .

    rules = [
        Rule(LinkExtractor(
            allow=['/r/\w*/\?count=\d*&after=\w*']),  # Looks for next page with RE
            # callback='parse_page',  # Deprecated. . . now all handled inside comment thread
            follow=True),  # Tells spider to continue after callback

        Rule(LinkExtractor(
            allow=['/r/\w*/comments/[a-zA-Z0-9]{6}/[a-z_]*?/$'],),  # Goes to comment section
            callback='parse_comments',  # What do I do with this? --- pass to self.parse_page
            follow=False)
    ]

    custom_settings = {
        "BOT_NAME": 'redditscraper',
        "DEPTH_LIMIT": 1,
    }

    def parse_page(self, response):
        """Gets title, author, and net votes on posts on each reddit page.
        Currently replaced by parse_comments"""
        selector_list = response.css('div.thing') # Each individual little "box" with content

        for selector in selector_list:
            item = RedditThread()
            item['title'] = selector.xpath('div/p/a[@class="title may-blank "]/text()').extract()

            url = selector.xpath('a/@href').extract()

            item['author'] = selector.xpath('.//p[@class="tagline"]/a/text()').extract()
            item['votes'] = selector.xpath('.//div[@class="score unvoted"]/text()').extract()
            # .//div means that under the selector_list, all div elements with [@class="etcetc"]

            if search_list(item['author'][0], build_list('vulgar')):
                print "{ DING! - AUTHOR = %s | POST = %s | VOTES = %s }" % (item['author'][0], item['title'][0], item['votes'][0])

            yield item

    def parse_comments(self, response):
        """Called when crawling into a comment section. Gets post title, author, net votes, and
        repeats the task for the top 200 comments in the thread."""
        thread_selector = response.xpath('//div[@class="sitetable linklisting"]')
        comment_selector = response.xpath('//div[@class="commentarea"]//div[@class="entry unvoted"]')

        for selector in thread_selector:  # Reads original post
            item = RedditThread()
            item['type'] = [u'THREAD']  #  [u'text'], u indicates "unicode" string
            item['title'] = selector.xpath('.//a[@class="title may-blank "]/text()').extract()
            item['url'] = selector.xpath('.//a[@class="title may-blank "]/@href').extract()  # URL = link to .self or to content
            item['text'] = selector.xpath('.//div[@class="md"]//text()').extract()  # Might not always be text/could return None
            item['votes'] = selector.xpath('//div[@class="score unvoted"]/text()').extract()
            item['author'] = selector.xpath('.//p[@class="tagline"]/a/text()').extract()

            yield item

        for selector in comment_selector:  # Reads comments
            item = RedditComment()
            item['type'] = [u'COMMENT']  # [u'text'], u indicates "unicode" string
            item['url'] = response.xpath('//div[@class="sitetable linklisting"]').xpath('.//a[@class="title may-blank "]/@href').extract()
            item['text'] = selector.xpath('.//div[@class="md"]/p/text()').extract()
            item['votes'] = selector.xpath('.//p/span[@class="score unvoted"]/text()').extract()
            item['hyperlink'] = selector.xpath('.//li[@class="first"]/a/@href').extract()  # Links directly to comment

            if item['hyperlink']:  # If there's no hyperlink, we scraped an invalid comment.
                yield item








