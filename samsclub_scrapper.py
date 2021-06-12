
from os import error
import urllib.request as request
from bs4 import BeautifulSoup
import json
import csv
from time import sleep, ctime
import random
import copy 
import getopt, sys

def openURL(url, parse=False):
    print("INFO: Sending Request...")
    response = request.urlopen(url)
    html = response.read()
    if parse:
        html = BeautifulSoup(html, "html.parser")
    return html

def saveFile (html, file_name):
    with open(file_name, 'w') as file:
        file.write(html.decode('utf-8'))

def saveJsonToCSV(data, filename, permission="w", headers=None, offset=0):
    
    with open(filename, permission) as file:
        def find_value (json_obj, keystring):
            images_root_url = "https://scene7.samsclub.com/is/image/samsclub/"
            NULL = "NULL"
            keys = [key.strip() for key in keystring.split(">")]
            item = copy.deepcopy(json_obj)
            for i, key in enumerate(keys):
                if (type(item) == dict):
                    try:
                        if (key == "image"):
                            item = images_root_url + item[key]
                        else:
                            item = item[key]
                    except:
                        item = NULL
                elif (type(item) == list):
                    values = []
                    for it in item:
                        values.append(find_value(it, '>'.join(keys[i:])))
                    values = list(map(str, values))
                    item = "><".join(values)
                else:
                    return item
            return item

        csv_writer = csv.writer(file)
        if headers is not None and offset == 0:
            csv_writer.writerow(headers)
            headers = None
        rows = []
        root_url = "https://www.samsclub.com"
        for product in data:
            product_id = find_value(product, "productId")
            product_type = find_value(product, 'productType')
            category_name = find_value(product, 'category>name')
            category_id = find_value(product, 'category>categoryId')
            product_name = find_value(product, 'descriptors>name')
            # description = find_value(product, 'descriptors>whyWeLoveIt')
            partial_url = find_value(product, 'searchAndSeo>url')
            product_url = root_url + partial_url
            try:
                product_details = openURL(product_url, parse=True)
            except:
                print("ERROR: Product fetching failed. SKIPPING...")
                pass
            description = product_details.find("div", class_="sc-full-description-long").text or "NULL"
            brand = find_value(product, 'manufacturingInfo>brand')
            images = find_value(product, 'skus>assets>image')
            price_types = find_value(product, "skus>onlineOffer>price>type")
            start_price = find_value(product, "skus>onlineOffer>price>startPrice>amount")
            start_price_cur = find_value(product, "skus>onlineOffer>price>startPrice>currency")
            final_price = find_value(product, "skus>onlineOffer>price>finalPrice>amount")
            final_price_cur = find_value(product, "skus>onlineOffer>price>finalPrice>currency")
            unit_price = find_value(product, "skus>onlineOffer>price>unitPrice>amount")
            unit_price_cur = find_value(product, "skus>onlineOffer>price>unitPrice>currency")
            rows.append([product_id, product_type,category_name,category_id,product_name,description,url,brand,images,price_types,start_price,start_price_cur,final_price,final_price_cur,unit_price,unit_price_cur])
            # price_types = ','.join([sku['onlineOffer']['price']['type'] for sku in product['skus']])
        csv_writer.writerows(rows)
        print("INFO: Records saved to file")
        return True



def dict_key_filter(obj, obj_filter):
    def inner_dict_key_filter(obj): return dict_key_filter(obj, obj_filter)
    def to_keep(subtree): return not isinstance(subtree, (dict, list)) or subtree

    def build_subtree(key, value):
        if key in obj_filter:
            return copy.deepcopy(value) # keep the branch
        elif isinstance(value, (dict, list)):
            return inner_dict_key_filter(value) # continue to search
        return [] # just an orphan value here

    if isinstance(obj, dict):
        key_subtree_pairs = ((key, build_subtree(key, value)) for key, value in obj.items())
        return {key:subtree for key, subtree in key_subtree_pairs if to_keep(subtree)}
    elif isinstance(obj, list):
        return list(filter(to_keep, map(inner_dict_key_filter, obj)))
    return []

if __name__ == "__main__":
    print("Use -h or --help to learn about command line arguments")
    offset = 4469
    records_limit = 48
    category_id = 1444
    filename = "data.csv"
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    # print(argument_list)
    short_options = "c:l:o:f:h"
    long_options = ["category_id=", "records_limit=", "offset=", "filename", "help"]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
        for current_argument, current_value in arguments:
            if current_argument in ("-c", "--category_id"):
                category_id = int(current_value)
            elif current_argument in ("-o", "--offset"):
                offset = int(current_value)
            elif current_argument in ("-l", "--records_limit"):
                records_limit = int(current_value)
            elif current_argument in ("-f", "--filename"):
                filename = current_value

            elif current_argument in ("-h", "--help"):
                print("Arguments details")
                print("------------------")
                print("--category | -c : The category id to fetch products from")
                print("--records_limit | -l : Number of records fetched per request [24, 48]")
                print("--offset | -o : Number of records to skip")
                print("--filename | -f : Name of the csv file to save records")
                print("--help | -h: Show information about command line arguments")
                sys.exit()
    except getopt.error as err:
        print (str(err))
        sys.exit(2)
    permission = "a"
    if offset == 0:
        permission="w"
    else:
        permission="a"
    column_names = ["product_id",
                    "product_type",
                    "category_name",
                    "category_id",
                    "product_name",
                    "description",
                    "url",
                    "brand",
                    "images",
                    "price_types",
                    "start_price",
                    "start_price_cur",
                    "final_price",
                    "final_price_cur",
                    "unit_price",
                    "unit_price_cur"]
    file_saved = False
    try:
        show_total = True
        log_file = open('logs_test.txt', 'a')
        log_file.write(f"New Session: csvfile->{filename} offset->{offset}\n")
        while True:
            url = f"https://www.samsclub.com/api/node/vivaldi/v2/az/products/search?sourceType=1&selectedFilter=all&sortKey=relevance&sortOrder=0&offset={offset}&searchType=PRODUCTS&recordType=primary&searchCategoryId={category_id}&br=true&limit={records_limit}"
            images_root_url = "https://scene7.samsclub.com/is/image/samsclub/"
            response = openURL(url)
            json_response = json.loads(response)
            if json_response['status'] == 'OK':
                payload = json_response['payload']
                if show_total:
                    print("total records in this category ", payload["totalRecords"])
                    show_total = False
                total_count = int(payload['totalRecords'])
                number_of_records = int(payload['numberOfRecords'])
                current_page = int(payload['currentPage'])
                total_fetched_records = offset + number_of_records
                products = payload['records']
                print(f"RESPONSE: retrieved products from {offset + 1}-{offset + records_limit}")
                log_file.write(f"{ctime()}\tRESPONSE: retrieved products from {offset + 1}-{offset + records_limit}\n")
                offset += records_limit
                file_saved = False
                file_saved = saveJsonToCSV(products, filename, permission=permission, headers=column_names, offset=offset)
                permission = "a"
                column_names = None
                if total_fetched_records >= total_count:
                    break

                sleep(random.randint(3, 5))
    except:
        print("RESPONSE: An error occurred while fetching products")
        print(f"INFO: Trying again by restarting the script with offset {offset}")
        import os
        # if file_saved:
        #     os.system(f'python {os.path.basename(__file__)} -f {filename} -o {offset}')
        # else:
        #     os.system(f'python {os.path.basename(__file__)} -f {filename} -o {offset-records_limit}')

    finally:
        log_file.close()

    print('completed')