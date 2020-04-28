import re
import urllib.request
import urllib.parse
import http.cookiejar
import bs4
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from PIL import Image
import pytesseract

url1 = 'http://zfjw.gdou.edu.cn:8016/'
url2 = 'http://210.38.137.126:8016/'
url3 = 'http://210.38.137.125:8016/'
url4 = 'http://210.38.137.124:8016/'
url = url2

cookie = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

username = input("输入用户名: ")
password = input("输入密码 ")

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
    im = im.convert('L')
    threshold = 160  # 设定二值化阈值
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    im = im.point(table, '1')
    im.save('./code_t.jpg')
    im.close
    im = Image.open(r'./code_t.jpg')
    # err:tesseract is not installed or it's not in your path
    # brew install tesseract
    captcha = pytesseract.image_to_string(im)
    captcha = re.sub(r'\W+', '', captcha).strip()
    print('验证码:', captcha)
    im.show()
    im.close

    params['txtSecretCode'] = input('请输入验证码：')
    goalNum = float(input('目标绩点：'))
    badNum = 0
    response = urllib.request.urlopen(url + 'default2.aspx')
    html = response.read().decode('gb2312')
    viewstate = re.search('<input type="hidden" name="__VIEWSTATE" value="(.*?)" />', html)
    params['__VIEWSTATE'] = viewstate.group(1)
    print(params['__VIEWSTATE'])

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
# 成绩查询
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
viewstate = re.search('<input type="hidden" name="__VIEWSTATE" value="(.*?)"', html)
params['__VIEWSTATE'] = viewstate.group(1)
req = urllib.request.Request(sub_url, urllib.parse.urlencode(params).encode('gb2312'))
req.add_header('Referer', url + 'default2.aspx')
req.add_header('Origin', url)
response = opener.open(req)
# 筛选table内容
soup = BeautifulSoup(response.read().decode('gb2312'), 'html.parser')
html = soup.find('table', class_='datelist')

outColumn = [1, 2, 3, 4, 6, 7, 8]
flag = True
itemCounter = 0
grade = {'total': 0.0}
saveYears = ''
print('你的所有成绩如下：')
for each in html:
    columnCounter = 0
    column = []
    if type(each) == bs4.element.NavigableString:
        pass
    else:
        for item in each.contents:
            if item != '\n':
                if (columnCounter == 0) & (flag is False):
                    years = str(item.contents[0]).strip()
                    if years not in grade.keys():
                        if saveYears != '':
                            grade[saveYears] = grade[saveYears] / yearsCounter
                        grade[years] = 0.0
                        yearsCounter = 1
                        saveYears = years
                    else:
                        yearsCounter += 1
                if columnCounter in outColumn:
                    data = str(item.contents[0]).strip()
                    column.append(data)
                    if (columnCounter == 7) & (flag is False):
                        grade[years] += float(data)
                        grade['total'] += float(data)
                        itemCounter += 1
                        if float(data) <= goalNum:
                            badNum += 1
                columnCounter += 1
        if flag:
            # 第一行作为表头
            table = PrettyTable(column)
            flag = False
        else:
            table.add_row(column)
grade[saveYears] = grade[saveYears] / yearsCounter
grade['total'] = grade['total'] / itemCounter
print(table)
print(grade)
print(badNum)
