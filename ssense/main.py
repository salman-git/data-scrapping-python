from requests import get
from bs4 import BeautifulSoup
import os
import urllib
import sys

def download_images(url, image_dir, page_num):
    print("Downloading Images From Page: ", page_num)
    response = get(url)
    if (response.ok):
        page = BeautifulSoup(response.content, 'html.parser')
        product_list = page.findAll("div", {"class": "browsing-product-list"})[0]
        images = product_list.findAll("img", {"class": "product-thumbnail"})
        for i in range(len(images)):
            image_link = images[i]['data-srcset']
            image_ext = image_link[-4:]
            image_path = image_dir + "/" + str(i) + "_p_" + str(page_num) + image_ext
            save_image(image_link, image_path)
    else:
        print("Request failed!")

def save_image(url, path):
    print("...saving image at ", path)
    urllib.request.urlretrieve(url, path)
    # with open(path, 'wb') as handle:
    #         response = get(url, stream=True)
    #         if not response.ok:
    #             print (response)
    #         for block in response.iter_content(1024):
    #             if not block:
    #                 break
    #             handle.write(block)

if __name__=="__main__":
    category = sys.argv[1]
    image_dir = category
    url = 'https://www.ssense.com/en-us/women/'+category

    if not os.path.exists(image_dir):
            os.makedirs(image_dir)
    download_images(url, image_dir, 1)
    response = get(url)
    if (response.ok):
        page = BeautifulSoup(response.content, 'html.parser')
        nav = page.findAll("div", {"class": "browsing-pagination"})
        total_pages = int(list(nav[0].div.nav.ul.children)[-2].text)

        for i in range(2,total_pages):
            url = url + "?page=" + str(i)
            download_images(url, image_dir, i)
    else:
        print("Request Failed!!!")

    print("end")