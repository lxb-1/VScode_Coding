from cgitb import html
import codecs
import csv
import json
import re
from bs4 import BeautifulSoup
import urllib, urllib.request
import xlwt, xlrd
import pandas

def main():
    # 爬取网站网址
    base_url = 'https://movie.douban.com/top250?start='
        
    # 保存爬取网页电影信息的路径
    save_path = r'./Films_Top250.xls'

    # 调用access_URL()函数，将爬虫访问由python访问，伪装成网页爬取过程，以防止被豆瓣反爬虫
    access_URL("https://movie.douban.com/top250?start=0")

    # 爬取网页
    data_list = getData(base_url)

    # 保存爬取数据
    saveData(data_list, save_path)

    # 将存储爬取信息的Excel文件格式转换为CSV格式
    Excel2Csv()

    # 将存储爬取信息的Excel文件格式转换为json格式
    Excel2Json()

# 定义全局变量

# 下面使用re模块的compile方法，生成正则表示对象，用于快速锁定目标内容，
# 为findall方法提供查找参数：

# 影片详情链接正则表达式对象
search_Link = re.compile(r'<a href="(.*?)">')
# 影片图片正则表达式对象
search_ImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
# 影片片名正则表达式对象
search_Title = re.compile(r'<span class="title">(.*)</span>')
# 影片评分正则表达式对象
search_Rating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 影片评价人数正则表达式对象
search_Eva_num = re.compile(r'<span>(\d*)人评价</span>')
# 影片概况正则表达式对象
search_Inq = re.compile(r'<span class="inq">(.*)</span>')
# 影片其他相关内容正则表达式对象
search_Other = re.compile(r'<p class="">(.*?)</p>', re.S)



# 获取网页数据函数，并返回数据列表
def getData(base_url):
    # 10页(每页25部电影)的全部电影信息
    all_film_data = []
    
    # 由于access_URL()函数一次只能访问一个页面，但是我们要访问多个网页，
    # 所以这里使用for循环实现0-10个网页的访问
    for i in range(0, 10):
        # (1)获取每个网页的全部内容：
        # 由于豆瓣电影每个网页包含25个电影信息，所以每次网页的起始点变化
        # 情况如下所示：
        url = base_url + str(i*25)  # 调用获取网页信息的函数10次
        # 调用access_URL函数访问每个页面的内容
        html = access_URL(url)      # 保存获取到的网页源码

        # (2)逐一解析数据：
        # 使用美味汤包得到网页内容的树形结构soup
        soup = BeautifulSoup(html, "html.parser")
        
        # 使用for循环遍历soup并提取想要的内容项，
        # 并通过find_all方法查找符合要求的字符串，形成列表
        for item in soup.find_all('div', class_="item"):
            film_data = []   # 以列表形式存放电影的所有信息
            
            # 将提取的item转换为字符串形式，以便用正则表达式处理
            item = str(item)
            
            # re库用来通过正则表达式查找指定的字符串
            # 影片详情链接，并添加到data列表中
            film_Link = re.findall(search_Link, item)[0]
            film_data.append(film_Link)

            # 影片图片，并添加到data列表中
            film_ImgSrc = re.findall(search_ImgSrc, item)[0]
            film_data.append(film_ImgSrc)
            
            # 影片名，由于影片只包含中文，还有英文所以，这里需要通过条件判断语句，
            # 只提取中文名字，最终添加到data列表中
            film_Titles = re.findall(search_Title, item)
            if(len(film_Titles) == 2):
                # 影片中文名，并添加到data列表中
                chinese_Title = film_Titles[0]
                film_data.append(chinese_Title)

                # 影片英文名,并添加到data列表中
                en_Tile = film_Titles[1].replace("/", "")   # 去掉前面的/
                film_data.append(en_Tile)

            else:
                film_data.append(film_Titles[0])
                film_data.append(' ')    # 外文名留空

            # 影片评分,并添加到data列表中
            film_Rating = re.findall(search_Rating, item)[0]
            film_data.append(film_Rating)

            # 影评人数,并添加到data列表中
            film_Eva_num = re.findall(search_Eva_num, item)[0]
            film_data.append(film_Eva_num)

            # 影片概述
            film_Inq = re.findall(search_Inq, item)
            # 由于有的电影没有概述,所以这里要进行判断,并分别对待
            if len(film_Inq) != 0:
                film_Inq = film_Inq[0].replace('。', " ")
                film_data.append(film_Inq)
            else:
                film_data.append(" ")

            # 影片其他内容
            film_Other = re.findall(search_Other, item)[0]
            film_Other = re.sub('<br(\s+)?/>(\s+)?', " ", film_Other)    # 去掉<br/>
            film_Other = re.sub('/', " ", film_Other)   # 去掉/,用空格代替
            film_data.append(film_Other.strip())     # 使用strip方法去掉多余空格

            # data是一部电影的全部信息,将data信息放入到全部电影列表all_film_data列表中
            all_film_data.append(film_data)
    # print(all_film_data)
    return all_film_data



# 定义一个得到指定一个URL网页内容的函数
def access_URL(url):
    # 豆瓣的user_agent，用于伪装Python访问网页形式为正常的网页访问形式，防止被反爬虫。
    # 即告诉了豆瓣服务器，我们是是什么类型的机器、浏览器（本质上告诉浏览器，我们可以接受什么水平的文件内容）。
    # 模拟浏览器头部信息，向豆瓣服务器发送消息
    header_user_agent = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}

    # 伪装网址
    fake_req_website = urllib.request.Request(url, headers=header_user_agent)

    html = ""

    try:
        response = urllib.request.urlopen(fake_req_website)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html

# 保存数据函数，以excel表格形式存储
def saveData(data, save_path):
    # (1) 创建以utf-8编码的一个Excel对象
    excel_book = xlwt.Workbook(encoding='utf-8', style_compression=0)

    # (2) 创建一个Sheet表及列名
    excel_sheet = excel_book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
    col = ('影片链接', '图片链接', '中文名', '英文名', '评分', '影评数', '概况', '其他信息')

    # (3) 向excel单元格内写入内容
    # 首先，使用for循环写入8个列名
    for i in range(0, 8):
        excel_sheet.write(0, i, col[i])

    # 然后，使用for循环写入250行爬取的数据
    for i in range(0, 250):
        data_list = data[i]
        for j in range(0, 8):
            excel_sheet.write(i+1, j, data_list[j])

    # 保存包含影片爬取信息的excel文件到指定的路径中
    excel_book.save(save_path)

# excel文件转换为csv文件的函数
def Excel2Csv():
    # 打开excel文件，本脚本存储excel文件在当前目录
    excel_book = xlrd.open_workbook('Films_Top250.xls')
    excel_sheet = excel_book.sheet_by_index(0)

    with codecs.open('Films_Top250.csv', 'w', encoding='utf-8') as f:
        csv_write = csv.writer(f)
        for row_num in range(excel_sheet.nrows):
            row_value = excel_sheet.row_values(row_num)
            csv_write.writerow(row_value) 


# excel文件转json的函数
def Excel2Json():
    ## 打开excel文件，本脚本存储excel文件在当前目录
    #excel_book = xlrd.open_workbook('Films_Top.xls')
    #excel_sheet = excel_book.sheet_by_index(0)

    # 通过pandas包读取爬取的excel表格形式的电影信息
    excel_data_pd = pandas.read_excel('Films_Top250.xls')

    # 将excel_data_pd转换为json格式
    json_data = excel_data_pd.to_json()

    with open('Films_Top250.txt', 'w', encoding='utf-8') as f:
        json.dump(json_data, f)


if __name__ == "__main__":      # 当程序执行时
    # 调用函数
    main()
