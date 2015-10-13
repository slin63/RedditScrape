import scrapy

from tutorial.items import DmozItem # From directory.[file.py] import class

class DmozSpider(scrapy.Spider):
    name = "dmoz" # Name of the spider . . . must be unique
    allowed_domains = ["dmoz.org"]
    start_urls = [ # Where the spider will begin crawling / first pages downloaded
        "http://www.dmoz.org/Computers/Programming/Languages/Python/",
    ]

    def parse(self, response): # Handles the main links on the directory page
        for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response): # called with the downloaded Response object of each start URL
        for sel in response.xpath('//ul/li'):  # For each selection element in the path //ul/li
            item = DmozItem() # From items.py, custom dict type used to store scrapy elements
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item
            # print '{ TITLE = %s }\n{ URL = %s }\n{ DESC = %s }\n\n'%(title, url, desc)

class redditSpider(scrapy.Spider.)