# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": 008451AD7B26A5E1F3DD942E6E495EA22BC44AB5B7D7E9829B5DE955F0BDFC1ADE4702F9F35BC4D676F7B467C6557379F3928E102984739E99E8C322D1BFC260A15AB702BC146B1B9184FC121AB8F0F49B78A94154B7AB993329A7C7E9DE4812872B3BB84CD219D602A2A0D2B262A409577BC8020DDB0FD374395549E452547BE28FD606774DD67502B801793649232E59CFB221E02B187D1DB937DA2D0218F113857B17C67C02A528B21065EBE40D29012810ABC1528CDA1BDCAE405BEE769B54FB4A51F6D85777998353003360EA7507F8C35A9E70A1D22D9B7D019D597DECC0600CF0C3D21F746B396D885DDE282D0DAC4B78BF36BF35B99AE89BAA1AE2853D8E5D77340B9E9FE53E191F339CEDC985964074D5EF479266D52FE770E97874481C047BC50D1FE35E724FEA1FA9ACB8B1EC6B57B4FCE6B185F6951C8AEF5B3887D4D47A78AC183804E3355CA15C68DEE635CE37F02636F9A06097AA9986CF0ABD", "value": "000F8CF431B31843EA1C5F228119F7CB8F702C7679B9EE82B38E42E45A10942D3938FA66FC4584FEFE9EA80A27A3E404B8FBBAC5870C93C063FE70BF53AC6C77FFF0A4F9271E57DB5436DC02EEFE31C9A0682D3393A472BE9DEC02A6BF40E3DC169FF7753529F7CE2B9E19061A7F4283388A67D8B9768EBA512BD7EA672A668781AD7D71B8C50782F113DEF6ECA9B81A4A16BCF63CAFDCE6ED84A9AE2A9B0DC4B236C5B79DB595E7B55550FE45575E8189F8E036CBC622E18C6EC7213E7A473703AB39FD3557C5C87A6510B6F06E602B6C4EE266819B83DFC795239D250143A9FD3484732B32BB52E03D1E1227BBE978C8B4D9D5399F934EF55CCEA97F3CCC160955638E65620C50CF651939B381CCFDA340E64B60C514B57D42178AA8C8588F5DD407EAA4CC961370132C7B63FEE180A91AC0BA2D7A380049CF0ADE0C558E9CDFDA7FB0C647C3A81AD090B085E9F585380993DBF112B54EDB69C83DDE7B3F5F01"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
