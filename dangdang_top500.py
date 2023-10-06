import requests
from bs4 import BeautifulSoup
import xlwt


# get dangdang datas
def request_dangdang(page):
    url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/116.0.0.0 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.text
    except requests.RequestException:
        return None


# output data
def write_to_excel(soup):
    list = soup.find(class_='bang_list').find_all('li')
    for item in list:
        try:
            item_title = item.find(class_='name').find('a').get('title')
            item_img = item.find(class_='pic').find('a').find('img').get('src')
            item_author = item.find(class_='publisher_info').find('a').string
            item_comment = item.find(class_='biaosheng').find('span').string
        except:
            item_title = 'NO TITLE'
            item_img = 'NO IMAGE'
            item_author = 'NO AUTHOR'
            item_comment = 'NO COMMENT'
        # 写入excel
        global item_cnt
        sheet.write(item_cnt, 0, item_title)
        sheet.write(item_cnt, 1, item_img)
        sheet.write(item_cnt, 2, item_author)
        sheet.write(item_cnt, 3, item_comment)
        item_cnt += 1
        print('爬取数据：' + ' | ', item_title, ' | ', item_img, ' | ', item_author, ' | ', item_comment)

def save_to_excel():
    book.save('当当top500.xls')

if __name__ == '__main__':
    item_cnt = 1  # excel文件中的行数
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('当当top500', cell_overwrite_ok=True)
    sheet.write(0, 0, '书本标题')
    sheet.write(0, 1, '图片')
    sheet.write(0, 2, '作者')
    sheet.write(0, 3, '评论数')  # construct sheet style

    for i in range(1, 26):
        html_text = request_dangdang(i)
        soup = BeautifulSoup(html_text, 'lxml')  # interpret data
        write_to_excel(soup)

    save_to_excel()