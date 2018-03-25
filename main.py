
#调试爬虫
from scrapy.cmdline import execute

import sys

#获取当前文件所在的目录
import os
# 获取当前文件所在的目录
import os
import sys

from scrapy.cmdline import execute

#打印一下
#print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#执行对应的命令
execute(["scrapy","crawl","jobbole"])