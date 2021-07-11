import scrapy


class ChildrenSpider(scrapy.Spider):
    name = 'children'
    allowed_domains = ['e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do']
    start_urls = ['http://e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do/']

    def parse(self, response):
        pass
