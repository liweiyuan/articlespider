# -*- coding: utf-8 -*-
import re
from urllib import parse

import scrapy
from scrapy.http import Request


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):

        '''
        处理的逻辑分为2步
        1.获取文章中的url列表并交给scrapy进行下载并解析
        2.获取下一个页的url交给scrapy进行下载,下载后交给parse函数。
        '''

        # 解析列表中的url并交给scrapy进行下载
        post_urls = response.css(".post.floated-thumb .post-thumb a::attr(href)").extract()
        # archive > div:nth-child(1) > div.post-thumb > a
        # archive > div:nth-child(2) > div.post-thumb > a
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)  #异步操作
            print(post_url)
        # 提取下一页并交给scrapy进行下载
        next_urls = response.css(".next.page-numbers::attr(href)").extract_first("")
        # 判断存在这样的url就进行迭代
        if next_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    # 解析具体的内容
    def parse_detail(self, response):
        '''
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
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        # 评论数
        comment_nums = response.xpath('//a[@href="#article-comment"]/span').extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        #没有评论就设置默认值为0
        else:
            common_nums=0
        # 正文内容
        content = response.xpath('//div[@class="entry"]').extract()[0]
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

        '''

        '''
        python通过css选择器来提取元素
        '''
        # 通过css选择器来获取标题。
        title = response.css(".entry-header h1::text").extract()[0]
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·", "").strip()
        praise_nums = response.css("span.vote-post-up h10::text").extract()[0]
        fav_nums = response.css("span.bookmark-btn::text").extract()[0]
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        content = response.css("div.entry").extract()[0]
        tag_list = response.css(".entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)
        pass

    '''
      extract_first() 处理异常，有一个默认的值
    '''
