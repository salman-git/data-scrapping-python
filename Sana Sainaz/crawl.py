#charcoal, outfitters, gulahmad, chenone, stylo, khaadi, bareeze


pg = 1
url = 'https://www.sanasafinaz.com/pk/ready-to-wear.html?p=' + str(pg)
image_folder = './images/'

import requests
from bs4 import BeautifulSoup as soup
import time
import os

image_name = 1
for x in range(8):
    print ('retrieving url...')
    url = 'https://www.sanasafinaz.com/pk/ready-to-wear.html?p=' + str(x + 1)
    r = requests.get(url)
    content = r.content
    r.close()
    page = soup(content, "html.parser")
    print("Loading page " + str(x+1))
    divs = page.find_all("div", class_="products wrapper grid products-grid")
    d = divs[1]
    images = d.ol.find_all("img")
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


