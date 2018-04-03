# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

# spider自带的组件进行格式转换
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline


# 主要做数据存储
class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 保存数据
class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    # 打开json文件,初始化的时候打开
    def __init__(self):
        self.file = codecs.open("article.json", "w", encoding="utf-8")

    # 处理打开的数据
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    #关闭文件
    def spider_close(self,spider):
        self.file.close()

#自带的json格式
class JsonItemExporterPipeline(object):
    #调用scrapy自带的json exporter导出json文件
    def __init__(self):
        self.file=open("articleexport.json","wb")
        self.exporter=JsonItemExporter(self.file,encoding="utf-8",ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

# 自己定制图片路由的pipelines--继承ImagesPipeline
class ArticleImagePipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        for ok, value in results:
            images_file_path = value["path"]
        item["front_image_path"] = images_file_path
        return item
