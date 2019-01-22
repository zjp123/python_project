from selenium import webdriver
from lxml import etree
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class Selboss(object):

    def __init__(self):
        self.driverpath = r'/home/zhangjunpeng/chromedrive/geckodriver'

        self.driver = webdriver.Firefox(executable_path=self.driverpath)
        self.data = []

    def run(self):
        self.driver.get('https://www.lagou.com/')
        #page_source = Selboss.driver.page_source
        #print(self.driver.current_url)

        #print(username)
        self.shuru()

    def shuru(self):
        cha = self.driver.find_element_by_xpath('//button[@id="cboxClose"]')
        cha.click()
        time.sleep(1)
        inputE = self.driver.find_element_by_xpath('//input[@id="search_input"]')
        #print(inputE.get_attribute('placeholder'))
        inputE.send_keys('python')
        # try:
        #     ele = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(By.ID, "search_input"))
        #     ele.send_keys('python')
        #
        # except:
        #     pass
        # finally:
        #     self.driver.quit()
        #inputE = self.driver.find_element_by_xpath('//input[@id="search_input"]')


        #password = self.driver.find_element_by_xpath('//div[contains(@data-propertyname, "password")]/input')
        btn = self.driver.find_element_by_xpath('//input[@id="search_button"]')

        btn.click()
        self.get_url_list(self.driver.page_source)
        #print(self.driver.current_url)

    def get_url_list(self, source):

        html = etree.HTML(source)
        listurl = html.xpath('//ul[@class="item_con_list"]/li//a[@class="position_link"]/@href')
        print(listurl)
        for url in listurl:
            self.get_detail_data(url)


    def get_detail_data(self, url):

        self.driver.execute_script("window.open('%s')"%url)
        self.driver.switch_to_window(self.driver.window_handles[1])
        WebDriverWait(self.driver, timeout=3).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='job-name']/span[@class='name']"))
        )
        html = etree.HTML(self.driver.page_source)
        #print(html.xpath('//div[@class="job-name"]/span[@class="name"]/text()'))
        #self.driver.quit()
        title = html.xpath('//div[@class="job-name"]/span[@class="name"]/text()')
        self.data.append(title)
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[0])
        print(self.data)






if __name__ == '__main__':

        Selboss().run()