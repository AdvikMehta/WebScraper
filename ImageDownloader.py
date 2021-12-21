from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time
from os import mkdir

def getImagesFromGoogle(wd, delay, maxImages):

    def scrollDown():
        wd.execute_script("window.scrollTo(0, document.body.scrollHeigh);")
        time.sleep(delay)

    imageUrls = set()
    skips = 0
    found = 0

    while len(imageUrls) + skips < maxImages:
        scrollDown()

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(imageUrls) + skips:maxImages]:
            try:
                img.click()
                time.sleep(delay)
            except Exception as e:
                print("Error: ", e)
                continue
            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute('src') in imageUrls or ('http' not in image.get_attribute('src')):
                    maxImages += 1
                    skips += 1
                    # print("Skipped")
                    continue
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    imageUrls.add(image.get_attribute('src'))
                    # print("Found image!")
                    found += 1
        print("Found", found, "images")
        print("Checked", (found+skips), "images")
        return imageUrls

def downloadImage(downloadPath, url, fileName):
    try:
        imageContent = requests.get(url).content
        imageFile = io.BytesIO(imageContent)  # storing in bytes, need to onvery to img to store
        image = Image.open(imageFile)
        filePath = downloadPath + fileName

        with open(filePath, "wb") as f:
            image.save(f, "JPEG")
        return 1
    except Exception as e:
        print("Failed: ", e)
        return 0

def downloadImages(wd, delay, max, searchField="imgs"):
    urls = getImagesFromGoogle(wd, delay, max)
    c = 1
    success = 0
    pathName = "imgs/" + searchField + "/"
    try:
        mkdir(pathName)
    except FileExistsError:
        pass

    for url in urls:
        fileName = "img" + str(c) + ".jpg"
        success += downloadImage(pathName, url, fileName)
        c += 1
    print("Successfully downloaded", success, "images")
