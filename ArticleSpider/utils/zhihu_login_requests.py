import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

session = requests.session()

agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0"

header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": agent
}

session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未能加载")


def is_login():
    # 通过个人中心来判断用户是否登录
    inbox_url = "https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True


def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=header)
    # print(response.text)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return match_obj.group(1)
    else:
        return ""


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print("ok")


# 知乎登录
def zhuhu_login(acount, password):
    if re.match("^1\d{10}", acount):
        print("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": acount,
            "password": password
        }
    else:
        if "@" in acount:
            print("邮箱登录")
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": acount,
                "password": password
            }
    response_text = session.post(post_url, post_data, headers=header)

    session.cookies.save()


zhuhu_login("15309951135", "lwy19998273333")
# get_index()
is_login()
