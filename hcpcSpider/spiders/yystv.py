import scrapy

from hcpcSpider.model.items import Article


class YysSpider(scrapy.Spider):
    name = 'yystv'
    source = '游研社'
    allowed_domains = ['yystv.cn']
    host = 'https://www.yystv.cn'
    start_urls = ['https://www.yystv.cn/docs']

    def parse(self, response, **kwargs) -> Article:
        containers = response.xpath('//*[@id="page-container"]/div[2]/div[1]/ul/li')
        for container in containers:
            article = Article()
            article['title'] = container.xpath('a/div/h2/text()').extract_first()
            article['source'] = self.source
            article['author'] = container.xpath('a/div/div/div[1]/text()').extract_first()
            article['description'] = container.xpath('a/div/p/text()').extract_first()
            article['cover_img_url'] = container.xpath('a/div[1]/div[@class="scale-img"]/@style').re(r'background-image: url\((.+)_w360\)')[0]
            article['tags'] = ['游戏']
            article['article_url'] = self.host + container.xpath('a/@href').extract_first()
            article['text_xpath'] = '//div[@class="doc-content rel"]/div[1]//text()'
            yield article


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl yystv'.split(' '))
