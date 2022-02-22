"""
Impletements and executes functions that scrapes the Soko Glam website for
skincare products data
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

def string_initials(string):
    """
    Returns a string made of the first letters of every word in the given
    string. If the string only contains one word, returns the first 3 letters 
    of the given string.
    """
    initials = ''
    words = string.upper().split()
    for i in range(len(words)):
        words[i] = ''.join(filter(str.isalnum, words[i]))   # remove special characters
    if len(words) == 1:
        word = words[0]
        initials = word[:3]
    else:
        for word in words:
            if word != '':
                initials = initials + word[0]
    return initials


def get_product_info(soup):
    """
    Returns a list containing the basic information and the ingredients of a 
    skincare product given the soup parsed from URL of its page on the Soko 
    Glam website
    Note: Ingredients are in a comma seperated string
    """
    product_html = soup.find(class_='main')

    product_name = product_html.find(class_='pdp__product-title').text
    brand = product_html.find(class_='pdp__product-vendor').contents[1].text
    price = float(product_html.find(class_='pdp-product__price--sale ProductPrice').text[1:])
    sku = string_initials(brand) + '-' + string_initials(product_name) + '-' + str(int(price))

    # some products don't have reviews
    rating = 0.0
    rating_count = 0
    reviews = product_html.find(itemprop='ratingCount')
    if reviews is not None:
        rating = float(product_html.find(itemprop='ratingValue').text)
        rating_count = int(reviews.text)

    # some product pages are formatted differently
    ingredients = product_html.find(id='content2')
    ingredients = ingredients.find(class_='tab-content--full')
    if ingredients.p is not None:
        ingredients = ingredients.p.text
    else:
    # ingredients = product_html.find(class_='tab-content--full').p.text
        ingredients = ingredients.h4.next_sibling.strip()

    product_info = [product_name, brand, price, rating, rating_count, sku, ingredients]

    return product_info


def get_category_urls(url):
    """
    Returns a list of URLs for individual products given the url for a search
    on Soko Glam - ie. all 'Facial Cleansers Double-Cleansing'
    """
    main_url = 'https://sokoglam.com/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(class_='collection-main-content')
    urls = []

    for product in results.find_all(class_='product__title'):
        product_page = product.a.get('href')
        product_page = main_url + product_page
        urls.append(product_page)

    return urls


def make_category_df(urls):
    """
    Returns a pandas dataframe containing the product info and ingredients
    of all products in a given list of URLs of product pages on the Soko Glam 
    website. Dataframe is in tidy format.
    Note: Ingredients are in a comma seperated string
    """
    category_rows = []
    for product_page in urls:
        page = requests.get(product_page)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        product_info = get_product_info(soup)
        category_rows.append(product_info)
       
    category_df = pd.DataFrame(category_rows)

    return category_df


def get_catgories_dict():
    """
    Returns a dictionary of categories for skincare for Soko Glam's menu.
    The category names are keys, and the html extensions are the values
    """
    page = requests.get('https://sokoglam.com/')
    soup = BeautifulSoup(page.content, 'html.parser')
    menu_soup = soup.find(class_='subnav__right')
    categories = menu_soup.find_all(class_='subnav__item')
    category_dict = dict()

    for category in categories:
        name = category.a.text
        url_ext = category.a.get('href')
        category_dict[name] = url_ext

    return category_dict


def make_data_file(categories, dictionary):
    """
    Creates a pandas dataframe of product data for all the products in the
    desired categories on the Soko Glam website and saves it to a csv
    file. Needs a dictionary of the URL extension for each category.
    """
    website_url = 'https://sokoglam.com/'
    big_df = pd.DataFrame()

    for category in categories:
        category_url = website_url + dictionary[category]
        product_urls = get_category_urls(category_url)

        category_df = make_category_df(product_urls)
        category_df['category'] = [category] * len(product_urls)

        big_df = pd.concat([big_df, category_df], ignore_index=True)
    
    big_df.columns = ['product_name', 'brand', 'price', 'rating', 
                      'rating_count', 'sku', 'ingredients', 'category']

    big_df.to_csv('sokoglam_data.csv', index=False, header=True)


def main():
    url_dictionary = get_catgories_dict()
    categories = ['Double-Cleanse', 'Exfoliators', 'Toners', 'Treatments', 
                  'Masks', 'Eye Care', 'Moisturizers', 'Sun Protection']
    
    make_data_file(categories, url_dictionary)

if __name__ == '__main__':
    main()
