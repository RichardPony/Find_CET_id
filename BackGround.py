import requests
from bs4 import BeautifulSoup

login_head = '''Host:cet-bm.neea.edu.cn
Connection:keep-alive
Content-Length:111
Accept:*/*
Origin:http://cet-bm.neea.edu.cn
X-Requested-With:XMLHttpRequest
User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36
Content-Type:application/x-www-form-urlencoded; charset=UTF-8
Referer:http://cet-bm.neea.edu.cn/Home/QuickPrintTestTicket
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9'''
def getHeaders(raw_head):
    headers = {}
    for raw in raw_head.split('\n'):
        headerkey, headerValue = raw.split(':', 1)
        headers[headerkey] = headerValue
    return headers

Request_header = getHeaders(login_head)
print(Request_header)
url = "http://cet-bm.neea.edu.cn/Home/"
form_data = {
    'IDNumber': '371522200011047856',
    'IDTypeCode': '1',
    'Name': '马长银',
    'provinceCode': '11',
    'verificationCode': ''
}

Page_url = url + "QuickPrintTestTicket"
s = requests.session()

page = s.get(Page_url)

pic = s.get(url + 'VerifyCodeImg').content
with open('Ver_CodeImg.png', 'wb') as f:
    f.write(pic)

ver_code = input("请输入验证码：")
form_data['verificationCode'] = ver_code
print(form_data)
# Page_Detail = BeautifulSoup(page.text, 'lxml')
res = s.post(Page_url, form_data, headers = Request_header)

# print(page.text)
print(res.text)