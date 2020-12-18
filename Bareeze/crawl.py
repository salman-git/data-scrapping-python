#charcoal, outfitters, gulahmad, chenone, stylo, khaadi, bareeze


image_folder = './images/'

import requests
from bs4 import BeautifulSoup as soup
import time
import os

image_name = 1
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
for x in range(100):
    print ('retrieving url...')
    url = 'https://www.bareeze.com/pk/collection.html?p=' + str(x + 1)
    r = requests.get(url, headers=headers)
    content = r.content
    r.close()
    page = soup(content, "html.parser")
    print("Loading page " + str(x+1))
    anchors = page.find_all("a", class_="product-image")
    for a in anchors:
        print('retrieving image')
        src = a.img.get('src')
        try:
            imagefile = open(image_folder + str(image_name) + ".jpg", "wb")
            print('saving ' + imagefile.name)
            imagefile.write(requests.get(src, headers=headers).content)
            imagefile.close()
            print("[done]")
        except:
            print('an error occured while retrieving file')
        image_name += 1
        time.sleep(1)
    time.sleep(1)    


