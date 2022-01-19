import hashlib
import logging
from datetime import datetime
from typing import Any

import pymysql
from scrapy.exceptions import DropItem

from hcpcSpider.settings import MYSQL_CONFIG


class MysqlPipeline:
    conn: pymysql.Connection
    cursor: Any

    def process_item(self, item, spider):
        item.setdefault('title', '')
        item.setdefault('author', '')
        item.setdefault('description', '')
        item.setdefault('cover_img_url', '')
        item.setdefault('tags', [])
        item.setdefault('publish_time', datetime.now())
        # 处理超长desc
        if isinstance(item['description'], str):
            if len(item['description']) >= 220:
                item['description'] = item['description'][:220] + "..."
        else:
            item['description'] = ''

        spider.log(f'''
        INSERT INTO hcpc_article (`title`, `source`, `author`, `description`, `cover_img_url`, `tags`, `article_url`, `sign`, `publish_time`)
        VALUES ('{item['title']}', 
                '{item['source']}', 
                '{item['author']}', 
                '{item['description']}', 
                '{item['cover_img_url']}', 
                '{item['tags']}', 
                '{item['article_url']}', 
                '{item['sign']}', 
                '{item['publish_time']}')''')
        insert_sql = '''INSERT INTO hcpc_article (`title`, `source`, `author`, `description`, `cover_img_url`, `tags`, `article_url`, `sign`, `publish_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        self.cursor.execute(insert_sql, (item['title'],
                                         item['source'],
                                         item['author'],
                                         item['description'],
                                         item['cover_img_url'],
                                         ','.join(item['tags']),
                                         item['article_url'],
                                         item['sign'],
                                         item['publish_time']))
        self.conn.commit()

    def open_spider(self, spider):
        self.conn = pymysql.Connect(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            passwd=MYSQL_CONFIG['password'],
            db=MYSQL_CONFIG['db']
        )
        self.cursor = self.conn.cursor()
        spider.log('[MysqlPipeline] MySQL连接已开启', level=logging.INFO)

    def close_spider(self, spider):
        if self.conn is not None:
            self.conn.close()
            spider.log('[MysqlPipeline] MySQL连接已关闭', level=logging.INFO)


class UnrepeatedPipeline:
    conn: pymysql.Connection
    cursor: Any

    def process_item(self, item, spider):
        item['sign'] = hashlib.md5(item['article_url'].encode('utf-8')).hexdigest().upper()

        self.cursor.execute('SELECT count(1) FROM hcpc_article WHERE `sign` = %s', (item['sign'],))
        res = self.cursor.fetchone()[0]
        if res == 0:
            return item
        else:
            raise DropItem(f'该文章已存在: <{item["sign"]}>')

    def open_spider(self, spider):
        self.conn = pymysql.Connect(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            passwd=MYSQL_CONFIG['password'],
            db=MYSQL_CONFIG['db']
        )
        self.cursor = self.conn.cursor()
        spider.log('[UnrepeatedPipeline] MySQL连接已开启', level=logging.INFO)

    def close_spider(self, spider):
        if self.conn is not None:
            self.conn.close()
            spider.log('[UnrepeatedPipeline] MySQL连接已关闭', level=logging.INFO)
