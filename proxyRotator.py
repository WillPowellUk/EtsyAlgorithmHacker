from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup

class ProxyRotator:
    def __init__(self,  option=''): 
        self.proxyIndex = -1
        self.option = option

    # main fn
    def rotate(self):
        # gets new proxy list
        self.filter_proxies()

        # gets new proxy from list
        self.get_new_proxy()

        # creates proxy driver
        self.create_proxy_driver()

        # returns proxy if working
        return self.get_content()

    def get_new_proxy(self):
        # if proxy index is less than 0, reset
        if self.proxyIndex < 0:
            self.proxyIndex = len(self.proxies) - 1
        # get new proxy and update index
        self.new_proxy = self.proxies.pop(self.proxyIndex)
        self.proxyIndex = self.proxyIndex - 1


    def filter_proxies(self):   
        response = requests.get('https://www.sslproxies.org/')
        soup = BeautifulSoup(response.text,"html.parser")
        self.proxies = []
        for item in soup.select("table.table tbody tr"):
            if not item.select_one("td"):break
            ip = item.select_one("td").text
            port = item.select_one("td:nth-of-type(2)").text
            self.proxies.append(f"{ip}:{port}")


    def create_proxy_driver(self):
        options = Options()
        options.add_argument('–ignore-ssl-errors=yes')
        options.add_argument('–ignore-certificate-errors')
        options.add_argument(f'--proxy-server={self.new_proxy}')
        if self.option != 'debug':
            options.add_argument('--headless')
        self.driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
        self.driver.set_page_load_timeout(10)


    def get_content(self):
        while True:
            # try accessing google
            try:
                self.driver.get("https://www.example.com/")
                title = self.driver.find_element(By.XPATH, "/html/body/div/h1").text
                if title:
                    print("Proxy Running: %s" % self.new_proxy)
                    return self.driver
            except Exception as e:
                if not self.proxies:
                    print("Proxies used up (%s)" % len(self.proxies))
                    self.proxies = self.filter_proxies()

                self.get_new_proxy()
                self.create_proxy_driver()
                print("Trying new proxy: %s" % self.new_proxy)


if __name__ == '__main__':
    proxy = ProxyRotator('debug')
    while True:
        driver = proxy.rotate()
        driver.close()