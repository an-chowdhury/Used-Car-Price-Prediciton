import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

opt = webdriver.ChromeOptions()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
opt.add_argument("no-sandbox")
opt.add_argument("--disable-gpu")
opt.add_argument("--disable-dev-shm-usage")
opt.add_argument("--incognito")
opt.add_argument("--headless")
opt.add_argument("--disable-xss-auditor")
opt.add_argument("--disable-web-security")
opt.add_argument("--allow-running-insecure-content")
opt.add_argument("--disable-setuid-sandbox")
opt.add_argument("--disable-webgl")
opt.add_argument("--disable-popup-blocking")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 2,
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.geolocation": 2,
    "profile.default_content_setting_values.notifications": 2
})
driver = webdriver.Chrome(options=opt, executable_path=r"C:\Users\chowd\Desktop\Cardekho\chromedriver.exe")

driver.get("https://www.cardekho.com/used-cars+in+kolkata")

ScrollNumber = 200
for i in range(1, ScrollNumber):
    driver.execute_script("window.scrollTo(1,document.body.scrollHeight)")
    time.sleep(5)

file = open('used_car.html', 'w', encoding='utf-8')
file.write(driver.page_source)
file.close()

driver.close()
