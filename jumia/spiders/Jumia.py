import scrapy


class JumiaSpider(scrapy.Spider):
    name = "Jumia"
    allowed_domains = ["jumia.com"]
    start_urls = ["https://jumia.com"]

    def parse(self, response):
        pass
