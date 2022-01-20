import re

import scrapy

from hcpcSpider.model.items import Article


class EngadgetSpider(scrapy.Spider):
    name = 'engadget'
    source = 'engadget'
    allowed_domains = ['engadget.com']
    host = 'https://chinese.engadget.com'
    start_urls = ['https://chinese.engadget.com/']

    def parse(self, response, **kwargs) -> Article:
        articles = response.xpath('//article')
        for article in articles:
            item = Article()
            item['title'] = article.xpath('div/a/@alt').extract_first()
            item['source'] = self.source
            item['description'] = article.xpath('div/div/div/text()').extract_first()
            item['cover_img_url'] = re.findall(r'background-image:url\((.+)\)', article.xpath('div/a/div/@style').extract_first())
            item['article_url'] = self.host + article.xpath('div/a/@href').extract_first()
            item['text_xpath'] = '//div[@id="post-center-col"]/div[1]//p/text()'
            yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl engadget'.split(' '))
