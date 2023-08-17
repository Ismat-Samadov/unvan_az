import scrapy


class LinksSpider(scrapy.Spider):
    name = "links"
    allowed_domains = ["test.az"]
    start_urls = ["https://unvan.az/yeni-bina-evi?start=1",
                  "https://unvan.az/kohne-bina-evi?start=1",
                  "https://unvan.az/heyet-evi-villa?start=1",
                  "https://unvan.az/obyekt-ofis?start=1",
                  "https://unvan.az/torpaq-sahesi?start=1"]

    def parse(self, response):
        pass
