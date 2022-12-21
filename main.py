import os
import sys
import time
import platform
import configparser
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from Screenshot import Screenshot
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

if platform.system() == 'Darwin':
    crop = (150, 290, 1850, 950)
else:
    crop = (70, 150, 950, 500)

cf = configparser.ConfigParser()
cf.read(os.getcwd() + "/conf.ini")
url = cf.get('credential', "url")
user = cf.get('credential', "email")
pw = cf.get('credential', "password")
channelId = cf.get('credential', "channel")
token = cf.get('credential', "token")


def screenshot(fileName, driver):
    ob = Screenshot.Screenshot()
    ob.full_Screenshot(driver, save_path=r'.', image_name='screenshot.png')
    with Image.open("screenshot.png") as im:
        # change numbers to get the area you want to crop
        (left, upper, right, lower) = crop
        im_crop = im.crop((left, upper, right, lower))
        im_crop.save(fileName + ".png", "png")
        print("screenshot: " + fileName + ".png")


# press down arrow key how many times to scroll down
def scrollDown(body, times):
    for i in range(1, times):
        body.send_keys(Keys.DOWN)
        print("press down arrow key")
        time.sleep(1)


def sendToSlack(filepath, msg):
    # if using a HTTPS proxy
    # proxyInfo = 'http://127.0.0.1:24000'
    # client = WebClient(token, timeout=300, proxy=proxyInfo)
    client = WebClient(token, timeout=300)
    try:
        response = client.files_upload_v2(channel=channelId,
                                          file=filepath,
                                          initial_comment=msg)
        print("send to slack: " + filepath + " is ok")
        assert response["file"]  # the uploaded file
    except SlackApiError as e:
        print(e)


def browser(url):
    browser_options = webdriver.ChromeOptions()
    # enable headless mode in linux without GUI
    browser_options.add_argument('--headless')
    browser_options.add_argument("--disable-notifications")
    browser_options.add_argument('--disable-gpu')
    browser_options.add_argument('--no-sandbox')
    browser_options.add_argument('--start-maximized')
    prefs = {"profile.default_content_setting_values.notifications": 2}
    browser_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
    driver.set_window_size(1920, 1080)
    driver.get(url)
    time.sleep(10)

    # no need to login
    if len(user) == 0:
        print("you don't have user and password to login...")
        try:
            screenshot('1', driver)
            body = driver.find_element("xpath", value='/html/body')
            body.click()

            scrollDown(body, 5)
            screenshot('2', driver)
            scrollDown(body, 5)
            screenshot('3', driver)
            driver.quit()

        except Exception as e:
            print("ERROR: {}".format(e))
            driver.quit()
    else:
        try:
            print("using user and password to login...")
            email = driver.find_element(
                "xpath",
                value=
                '//*[@id="reactRoot"]/div[1]/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input'
            )
            email.send_keys(user)

            password = driver.find_element("xpath",
                                           value='//*[@id="current-password"]')
            password.send_keys(pw)

            login = driver.find_element(
                "xpath",
                value=
                '//*[@id="reactRoot"]/div[1]/main/div[3]/div/div[2]/div/div/form/button'
            )
            login.click()
            time.sleep(30)
            screenshot('1', driver)
            body = driver.find_element("xpath", value='/html/body')
            body.click()

            scrollDown(body, 13)
            screenshot('2', driver)
            scrollDown(body, 13)
            screenshot('3', driver)
            driver.quit()

        except Exception as e:
            print("ERROR: {}".format(e))
            driver.quit()


if __name__ == "__main__":
    if len(url) <= 0:
        print("Error: Invalid url, exiting...")
        sys.exit()

    # delete old screenshots
    for item in os.listdir('./'):
        if item.endswith(".png"):
            os.remove(os.path.join('./', item))
    browser(url)

    msgs = ['pic 1 is ....', 'pic 2 is ...',
            'pic 3 is ...']  # the text about the pic

    for i in range(0, len(msgs)):
        sendToSlack(str(i + 1) + '.png', msgs[i])
        time.sleep(8)
