import scrapy
from scrapy_splash import SplashRequest


class LinksSpider(scrapy.Spider):
    name = "links"
    allowed_domains = ["unvan.az"]
    start_urls = [
        "https://unvan.az/yeni-bina-evi?start=1",
        "https://unvan.az/kohne-bina-evi?start=1",
        "https://unvan.az/heyet-evi-villa?start=1",
        "https://unvan.az/obyekt-ofis?start=1",
        "https://unvan.az/torpaq-sahesi?start=1"
    ]
    script = '''
       function main(splash, args)
           splash.private_mode_enabled = false
           assert(splash:go(args.url))
           assert(splash:wait(2))  -- Adjust the wait time if needed
           return {
               html = splash:html()
           }
       end
    '''

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                endpoint='execute',
                args={'lua_source': self.script}
            )

    def parse(self, response):
        # Extract links from the current page
        links = response.css('div.holderimg a::attr(href)').getall()
        for link in links:
            yield {
                "link": link
            }

        # Follow all pagination links using Splash
        pagination_links = response.css('div.pagination a[href*="start="]::attr(href)').getall()
        for pag_link in pagination_links:
            yield SplashRequest(
                url=response.urljoin(pag_link),
                callback=self.parse,
                endpoint='execute',
                args={'lua_source': self.script}
            )
