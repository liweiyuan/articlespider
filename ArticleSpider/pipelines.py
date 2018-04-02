# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline


# 主要做数据存储
class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 自己定制图片路由的pipelines--继承ImagesPipeline
class ArticleImagePipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        for ok, value in results:
            images_file_path = value["path"]
        item["front_image_path"]=images_file_path
        return item
