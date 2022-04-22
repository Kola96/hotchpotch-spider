import json

import scrapy

from hcpcSpider.model.items import Article
from hcpcSpider.utils.strutils import remove_empty_char


class GcoresSpider(scrapy.Spider):
    name = '36kr'
    source = '36氪'
    allowed_domains = ['36kr.com']
    host = 'https://www.36kr.com'
    start_urls = ['https://36kr.com/']

    def parse(self, response, **kwargs) -> Article:
        res_json = response.xpath('.').re(r'<script>window.initialState=(.+?)</script>')[0]
        item_list = json.loads(res_json)['homeData']['data']['homeFlow']['data']['itemList']
        for item in item_list:
            if "itemType" not in item.keys():
                continue
            if item['itemType'] == 10:
                temp = item['templateMaterial']
                article = Article()
                article['title'] = temp['widgetTitle']
                article['source'] = self.source
                if 'authorName' in temp.keys():
                    article['author'] = temp['authorName']
                article['description'] = temp['summary']
                article['cover_img_url'] = temp['widgetImage']
                article['article_url'] = f'{self.host}/p/{temp["itemId"]}'
                article['text_xpath'] = '//p/text()'
                article['media_type'] = 0
                yield article
            elif item['itemType'] == 5000:
                continue
            elif item['itemType'] == 60:
                temp = item['templateMaterial']
                if temp['templateType'] == 6:
                    w_list = temp['widgetList']
                    for w in w_list:
                        article = Article()
                        article['title'] = w['widgetTitle']
                        article['source'] = self.source
                        article['author'] = ''
                        article['description'] = ''
                        article['cover_img_url'] = w['widgetImage']
                        article['article_url'] = f'{self.host}/video/{w["widgetId"]}'
                        article['media_type'] = 1
                        yield article
                elif temp['templateType'] == 1:
                    article = Article()
                    article['title'] = temp['widgetTitle']
                    article['source'] = self.source
                    article['author'] = temp['authorName']
                    article['description'] = remove_empty_char(temp['summary'])
                    article['cover_img_url'] = temp['widgetImage']
                    article['article_url'] = f'{self.host}/video/{temp["itemId"]}'
                    article['media_type'] = 1
                    yield article
                else:
                    continue
            else:
                continue


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl 36kr'.split(' '))
