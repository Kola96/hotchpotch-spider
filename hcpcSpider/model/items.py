import scrapy


class Article(scrapy.Item):
    title = scrapy.Field()
    source = scrapy.Field()
    author = scrapy.Field()
    description = scrapy.Field()
    cover_img_url = scrapy.Field()
    tags = scrapy.Field()
    article_url = scrapy.Field()
    sign = scrapy.Field()
    publish_time = scrapy.Field()
    text_xpath = scrapy.Field()
