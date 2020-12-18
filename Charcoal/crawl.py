#charcoal, outfitters, gulahmad, chenone, stylo, khaadi, bareeze


url = 'https://www.charcoal.com.pk/'
image_folder = './images/'

import requests
from bs4 import BeautifulSoup as soup
import time
import os

print("Retrieving url...")
r = requests.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}, timeout=15)
content = r.content
r.close()

page = soup(content, "html.parser")

menu = page.find("div", id="menu")  #main navigation menu
menu_anchors = menu.find_all('a', class_="submenu1")  #sub-menu elements in main menu

for anchor in menu_anchors:
    href = anchor['href']
    text = anchor.text

    dir_path = image_folder + text  
    dir_path = dir_path.replace(' ', '_')

    if not os.path.exists(dir_path):    #create directory for each product category if it does not exists
        os.makedirs(dir_path)
    dir_path += '/'

    print('sending request to ' + href)
    #request sub-category
    sub_r = requests.get(href, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}, timeout=15)
    sub_content = sub_r.content
    sub_r.close()

    sub_page = soup(sub_content, "html.parser")
    products = sub_page.find_all("div", class_='product-block-inner') #array of products

    image_name = 1
    for p in products:
        print('retrieving image')
        src = p.img.get('src')
        try:
            imagefile = open(dir_path + str(image_name) + ".jpg", "wb")
            print('saving ' + imagefile.name)
            imagefile.write(requests.get(src, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}, timeout=15).content)
            imagefile.close()
            print("[done]")
        except:
            print('an error occured while retrieving file')
        image_name += 1
        time.sleep(1)
    time.sleep(1)    
