# Left off : Trim vulgar.txt so we get less false positives . . .
# implement parsing comment sections / text posts
# implement some way to analyze collected information / posts outside / inside of crawler
# Maybe just parse comment threads and get title/author/votes from there

# Idea... scraper to find men's clothes, small
# Idea... scraper to cull images from /r/elitedangerous, best images each week compile them etc.
#         scraper to detect frequency of "vulgar" usernames in certain subreddit front pages
# Debug and figure out xpaths/css with shell


from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tutorial.items import RedditThread, RedditComment
from scrapy.http import Request

from tutorial.items import DmozItem  # From directory.[file.py] import class
from tutorial.spiders.filters import build_list, search_list, assign_to_item, clean_textlist

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
    allowed_domains = ["reddit.com"]
    current_subreddit = "EliteDangerous"  # Caps sensitive . . .
    start_urls = [
        "https://www.reddit.com/r/" + current_subreddit,
    ]

    rules = [
        Rule(LinkExtractor(
            allow=['/r/' + current_subreddit + '/\?count=\d*&after=\w*']),  # Looks for next page with RE
            # callback='parse_page',  # Deprecated. . . now all handled inside comment thread
            follow=True),  # Tells spider to continue after callback


        Rule(LinkExtractor(
            allow=['/r/' + current_subreddit + '/comments/[a-zA-Z0-9]{6}/[a-z_]*?/$'],),  # Looks for next page with RE
            callback='parse_comments',  # What do I do with this? --- pass to self.parse_page
            follow=False)
    ]

    def parse_page(self, response):
        """Gets title, author, and net votes on posts on each reddit page.
        Currently replaced by parse_comments"""
        selector_list = response.css('div.thing') # Each individual little "box" with content

        for selector in selector_list:
            item = RedditThread()
            item['title'] = selector.xpath('div/p/a[@class="title may-blank "]/text()').extract()

            url = selector.xpath('a/@href').extract()

            # if url[0][0] == "/":
            #     item['url'] = "https://www.reddit.com" + url[0]
            # else:
            #     item['url'] = url

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

        count = 0

        for selector in thread_selector:
            item = RedditThread()
            title = selector.xpath('.//a[@class="title may-blank "]/text()').extract()
            url = selector.xpath('.//a[@class="title may-blank "]/@href').extract()  # URL = link to .self or to content

            text = selector.xpath('.//div[@class="md"]//text()').extract()  # Might not always be text/could return None
            text = clean_textlist(text)  # Processing to make the text look pretty

            votes = selector.xpath('//div[@class="score unvoted"]/text()').extract()
            author = selector.xpath('.//p[@class="tagline"]/a/text()').extract()

            if url[0][0] == "/":
                item['url'] = "https://www.reddit.com" + url[0]
            else:
                item['url'] = url

            yield assign_to_item(item, ['title', 'url', 'votes', 'author', 'text'], [title, url, votes, author, text])

        for selector in comment_selector:
            item = RedditComment()
            hyperlink = selector.xpath('.//li[@class="first"]/a/@href').extract()
            text = selector.xpath('.//div[@class="md"]/p/text()').extract()
            if hyperlink:
                item['hyperlink'] = hyperlink  # Returns hyperlink to comment thread
            if text:
                item['text'] = clean_textlist(text)

            count += 1

            yield item

        # print "{COUNT = %i | THREAD = %s}" % (count, response.url)

