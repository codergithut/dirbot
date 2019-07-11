import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector

from dirbot.items import Website


class DmozSpider(Spider):
    name = "dmoz"
    depth = 2
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "https://www.python.org/",
    ]

    def parse(self, response):
        item=None
        print("===============")
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """

        if 'item' in response.meta:
            item = response.meta['item']

        if item is None:
            item = Website()
            item['url'] = self.start_urls[0]
            item['depth']=0

        hxs = Selector(response)
        hrefs = hxs.xpath("/html/body//@href").extract()
        item['description'] = '测试'
        item['title']= 'title'
        yield item
        for a in hrefs:
            item_detail=Website()
            item_detail['depth'] = item['depth'] + 1
            item_detail['url'] = a
            if item_detail['depth'] > self.depth :
                return
            else:
                if a.startswith('http') and a.find('python') >= 0:
                    yield scrapy.Request(url=a, meta={'item': item_detail}, callback=self.parse, dont_filter=True)
                    pass
                pass
        pass
    pass
