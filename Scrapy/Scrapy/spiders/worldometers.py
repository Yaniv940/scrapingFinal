import scrapy


class WorldometersSpider(scrapy.Spider):
    name = "worldometers"
    allowed_domains = ["worldometers.info"]
    start_urls = ["https://worldometers.info"]

    def parse(self, response):
        pass
