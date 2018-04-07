# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

import MySQLdb
import MySQLdb.cursors
# spider自带的组件进行格式转换
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
# twisted异步调用框架
from twisted.enterprise import adbapi


# 主要做数据存储
class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 定义自己的pipeline来存储数据到mysql
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', 'lwy19998273333', 'article_spider', charset='utf8',
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = '''
            insert into article(title,url,create_date,fav_nums)
            VALUES (%s,%s,%s,%s)
        '''
        # 同步的操作
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))
        self.conn.commit()


# mysql连接池，通过scrapy来实现。
# twisted提供的框架
class MysqlTwistedPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    # 注意方法的名字不能写错
    @classmethod
    def from_settings(cls, settings):
        dbprams = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dppool = adbapi.ConnectionPool("MySQLdb", **dbprams)
        return cls(dppool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handler_error)  # 处理异常

    # 异步处理
    def handler_error(self, failure):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = '''
                    insert into article(title,url,create_date,fav_nums,
                    url_object_id,front_image_url,comment_nums,praise_nums,tags,content)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                '''
        # 同步的操作
        cursor.execute(insert_sql,
                       (item["title"], item["url"], item["create_date"],
                        item["fav_nums"], item["url_object_id"], item["front_image_url"],
                        item["comment_nums"], item["praise_nums"], item["tags"],
                        item["content"]))


# 保存数据
class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    # 打开json文件,初始化的时候打开
    def __init__(self):
        self.file = codecs.open("article.json", "w", encoding="utf-8")

    # 处理打开的数据
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    # 关闭文件
    def spider_close(self, spider):
        self.file.close()


# 自带的json格式
class JsonItemExporterPipeline(object):
    # 调用scrapy自带的json exporter导出json文件
    def __init__(self):
        self.file = open("articleexport.json", "wb")
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
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
        if "front_image_url" in item:
            for ok, value in results:
                images_file_path = value["path"]
            item["front_image_path"] = images_file_path
        return item
