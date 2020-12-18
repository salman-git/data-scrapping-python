#charcoal, outfitters, gulahmad, chenone, stylo, khaadi, bareeze


url = 'https://www.khaadi.com/pk'
image_folder = './images/'

import requests
from bs4 import BeautifulSoup as soup
import time
import os

image_name = 1
for i in range(1, 12):
    print("retrieving page " + str(i))
    url = 'https://www.khaadi.com/pk/woman.html?p=' + str(i) + '&product_list_limit=45'

    r = requests.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}, timeout=15)
    content = r.content
    r.close()
    page = soup(content, "html.parser")

    product_images = page.find_all("img", class_="product-image-photo")
    print("total images: " + str(len(product_images)))
    for p in product_images:
        print('retrieving image')
        src = p.get('src')
        try:
            imagefile = open(image_folder + str(image_name) + ".jpg", "wb")
            print('saving ' + imagefile.name)
            imagefile.write(requests.get(src, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}, timeout=15).content)
            imagefile.close()
            print("[done]")
        except:
            print('an error occured while retrieving file')
        image_name += 1
        time.sleep(1)
    time.sleep(1)    

print("Crawling completed")