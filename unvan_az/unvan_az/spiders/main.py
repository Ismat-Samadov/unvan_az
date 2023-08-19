import scrapy
from scrapy_splash import SplashRequest


class PropertySpider(scrapy.Spider):
    name = "main"
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'middlewares.DelayedRequestsMiddleware': 123},
    }
    allowed_domains = ["unvan.az"]
    start_urls = [
        "https://unvan.az/yeni-bina-evi?start=1",  # 152 * 20 + 3
        "https://unvan.az/kohne-bina-evi?start=1",  # 80 * 20 + 3
        "https://unvan.az/heyet-evi-villa?start=1",  # 159 * 20
        "https://unvan.az/obyekt-ofis?start=1",  # 32 * 20 + 6
        "https://unvan.az/torpaq-sahesi?start=1"  # 30 *20 + 13    ==>> total :  9085
    ]
    script = '''
        function main(splash,args)
          splash.private_mode_enabled=false
          url=args.url
          assert(splash:go(url))
          assert(splash:wait(2))  -- Adjust the wait time if needed
          return {
            html=splash:html()
            }
        end   
    '''

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse_links,
                endpoint='execute',
                args={'lua_source': self.script},
                meta={'delay_request_by': 5}
            )

    def parse_links(self, response):
        # Extract links from the current page
        links = response.css('div.holderimg a::attr(href)').getall()
        for link in links:
            yield SplashRequest(
                url=response.urljoin(link),
                callback=self.parse_details,
                endpoint='execute',
                args={'lua_source': self.script}
            )

        # Follow all pagination links using Splash
        pagination_links = response.css('div.pagination a[href*="start="]::attr(href)').getall()
        for pag_link in pagination_links:
            yield SplashRequest(
                url=response.urljoin(pag_link),
                callback=self.parse_links,
                endpoint='execute',
                args={'lua_source': self.script}
            )

    def parse_details(self, response):

        yield {
            'link': response.url,
            'phone': response.css('div.telzona::attr(tel)').getall(),
            'short_descr': response.css('h1.leftfloat::text').get(),
        }
