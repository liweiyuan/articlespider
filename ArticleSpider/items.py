# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 传递的值的预处理如title
def add_jobbole(value):
    return value + ".jobbole"


def date_covert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


# 定义自己的loader
class ArticleItemLoader(ItemLoader):
    # 定义自己的loader
    default_output_processor = TakeFirst()


# 正则表达式匹配(点赞，收藏，评论)
def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def remove_comment_tags(value):
    #去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value

def return_value(value):
    return value

# 定义自己的item，方便统一处理
class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        # 会调用多个
        # input_processor=MapCompose(add_jobbole)#也可以是lambda表达式
        # input_processor=MapCompose(lambda x: x + "-jobbole")
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(date_covert)
        # output_processor=TakeFirst() #只取第一个
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()  # md5压缩
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    content = scrapy.Field()
