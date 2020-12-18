#charcoal, outfitters, gulahmad, chenone, stylo, khaadi, bareeze


image_folder = './images/'

import requests
from bs4 import BeautifulSoup as soup
import time
import os

image_name = 1
for x in range(10):
    print ('retrieving url...')
    url = 'https://www.almirah.com.pk/women/pret-wear.html?p=' + str(x + 1)
    r = requests.get(url)
    content = r.content
    r.close()
    page = soup(content, "html.parser")
    print("Loading page " + str(x+1))
    images = page.find_all("img", class_="front product-collection-image")
    for img in images:
        print('retrieving image')
        src = img.get('src')
        try:
            imagefile = open(image_folder + str(image_name) + ".jpg", "wb")
            print('saving ' + imagefile.name)
            imagefile.write(requests.get(src).content)
            imagefile.close()
            print("[done]")
        except:
            print('an error occured while retrieving file')
        image_name += 1
        time.sleep(1)
    time.sleep(1)    


