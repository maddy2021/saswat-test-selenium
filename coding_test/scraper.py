from datetime import datetime
import json
from lib2to3.pgen2 import driver
from locale import currency
import os
from statistics import mode
from telnetlib import STATUS
import webbrowser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from abt_items import AbtItems
from webdriver import WebDriver
from urllib.error import HTTPError
from time import sleep
import csv
import chompjs
from urllib.parse import urlparse
import argparse
import re
import constants as CONSTANTS

dirname, filename = os.path.split(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(dirname,"output")


# url = "https://www.abt.com/Apple-128GB-Starlight-iPhone-13-Cellular-Phone-ML953LLA6163D/p/168479.html"

def get_product_name(browser: WebDriver,json_data):
    name = ""
    try:
        if("name" in json_data):
            name = json_data["name"]
        if not name:
            name = browser.driver.find_element(by=By.ID,value=CONSTANTS.PRODUCT_TITLE_ID).text
        if name:
            return name.strip()
        return name
    except:
        print("Not able to find product title")
        return name

def get_brand_model(json_data):
    brand = ""
    model = ""
    try:
        if("brand" in json_data and "name" in json_data["brand"]):
            brand = json_data["brand"]["name"]
        if("model" in json_data):
            model = json_data["model"]
        return brand, model
    except:
        print("Not able to find brand or model")
        return brand,model

def get_upc_sku(json_data):
    sku = ""
    upc = ""
    try:
        if("productID" in json_data):
            upc = json_data["productID"]
            upc = re.search("\d{12}",upc).group(0)
        # by looking at json, have took value of sku
        if("sku" in json_data):
            sku = json_data["sku"]
        return upc,sku
    except:
        print("Not ale to find brand or model")
        return upc, sku

def get_buy_box_message(browser:WebDriver):
    buy_box_message = ""
    try:
        buy_box_message = browser.driver.find_element(by=By.ID,value=CONSTANTS.BUY_BOX_MESSAGE_ID).text
        if buy_box_message:
            return buy_box_message.strip()
        return buy_box_message
    except:
        print("Not able to find buy box message")
        return ""

def get_category(browser:WebDriver,json_data):
    category = []
    try:
        if('breadcrumb' in json_data and 'itemListElement' in json_data['breadcrumb']):
            for data in json_data['breadcrumb']['itemListElement']:
                if("item" in data and "name" in data["item"]):
                    category.append(data['item']['name'])
        if not category:
            categories_obj = browser.driver.find_elements(by=By.XPATH,value=CONSTANTS.BREAD_CRUMB_XPATH)
            if len(categories_obj)>0:
                category.append(categories_obj.text)
        return category
    except:
        print("Not able to find category")
        return category
    
def get_image(json_data):
    image_url = ""
    try:
        if "image" in json_data:
            image_url = json_data["image"]
        return image_url
    except:
        print('Not able to find image url')
        return image_url

def get_all_images(browser:WebDriver):
    images = []
    try:
        images_obj = browser.driver.find_elements(by=By.XPATH,value=CONSTANTS.IMAGE_GALLARY_XPATH)
        for img in images_obj:
            images.append(img.get_attribute(CONSTANTS.HREF_ATTRIBUTE))
        return images
    except:
        print("Not able to find gallary of images of products")
        return images


def get_short_desc(browser:WebDriver):
    short_desc = ""
    try:
        short_desc = browser.driver.find_element(by=By.XPATH,value=CONSTANTS.DESCRIPTION_XPATH).text
        return short_desc
    except:
        print("Not able find description")
        return short_desc

    

def get_price_currency(json_data):
    price = ""
    currency = ""
    try:
        if "offers" in json_data:
            if("price" in json_data["offers"]):
                price = json_data["offers"]["price"]
            if("priceCurrency" in json_data["offers"]):
                currency = json_data["offers"]["priceCurrency"]
        return price,currency
    except:
        print('Not able to find price or currency')
        return price,currency
    

def get_varients(browser:WebDriver):
    varients = []
    try:
        dom_varients = browser.driver.find_elements(by=By.XPATH,value=CONSTANTS.VARIENTS_XPATH)    
        for varient in dom_varients:
            varients += varient.text.strip().split("\n")
        return varients
    except:
            print("Not able to find varients")
            return varients

def get_buyer_rating(browser:WebDriver):
    buyer_rating = ""
    try:
        buyer_rating = browser.driver.find_element(by=By.XPATH, value=CONSTANTS.BUYER_RATING_XPATH).text
        return buyer_rating
    except:
        print("Not able to find buyer rating")
        return buyer_rating
    
def get_buyer_reviews(browser:WebDriver,buyer_rating):
    out_of = re.search(CONSTANTS.RATING_SATAR_REGEX,buyer_rating,re.IGNORECASE).group(0)
    buyer_review = {
        "out of 5" : re.search("\d{1}",out_of).group(0)
    }
    try:
        buyer_review_obj = browser.driver.find_elements(by=By.XPATH, value=CONSTANTS.REVIEW_SECTION_XPATH)
        previous_key = ""
        for review in buyer_review_obj:
            if re.search(CONSTANTS.RATING_SATAR_REGEX,review.text,re.IGNORECASE):
                previous_key = re.search(CONSTANTS.RATING_SATAR_REGEX,review.text,re.IGNORECASE).group(0)
                buyer_review[previous_key] = ""
            else:
                buyer_review[previous_key] = review.text
        return [buyer_review]
    except:
        print("Not able to find buyer reviews")
        return [buyer_review]

        
def scrape_abt_data(browser:WebDriver,url):
    browser.driver.get(url)
    html = browser.driver.find_element(by=By.TAG_NAME,value='html')
    lang = html.get_attribute(CONSTANTS.LANG_ATTRIBUTE)
    html.send_keys(Keys.END)
    sleep(5)
    # html_source = browser.driver.page_source
    # with open("source.html","w+",encoding="utf-8") as fp:
    #     fp.write(html_source)
    current_url = browser.driver.current_url
    item = AbtItems(url=current_url)
    if lang:
        item.lang = lang
    price_container_script = browser.driver.find_element(by=By.XPATH,value=CONSTANTS.PRODUCT_AND_PRICE_SCRIPT_XPATH)
    bread_crumb_script = browser.driver.find_element(by=By.XPATH,value=CONSTANTS.BREAD_CRUMB_SCRIPT_XPATH)
    price_container_json = chompjs.parse_js_object(price_container_script.get_attribute(CONSTANTS.INNER_HTML_ATTRIBUTE))
    bread_crumb_json = chompjs.parse_js_object(bread_crumb_script.get_attribute(CONSTANTS.INNER_HTML_ATTRIBUTE))
    item.title = get_product_name(browser,price_container_json)
    item.brand,item.model= get_brand_model(price_container_json) 
    item.upc,item.sku = get_upc_sku(price_container_json) 
    # Assuming asin, eseller_id, productId/upc are same
    item.asin = item.upc
    item.reseller_id = item.upc
    # upc =  "".join([data[1] for data in price_container_json["productID"].split(":") if data[0].lower()=="upc"])
    item.buybox_message = get_buy_box_message(browser)
    item.categories = get_category(browser,bread_crumb_json)
    item.image_url = get_image(price_container_json)
    item.image_urls = get_all_images(browser)
    item.stie = urlparse(url).netloc
    item.site_product_id = item.model
    item.short_description = get_short_desc(browser)
    price,currency = get_price_currency(price_container_json)
    item.price_ammount = price
    item.now_price = item.price_ammount
    item.buyer_ratings = get_buyer_rating(browser)
    if(currency):
        item.price_currency = currency
    item.variants = get_varients(browser)
    item.buyer_reviews = get_buyer_reviews(browser,item.buyer_ratings)
    item.crawled_at = datetime.now().strftime(CONSTANTS.DATE_FORMAT)
    item.status = 200
    # print(item.__dict__)
    return item.__dict__


if __name__=="__main__":
    # start_time = time()
    parser = argparse.ArgumentParser("simple_example")
    parser.add_argument("url", help="pass the url for scraping", type=str)
    args = parser.parse_args()
    if(args.url):
        browser = WebDriver("ChromeDriver")
        try:
            if(browser.driver):
                result = scrape_abt_data(browser,url=args.url)
                result_data = json.dumps(result,indent=3)
                browser.driver.close()
                print(result_data)
                with open(OUTPUT_PATH+"/example.json","w+") as fp:
                    json.dump(result,fp)
            else:
                print("please provide valid driver")
        except:
            print("something is wrong, need to fix it")
            
            