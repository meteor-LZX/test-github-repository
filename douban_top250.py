import requests
from bs4 import BeautifulSoup
import xlwt

class Spider():

    def __init__(self):
        # 创建excel文件
        self.cnt = 1
        self.book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        self.sheet = self.book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
        self.sheet.write(0, 0, '名称')
        self.sheet.write(0, 1, '图片')
        self.sheet.write(0, 2, '排名')
        self.sheet.write(0, 3, '评分')
        self.sheet.write(0, 4, '作者')
        self.sheet.write(0, 5, '简介')

    '''
    获取豆瓣top250的html文件
    '''
    def request_douban(self, page):
        url = 'https://movie.douban.com/top250?start=' + str(page*25) + '&filter='
        # 请求头必须要有，否则会返回418
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/116.0.0.0 Safari/537.36'
        }
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                return r.text
        except requests.RequestException:
            return None

    '''
    写入结果到excel文件
    '''
    def write_to_excel(self, soup):
        list = soup.find(class_='grid_view').find_all('li')
        for item in list:
            # 获取特定内容
            item_name = item.find(class_='title').string
            item_img = item.find('a').find('img').get('src')
            item_index = item.find(class_='').string
            item_score = item.find(class_='rating_num').string
            item_author = item.find('p').text
            # inq标签有可能为空
            try:
                item_intr = item.find(class_='inq').string
            except:
                item_intr = 'EMPTY'
            # 写入文件
            self.sheet.write(self.cnt, 0, item_name)
            self.sheet.write(self.cnt, 1, item_img)
            self.sheet.write(self.cnt, 2, item_index)
            self.sheet.write(self.cnt, 3, item_score)
            self.sheet.write(self.cnt, 4, item_author)
            self.sheet.write(self.cnt, 5, item_intr)
            self.cnt += 1
            # 打印输出
            print('爬取电影：' + item_index + ' | ' + item_name + ' | ' + item_score + ' | ' + item_intr)

    '''
    保存excel文件
    '''
    def save_to_excel(self):
        self.book.save('豆瓣top250.xls')

if __name__ == '__main__':
    s = Spider()
    for page in range(10):
        html_text = s.request_douban(page)
        soup = BeautifulSoup(html_text, 'lxml')  # interpret datas
        s.write_to_excel(soup)
    s.save_to_excel()
