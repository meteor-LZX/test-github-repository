from selenium import webdriver
import time

def main():
    driver = webdriver.Chrome('chromedriver-win64/chromedriver.exe')
    driver.get('https://www.bilibili.com/')
    


if __name__ == '__main__':
    main()
    time.sleep(3)

