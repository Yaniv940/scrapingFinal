import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        # Extract quotes and authors from the page
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('span[@class="text"]/text()').get(),
                'author': quote.xpath('span/small[@class="author"]/text()').get(),
            }

        # Follow pagination links (next page)
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
