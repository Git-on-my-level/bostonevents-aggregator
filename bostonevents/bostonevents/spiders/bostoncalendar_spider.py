import scrapy
from bostonevents.items import BostoneventsItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            title = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()
            desc = sel.xpath('text()').extract()
            print title, link, desc

class BostonCalendarSpider(scrapy.Spider):
    name = "bostoncalendar"
    allowed_domains = ["thebostoncalendar.com/"]
    start_urls = [
        "http://www.thebostoncalendar.com/"
    ]

    def parse(self, response):
        for sel in response.xpath('//ul/li[@class="event"]'):
            item = BostoneventsItem()
            item['title'] = sel.xpath('div/h3/a/text()').extract()
            item['link'] = sel.xpath('div/h3/a/@href').extract()
            item['location'] = sel.xpath('div/p[@class="location"]/text()').extract()
            item['time'] = [text.strip() for text in sel.xpath('div/p[@class="time"]/text()').extract() if text.strip()]
            yield item
