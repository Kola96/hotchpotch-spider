import scrapy

from hcpcSpider.model.items import Article


class ChuappSpider(scrapy.Spider):
    name = 'chuapp'
    source = '触乐网'
    allowed_domains = ['chuapp.com']
    host = 'https://www.chuapp.com'
    start_urls = ['http://www.chuapp.com/category/index/id/daily/p/1.html',
                  'http://www.chuapp.com/category/index/id/pcz/p/1.html',
                  'http://www.chuapp.com/tag/index/id/20369/p/1.html',
                  'http://www.chuapp.com/category/index/id/zsyx/p/1.html']

    def parse(self, response, **kwargs) -> Article:
        article_list = response.xpath('//div[@class="category-list"]/a')
        for a in article_list:
            article = Article()
            article['title'] = a.xpath('@title').extract_first().strip()
            article['source'] = self.source
            article['author'] = a.xpath('.//span/em/text()').extract_first().strip()
            article['description'] = a.xpath('dl[@class="fn-left"]/dd/text()').extract_first().strip()
            article['cover_img_url'] = a.xpath('img/@src').re(r'(.+)\?imageView')[0]
            article['tags'] = ['游戏']
            article['article_url'] = self.host + a.xpath('@href').extract_first().strip()
            article['text_xpath'] = '//div[@class="the-content"]//text()'
            article['media_type'] = 0
            yield article


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl chuapp'.split(' '))
