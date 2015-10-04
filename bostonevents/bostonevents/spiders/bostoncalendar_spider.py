import scrapy
from urlparse import urljoin
from bostonevents.items import BostoneventsItem

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
            item['link'] = [urljoin(response.url, relative_url) for relative_url in sel.xpath('div/h3/a/@href').extract()]
            item['location'] = sel.xpath('div/p[@class="location"]/text()').extract()
            item['time'] = [text.strip() for text in sel.xpath('div/p[@class="time"]/text()').extract() if text.strip()]
            item['image_url'] = [urljoin(response.url, thumb_url.replace('/thumb/', '/original/')) for thumb_url in sel.xpath('a[@class="img-link"]/img/@href').extract()]
            yield item
