__author__="wade"

import hashlib
#定义自己的md5函数
def get_md5(url):
    #判断编码格式
    if isinstance(url,str):
        url=url.encode("utf8")
    m=hashlib.md5()
    m.update(url)
    return m.hexdigest()

#测试一下
if __name__=="__main__":
    print(get_md5("http://blog.jobbole.com/all-posts/".encode("utf8")))