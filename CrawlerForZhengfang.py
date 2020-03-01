import re
import urllib.request
import urllib.parse
import http.cookiejar
import bs4
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from PIL import Image

url1 = 'http://zfjw.gdou.edu.cn:8016/'
url2 = 'http://210.38.137.126:8016/'
url3 = 'http://210.38.137.125:8016/'
url4 = 'http://210.38.137.124:8016/'
viewstate1 = ''
viewstate2 = 'dDwxNTMxMDk5Mzc0Ozs+OBE730NQqeUlEYO76T3Qls4CiUo='
viewstate3 = ''
viewstate4 = ''

url = url2
viewstate = viewstate2

cookie = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

# username = input("输入用户名: ")
# password = input("输入密码 ")
username = '201711672114'
password = 'h19981027'

while True:
    params = {
        'txtUserName': username,
        'Textbox1': '',
        'Textbox2': password,
        'RadioButtonList1': '学生',
        'Button1': '',
        'lbLanguage': '',
        'hidPdrs': '',
        'hidsc': ''
    }
    res = opener.open(url + 'CheckCode.aspx').read()
    with open(r'./code.jpg', 'wb') as file:
        file.write(res)
    im = Image.open(r'./code.jpg')
    im.show()
    params['txtSecretCode'] = input('请输入验证码：')
    im.close()
    # response = urllib.request.urlopen(url)
    # html = response.read().decode('gb2312')
    # viewstate = re.search('<input type="hidden" name="__VIEWSTATE" value="(.+?)"', html)
    # print(viewstate)
    # params['__VIEWSTATE'] = viewstate.group(1)
    params['__VIEWSTATE'] = viewstate

    loginurl = url + 'default2.aspx'
    data = urllib.parse.urlencode(params).encode('gb2312')
    response = opener.open(loginurl, data)
    if response.geturl() != url + 'default2.aspx':
        catch = '<span id="xhxm">(.*?)</span>'
        tmpname = re.search(catch, response.read().decode('gb2312'))
        name = tmpname.group(1)
        name = name[:-2]
        break
print(name)
sub_url = ''.join([url, 'xscj_gc.aspx', '?xh=', username,
                   '&xm=', urllib.parse.quote(name), '&gnmkdm=N121613'])
params = {
    'ddlXN': '',
    'ddlXQ': '',
    'Button2': '',
}
req = urllib.request.Request(sub_url)
print(username)
print(sub_url)
req.add_header('Referer', url + 'xs_main.aspx?xh=' + username)
req.add_header('User-Agent',
               'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/63.0.3239.132 Safari/537.36')
response = opener.open(req)
html = response.read().decode('gb2312')
viewstate = re.search('<input type="hidden" name="__VIEWSTATE" value="(.+?)"', html)
print(viewstate.group(1))
params['__VIEWSTATE'] = viewstate.group(1)
req = urllib.request.Request(sub_url, urllib.parse.urlencode(params).encode('gb2312'))
req.add_header('Referer', url + 'default2.aspx')
req.add_header('Origin', url)
response = opener.open(req)
soup = BeautifulSoup(response.read().decode('gb2312'), 'html.parser')
html = soup.find('table', class_='datelist')

print('你的所有成绩如下：')
outColumn = [1, 2, 3, 4, 6, 7, 8]
flag = True

for each in html:
    columnCounter = 0
    column = []
    if (type(each) == bs4.element.NavigableString):
        pass
    else:
        for item in each.contents:
            if (item != '\n'):
                if columnCounter in outColumn:
                    column.append(str(item.contents[0]).strip())
                columnCounter += 1
        if flag:
            table = PrettyTable(column)
            flag = False
        else:
            table.add_row(column)
print(table)
