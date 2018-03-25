# -*- coding: utf-8 -*-
import re

import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/112048/']

    def parse(self, response):
        # re_selector = response.xpath("/html/body/div[3]/div[3]/div[1]/div[1]/h1")
        # re2_selector = response.xpath('//*[@id="post-112048"]/div[1]/h1/text()')
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        # 获取时间
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·",
                                                                                                                    "").strip()
        # 点赞数
        praise_nums = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract()[0]
        # 收藏数
        fav_nums = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0]
        match_re = re.match(".*(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        # 评论数
        common_nums = response.xpath('//a[@href="#article-comment"]/span').extract()[0]
        match_re = re.match(".*(\d+).*", common_nums)
        if match_re:
            common_nums = match_re.group(1)
        # 正文内容
        content = response.xpath('//div[@class="entry"]').extract()[0]
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

        '''
        python通过css选择器来提取元素
        '''
        # 通过css选择器来获取标题。
        title = response.css(".entry-header h1::text").extract()[0]
        create_date=response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·","").strip()
        praise_nums=response.css("span.vote-post-up h10::text").extract()[0]
        fav_nums=response.css("span.bookmark-btn::text").extract()[0]
        match_re = re.match(".*(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        common_nums=response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(".*(\d+).*", common_nums)
        if match_re:
            common_nums = match_re.group(1)
        content=response.css("div.entry").extract()[0]
        tags=response.css(".entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)
        pass
