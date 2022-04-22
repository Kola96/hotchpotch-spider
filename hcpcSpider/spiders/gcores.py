import scrapy

from hcpcSpider.model.items import Article


class GcoresSpider(scrapy.Spider):
    name = 'gcores'
    source = '机核网'
    allowed_domains = ['gcores.com']
    host = 'https://www.gcores.com'
    start_urls = ['https://www.gcores.com/gapi/v1/originals?page[limit]=20&page[offset]=0&sort=-published-at&include=category,user&filter[is-news]=1&filter[list-all]=0&fields[articles]=title,desc,is-published,thumb,app-cover,cover,comments-count,likes-count,bookmarks-count,is-verified,published-at,option-is-official,option-is-focus-showcase,duration,category,user',
                  'https://www.gcores.com/gapi/v1/articles?page[limit]=20&page[offset]=12&sort=-published-at&include=category,user&filter[is-news]=0&filter[list-all]=0&fields[articles]=title,desc,is-published,thumb,app-cover,cover,comments-count,likes-count,bookmarks-count,is-verified,published-at,option-is-official,option-is-focus-showcase,duration,category,user']

    def parse(self, response, **kwargs) -> Article:
        res_json = response.json()

        # 处理相关信息映射关系
        authors = {}
        categories = {}
        included = res_json['included']
        for i in included:
            if i['type'] == 'users':
                authors[i['id']] = i['attributes']['nickname']
            elif i['type'] == 'categories':
                categories[i['id']] = i['attributes']['name']

        # 处理文章内容
        data = res_json['data']
        for i in data:
            article = Article()
            article['title'] = i['attributes']['title']
            article['source'] = self.source
            article['author'] = authors[i['relationships']['user']['data']['id']]
            article['description'] = i['attributes']['desc']
            article['cover_img_url'] = 'https://image.gcores.com/' + i['attributes']['thumb']
            article['tags'] = ['游戏', categories[i['relationships']['category']['data']['id']]]
            article['article_url'] = self.host + '/articles/' + i['id']
            article['publish_time'] = i['attributes']['published-at'].split('+')[0].replace('T', ' ')
            article['text_xpath'] = '//div[@data-contents="true"]//text()'
            article['media_type'] = 0
            yield article


if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl gcores'.split(' '))
