import re
from html import unescape

import scrapy

from hcpcSpider.model.items import Article


class VgtimeSpider(scrapy.Spider):
    name = 'vgtime'
    source = 'vgtime'
    allowed_domains = ['vgtime.com']
    host = 'https://www.vgtime.com'
    start_urls = [
        'https://www.vgtime.com/topic/index/load.jhtml?page=1&pageSize=20',
        'https://www.vgtime.com/game/eval_list.jhtml?page=1&pageSize=20',
        'https://www.vgtime.com/column/list.jhtml?page=1&pageSize=20',
    ]

    def parse(self, response, **kwargs) -> Article:
        xml: str = response.json()['data']
        if isinstance(xml, list):
            for o in xml:
                article = Article()
                article['title'] = unescape(o['title'])
                article['source'] = self.source
                article['author'] = o['author']
                article['description'] = unescape(o['remark'])
                article['cover_img_url'] = o['cover']
                article['tags'] = ['游戏']
                article['article_url'] = f'{self.host}/topic/{o["id"]}.jhtml'
                article['text_xpath'] = '//article/div[3]//text()'
                yield article
        else:
            lis = re.findall(r'<li class=\'news\'>.+?</li>', xml)
            for li in lis:
                article = Article()
                article['title'] = unescape(re.findall(r'<h2>(.+)</h2>', li)[0])
                article['source'] = self.source
                article['author'] = re.findall(r'<span class=\'user_name left\'>(.+?)</span>', li)[0]
                article['description'] = unescape(re.findall(r'<p>(.+)</p>', li)[0])
                cover_img_url = re.findall(r'<img +src=\'(.+?)\'/>', li)
                if len(cover_img_url) > 0:
                    article['cover_img_url'] = cover_img_url[0]
                article['tags'] = ['游戏']
                article['article_url'] = self.host + re.findall(r'href=\'(.+?)\'', li)[0]
                article['text_xpath'] = '//article/div[3]//text()'
                yield article


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl vgtime'.split(' '))
