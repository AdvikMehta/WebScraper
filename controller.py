import ImageDownloader as Id
from selenium import webdriver
from selenium.webdriver.common.by import By

PAGE_URL = "https://www.google.com/imghp?hl=en"

def getInput():
    searchField = input("What images would you like to see?: ")
    maxImages = int(input("How many images do you want?: "))
    return searchField, maxImages

def googleSearch(userInput):
    searchField, maxImages = userInput[0], userInput[1]
    PATH = "/Users/advikmehta/Desktop/PycharmProjects/ImageScraperBot/chromedriver"
    wd = webdriver.Chrome(PATH)
    wd.get(PAGE_URL)

    # finding search box and searching with keyword
    ele = wd.find_element(By.NAME, "q")
    ele.send_keys(searchField)
    ele.submit()

    # downloading images
    Id.downloadImages(wd, 1, maxImages, searchField)
    wd.quit()

googleSearch(getInput())