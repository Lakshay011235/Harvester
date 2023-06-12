import scrapy
import pandas as pd
# from ..items import DataextractionItem

websites_to_scrape = '../Input.xlsx'
websites = pd.read_excel(websites_to_scrape)
webName = list(websites.iloc[:, 0])
webLink = list(websites.iloc[:, 1])

class ContentSpider(scrapy.Spider):
    name = 'harvester'
    handle_httpstatus_list = [200]
    fileNumber = 0
    start_urls = [webLink[fileNumber]]

    def parse_error(self, failure):
        if failure.value.response.status == 404:
            ContentSpider.fileNumber += 1
            yield scrapy.Request(webLink[ContentSpider.fileNumber], callback=self.parse, errback=self.parse_error)

    def parse(self, response):
        tre = open( r"Extracted Files\{}.txt".format(webName[ContentSpider.fileNumber]), 'w', encoding="utf-8")
        title = response.css('h1::text').extract_first()
        content = response.css('div p::text').extract()[:-3]
        try:
            tre.write(str(title)+"\n"+ '\n'.join(content))
        except:
            tre.writelines(str(title))
            tre.write(str(content))
        tre.close()
        yield {'title' : title , 'content' : content}

        if webName[ContentSpider.fileNumber] is not None:
            ContentSpider.fileNumber += 1
            yield response.follow(webLink[ContentSpider.fileNumber], callback=self.parse, errback=self.parse_error)
