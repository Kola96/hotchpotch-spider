import logging

import requests
from lxml import etree

from hcpcSpider.utils.hanlputils import get_keyword
from hcpcSpider.settings import USER_AGENT


class SegmentPipeline:

    def process_item(self, item, spider):
        if item['media_type'] == 1:
            item['content'] = '视频'
            return item
        url = item['article_url']
        spider.log(f'提取文章关键词, 标题: {item["title"]}, URL: {url}', level=logging.INFO)
        html_text = requests.get(url, headers={"User-Agent": USER_AGENT}).text
        html = etree.HTML(html_text)
        res = html.xpath(item['text_xpath'])
        text = ''.join([p.strip() for p in res])
        keywords = get_keyword(text)
        keywords = [w for w in keywords if len(w) > 1]
        spider.log(f'提取结果: {keywords}', level=logging.INFO)
        item['tags'] = keywords
        item['content'] = text
        return item
