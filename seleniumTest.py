# details from https://github.com/SeleniumHQ/docker-selenium/tree/selenium-3 

# Release
# docker run -d -p 4444:4444 --shm-size=2g selenium/standalone-chrome:3.141.59-20210929

# Debug: VNC on 127.0.0.1:5900 
# docker run -d -p 4444:4444 -p 5900:5900 --shm-size=2g selenium/standalone-chrome-debug:3.141.59-20210929

from selenium import webdriver

import time

print('Test Execution Started')

options = webdriver.ChromeOptions()

options.add_argument('–ignore-ssl-errors=yes')

options.add_argument('–ignore-certificate-errors')

driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)

driver.maximize_window()

time.sleep(10)

driver.get('https://www.testsigma.com/')

time.sleep(10)

driver.find_element_by_link_text('Testsigma Cloud').click()

time.sleep(10)

driver.close()

driver.quit()

print('Test Execution Completed Successfully!')