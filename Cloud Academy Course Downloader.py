from selenium.common.exceptions import NoSuchElementException
import time
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import *
from functools import partial


def send_details(username, password, courseUrl):
    print("username entered printed from ca2.py  :", username)
    print("password entered :", password)
    print("password entered :", courseUrl)

    put_course_name = ("/".join(courseUrl.split("/course")[::-2]))
    print("Working on " + put_course_name)
    DownloadCourse(username, password, courseUrl, put_course_name)
    return


def DownloadCourse(UserName, Password, courseUrl, put_course_name):
    options = webdriver.ChromeOptions()
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.set_capability('unhandledPromptBehavior', 'accept')
    # options.add_argument("--headless")
    options.add_argument("ignore-certificate-errors")
    chromebrowser = 'YOUR_PATH_OF_EXE_FILE\\chromedriver.exe'       #--------------ChromeDriver Path-----------
    browser = webdriver.Chrome(chromebrowser, chrome_options=options)

    browser.get('https://cloudacademy.com/login/')
    username = browser.find_element_by_id("loginform_username")
    password = browser.find_element_by_id("loginform_password")
    username.send_keys(UserName)
    password.send_keys(Password)  # password to go in here
    browser.find_element_by_id("loginSubmit").click()
    course_url = courseUrl
    parent_path = "F:\\cloudAcademy\\"
    time.sleep(10)
    browser.get(course_url)
    course_dir = parent_path + os.path.basename(course_url)
    os.makedirs(course_dir, exist_ok=True)
    elems = browser.find_elements_by_xpath(f"//a[contains(@href,'/course{put_course_name}')]")
    print('href', elems)
    try:
        play_button = browser.find_element_by_xpath('//*[@id="vjs_video_3"]/div[1]/div/div/div/span')
        if play_button.is_displayed() and play_button.is_enabled():
            play_button.click()
            print("Play button found")
    except NoSuchElementException:
        print("Play button not found")
        pass
    time.sleep(8)
    for ii in WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@class='sc-1y1qaby-3 bmoGTH']"))):

        ii.click()
        try:
            play_button = browser.find_element_by_xpath('//*[@id="vjs_video_3"]/div[1]/div/div/div/span')
            if play_button.is_displayed() and play_button.is_enabled():
                play_button.click()
                print("Play button found")
        except NoSuchElementException:
            print("Play button not found")
            pass
        time.sleep(8)
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//video[contains(@id, 'vjs_video')]")))
        src = browser.page_source  # gets the html source of the page

        parser = BeautifulSoup(src, "lxml")  # initialize the parser and parse the source "src"

        tag = parser.findAll('video')  # Get the video tag from the source
        print(tag)
        n = 0  # Specify the index of video element in the web page
        url = tag[n]['src']  # get the src attribute of the video
        print(url)
        import re
        my_new_string = re.sub('[^ a-zA-Z0-9]', '', browser.title)
        time.sleep(2)
        os.makedirs(course_dir + '\\' + my_new_string, exist_ok=True)
        time.sleep(2)
        disassembled = urlparse(url)
        filename = os.path.basename(disassembled.path)
        time.sleep(2)
        fullfilename = os.path.join(course_dir + '\\' + my_new_string, filename)
        time.sleep(2)
        urllib.request.urlretrieve(url, fullfilename)
        time.sleep(15)
    browser.close()  # closes the browser
    print("================")
    print("Course Downloaded")
    print("================")

def validateLogin(username, password, courseUrl):
    send_details(username.get(), password.get(), courseUrl.get())

# window
tkWindow = Tk()
tkWindow.geometry('800x190')
tkWindow.title('Cloud Academy Course Downloader - www.zainulhassan.net')

# username label and text entry box
usernameLabel = Label(tkWindow, text="Email").grid(row=0, column=0)
username = StringVar()
usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1, padx=10, pady=10)

# password label and password entry box
passwordLabel = Label(tkWindow, text="Password").grid(row=1, column=0)
password = StringVar()
passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1, padx=10, pady=10)

# password label and password entry box
courseUrlLabel = Label(tkWindow, text="Complete Course URL ").grid(row=2, column=0)
courseUrl = StringVar()
courseUrlEntry = Entry(tkWindow, textvariable=courseUrl).grid(row=2, column=1, padx=10, pady=10)

Label(tkWindow, text="Make Sure to Add Complete Course URL 'https://cloudacademy.com/course/course-name'").grid(row=2, column=2)
validateLogin = partial(validateLogin, username, password, courseUrl)

# login button
loginButton = Button(tkWindow, text="Download Course", command=validateLogin).grid(row=4, column=0)

tkWindow.mainloop()

if __name__ == "__main__":
    DownloadCourse()
