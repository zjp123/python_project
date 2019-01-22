from selenium import webdriver

driverpath = r'/home/zhangjunpeng/chromedrive/geckodriver'

driver = webdriver.Firefox(executable_path=driverpath)

driver.get('https://wwww.baidu.com')
print(driver.page_source)
