import scrapy

from hcpcSpider.model.items import Article


class YicheArticleSpider(scrapy.Spider):
    name = 'yiche-article'
    source = '易车'
    allowed_domains = ['yiche.com']
    host = 'https://news.yiche.com'
    start_urls = ['https://news.yiche.com/info/categoryId0_p0_l0_f0_g0_c0_b0_1.html']

    def parse(self, response, **kwargs) -> Article:
        article_divs = response.xpath('//div[@class="article-list"]/div')
        for div in article_divs:
            article = Article()
            article['title'] = div.xpath('div//h2/a/text()').extract_first()
            article['source'] = self.source
            article['author'] = div.xpath('div//a[@class="author"]/text()').extract_first()
            article['description'] = div.xpath('div//p[@class="desc"]/text()').extract_first()
            article['cover_img_url'] = div.xpath('div//img/@data-original').extract_first()
            article['tags'] = ['汽车']
            article['article_url'] = self.host + div.xpath('div//a/@href').extract_first()
            article['publish_time'] = div.xpath('div//*[@class="time"]/text()').extract_first()
            article['text_xpath'] = '//div[@class="news-detail-main motu_cont"]//text()'
            yield article


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl yiche-article'.split(' '))
