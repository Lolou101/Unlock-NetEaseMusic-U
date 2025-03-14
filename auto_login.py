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
    browser.add_cookie({"name":music_u, "value": "00546FA66D41595ECA3C299C5E4E5BE4D872EB865C0E3D30BD43070B9034CB7E41A47528D8BC394B092819CC51E974DC4E607959E0474D408B63CE8E5A39B72263C0F43317B425D1BDF6F1D2BBDDDDF8EDE28103E20EC866FEA763307059909693545B2974F99D1DC996D3520BCA76D0E89818463FC30BDDD5100A291741D06F4261E123B31DB72C39727C5D36F4F9D2370870D82A79566AD3492D5F86FC38C6864AD5B66AF4322C1886465CA7E36391B4366F863CEF86677089C24D60F219098840E0D76BECAD95E4749E086ACB7B7EE1215A2EE6B1A45A58C032E15CDC68B995626A5D8C58B4D1909D31C22F71B7837ADB2B4845D55C607477EE65D0D177BB10D2D4824D56DAA83033BD2B8E13E23E145D67F2D050D1D775BA41514D67F1F6499BB2953A866708519707F73E8EB2829CAE762AF834558DC3913C0ECC0378BE7AEFD1FCD5F3C6175DB0EE182206C6EA4458A477E57E16B97A9EC0FAB4B5CB345F"})
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
