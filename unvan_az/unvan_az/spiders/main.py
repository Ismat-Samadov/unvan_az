import scrapy
from scrapy_splash import SplashRequest


class LinksSpider(scrapy.Spider):
    name = "main"
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
        assert(splash:wait(2))  -- Adjust the wait time as needed
    
        -- Execute JavaScript to retrieve specific data
        local phone_number = splash:evaljs("document.querySelector('div.telzona').getAttribute('tel');")
        
        return {
            phone_number = phone_number,
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
        # Extract links and phone numbers from the current page
        divs = response.css('div.infocontact')
        for div in divs:
            link = div.css('a::attr(href)').get()
            phone_number = div.css('div.telzona::attr(tel)').get()

            yield {
                "link": link,
                "phone_number": phone_number
            }

        # Follow pagination links using Splash
        pagination_links = response.css('div.pagination a[href*="start="]::attr(href)').getall()
        for pag_link in pagination_links:
            yield SplashRequest(
                url=response.urljoin(pag_link),
                callback=self.parse,
                endpoint='execute',
                args={'lua_source': self.script}
            )
