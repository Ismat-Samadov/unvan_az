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
                            args={'lua_source': self.script}
                            )

    def parse(self, response):
        phone_number = response.css('div.telzona::attr(tel)').getall()

        yield {
            'phone': phone_number
        }
