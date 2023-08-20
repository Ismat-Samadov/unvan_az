import scrapy
from scrapy_splash import SplashRequest


class ContentSpider(scrapy.Spider):
    name = "content"
    allowed_domains = ["unvan.az"]

    script = '''
        function main(splash,args)
          splash.private_mode_enabled=false
          url=args.url
          assert(splash:go(url))
          splash:set_viewport_full()
          return {
            html=splash:html()
            }
        end   
    '''

    def start_requests(self):

        yield SplashRequest(url='https://unvan.az/neftciler-metrosu-2584465.html',
                            callback=self.parse,
                            endpoint='execute',
                            args={'lua_source': self.script},
                            headers=headers
                            )

    def parse(self, response):
        phone_number = response.css('div.telzona::attr(tel)').getall()

        yield {
            'id': response.css('span.open_idshow::text').getall(),
            'date': response.xpath('//*[@id="openhalf"]/div[3]/span/text()').getall(),
            'link': response.url,
            'short_descr': response.css('h1.leftfloat::text').getall(),
            'long_descr': response.xpath('//*[@id="openhalf"]/p[1]/text()').getall(),
            'address': response.css('p.infop100.linkteshow::text').getall()[2],
            'location': response.css('.linkteshow > a::text').getall(),
            'type': response.css('p > a::text').getall()[0],
            'room_count': response.css('p:contains("Otaq sayı")::text').getall(),
            'area': response.css('p:contains("Sahə")::text').getall(),
            'price': response.css('span.pricecolor::text').getall(),
            'owner': response.xpath('//*[@id="openhalf"]/div[2]/text()').getall()[3],
            'owner_address': response.xpath('//*[@id="openhalf"]/div[2]/text()').getall()[5],
            'phone': response.css('div.telzona::attr(tel)').getall(),

        }
