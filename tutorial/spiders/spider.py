import scrapy


class DmozSpider(scrapy.Spider):
    name = 'dmoz' # Name of the spider . . . must be unique
    allowed_domains = ["dmoz.org"]
    start_urls = [ # Where the spider will begin crawling / first pages downloaded
         "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
         "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response): #called with the downloaded Response object of each start URL
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)