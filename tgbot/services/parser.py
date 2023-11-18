import re

from selenium import webdriver
from bs4 import BeautifulSoup
import time

way = r"C:\Users\kotwi\Downloads\geckodriver-v0.33.0-win64\geckodriver.exe"
options = webdriver.FirefoxOptions()
options.set_preference("javascript.enabled", True)

browser = webdriver.Firefox(executable_path=way, options=options)

def getLinks():
    browser.get('https://uippno.upft.ru/shop#/')
    time.sleep(5)

    html_code = browser.page_source
    soup = BeautifulSoup(html_code, 'html.parser')

    titles = soup.find_all(class_="v-col-sm-12 v-col-md-6 v-col-lg-6 v-col-xl-4 v-col")
    links = []


    for title in titles:
        title_title = title.find_all(class_="directions__title")

        link_tag = title.find('a', class_="directions__link")
        link_title = link_tag.get("href")

        arr = [title_title[0].text, link_title]
        links.append(arr)

    return links

def getCoursesLink(links):
    coursesInfo = []

    for link in links:
        url = "https://uippno.upft.ru/shop"+str(link[1])
        browser.get(url)
        time.sleep(5)

        html_code = browser.page_source
        soup = BeautifulSoup(html_code, 'html.parser')

        courses_div = soup.find_all(class_="v-card v-theme--light v-card--density-default v-card--variant-elevated courses__card")
        for course_div in courses_div:
            course = {}
            course["title"] = link[0]

            link_tag = course_div.find('a', class_="courses__link")
            link_title = link_tag.get("href")

            url = "https://uippno.upft.ru/shop" + str(link_title)
            course["link"] = url

            name = course_div.find_all(class_="courses-title")
            course["name"] = name[0].text

            price = course_div.find_all(class_="courses__price")
            if price == []:
                price = course_div.find_all(class_="courses__price-none")
                priceNum = None
            else:
                priceNum = int(re.sub(r'\D', '', price[0].text)[:-2])

            course["price"] = price[0].text
            course["priceNum"] = priceNum

            hours = course_div.find_all(class_="courses__time")
            try:
                hoursNum = int(re.sub(r'\D', '', hours[0].text))
            except Exception as e:
                hoursNum = None

            course["hours"] = hours[0].text
            course["hoursNum"] = hoursNum

            coursesInfo.append(course)

    return coursesInfo



links = getLinks()
coursesLinks = getCoursesLink(links)


browser.quit()
