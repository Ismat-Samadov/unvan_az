import scrapy


class LinksSpider(scrapy.Spider):
    name = "links"
    allowed_domains = ["test.az"]
    start_urls = ["https://unvan.az/yeni-bina-evi?start=1",
                  "https://unvan.az/kohne-bina-evi?start=1",
                  "https://unvan.az/heyet-evi-villa?start=1",
                  "https://unvan.az/obyekt-ofis?start=1",
                  "https://unvan.az/torpaq-sahesi?start=1"]
    script = '''
           function main(splash, args)
               splash.private_mode_enabled = false
               url = args.url
               assert(splash:go(url))
               splash:set_viewport_full()
               return {
                   png = splash:png(),
                   html = splash:html()
               }
           end   
       '''

    def parse(self, response):
        href=response.css('holderimg').get()
        yield {
            "link":href
        }
