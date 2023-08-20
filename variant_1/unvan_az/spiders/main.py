import scrapy
from scrapy_splash import SplashRequest


class PropertySpider(scrapy.Spider):
    name = "main"
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
          local response = splash:go(url)
          if not response then
             error("Failed to retrieve the page")
          end
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
        try:
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
        except Exception as e:
            self.logger.error(f"Error parsing details for {response.url}: {e}")
