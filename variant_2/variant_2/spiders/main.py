import scrapy


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

    def parse(self, response):
        # Extract links from the current page
        links = response.css('div.holderimg a::attr(href)').getall()
        for link in links:
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.parse_details
            )

        # Follow all pagination links
        pagination_links = response.css('div.pagination a[href*="start="]::attr(href)').getall()
        for pag_link in pagination_links:
            yield scrapy.Request(
                url=response.urljoin(pag_link),
                callback=self.parse
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
                'address_2': response.css('.linkteshow > a::text').getall(),
                'type': response.css('p > a::text').getall()[0],
                'room_count': response.css('p:contains("Otaq sayı")::text').getall(),
                'area': response.css('p:contains("Sahə")::text').getall(),
                'price': response.css('span.pricecolor::text').getall(),
                'owner_address': response.xpath('//*[@id="openhalf"]/div[2]/text()').getall()[6],
                'owner': response.xpath('//div[@class="infocontact"]/strong/text()').getall(),
                'phone_main': response.css('div#telshow::text').getall(),
            }
        except Exception as e:
            self.logger.error(f"Error parsing details for {response.url}: {e}")
