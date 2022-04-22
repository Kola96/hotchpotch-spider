import scrapy

from hcpcSpider.model.items import Article


class AutohomeArticleSpider(scrapy.Spider):
    name = 'autohome-article'
    source = '汽车之家'
    allowed_domains = ['autohome.com.cn']
    host = 'https://www.autohome.com.cn'
    start_urls = ['https://www.autohome.com.cn/all/']

    def parse(self, response, **kwargs) -> Article:
        focus_list = response.xpath('//div[@class="news-focus"]//div[@class="focusimg-pic"]//li')
        for focus in focus_list:
            article = Article()
            article['title'] = focus.xpath('h2//text()').extract_first()
            article['source'] = self.source
            article['description'] = focus.xpath('p//text()').extract_first()
            article['cover_img_url'] = "https://x.autoimg.cn/www/common/images/logo_slogan_beta_2021.png"
            article['tags'] = ['汽车']
            article['article_url'] = 'https:' + focus.xpath('a/@href').extract_first()
            article['text_xpath'] = '//*[@id="articleContent"]/p//text()'
            article['media_type'] = 0
            yield article

        article_list = response.xpath('//ul[@class="article"]/li')
        for a in article_list:
            article = Article()
            article['title'] = a.xpath('a/h3/text()').extract_first()
            if article['title'] is None:
                continue
            article['source'] = self.source
            article['description'] = a.xpath('a/p/text()').extract_first()
            article['cover_img_url'] = "https://x.autoimg.cn/www/common/images/logo_slogan_beta_2021.png"
            article['tags'] = ['汽车']
            article['article_url'] = 'https:' + a.xpath('a/@href').extract_first()
            article['text_xpath'] = '//*[@id="articleContent"]/p//text()'
            article['media_type'] = 0
            yield article


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl autohome-article'.split(' '))
