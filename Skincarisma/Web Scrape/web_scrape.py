"""
Impletements and executes functions that scrapes the Skincarisma website for
skincare products data
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd


def product_info(soup):
    """
    Returns a list containing the basic information of a skincare product
    given the soup parsed from URL of its ingredients page on the Skincarisma
    website
    """
    info_html = soup.find(class_='d-block d-md-none card product-section')

    product_name = info_html.find(class_='card-title font-125').text
    brand = info_html.find(class_='font-090 d-inline-block text-muted').text
    rating = float(info_html.find(class_='font-080 ml-1').text)
    rating_count = info_html.find('span', class_='bold')
    rating_count = int(rating_count.text.strip().split()[0])

    product_info = [product_name, brand, rating, rating_count]
    return product_info


def product_ingredients(soup):
    """
    Returns a list containing the ingredients of a skincare product given
    the soup parsed from the URL of its ingredients page on the Skincarisma
    website
    """
    ing_table = soup.find(class_='table table-sm mt-4 ingredients-table')
    ingredients = []

    if ing_table is None:
        return ingredients

    ing_table = ing_table.find('tbody').find_all('tr')
    for ingredient in ing_table:
        name = ingredient.find_all(class_='align-middle')
        name = name[2].text.strip().split('(')[0].strip()
        ingredients.append(name)

    return ingredients


def make_product_df(info, ingredients):
    """
    Returns a pandas dataframe containing the product info and ingredients
    of a single product in tidy format given a list of product info and a
    list of ingredients
    """
    n = len(ingredients)
    product = dict()
    if n == 0:
        product = {'Product_Name': [info[0]], 'Brand': [info[1]],
                   'Rating': [info[2]], 'Ratings_Count': [info[3]],
                   'Ingredients': ['None Listed']}
    else:
        name_list = [info[0]] * n
        brand_list = [info[1]] * n
        rating_list = [info[2]] * n
        rating_count_list = [info[3]] * n
        product = {'Product_Name': name_list, 'Brand': brand_list,
                   'Rating': rating_list, 'Ratings_Count': rating_count_list,
                   'Ingredients': ingredients}
    return pd.DataFrame(product)


def short_list_of_urls(url):
    """
    Returns a list of URLs for individual products given a URL of a single
    page containing the search results of a search
    """
    main_url = 'https://www.skincarisma.com'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(class_='list-unstyled mt-2 mb-0')
    urls = []

    for product in results.find_all(id='search-product-item'):
        product_page = product.find(itemprop='url')['href']
        product_page = main_url + product_page + '/ingredient_list'
        urls.append(product_page)

    return urls


def long_list_of_urls(url):
    """
    Returns a list of all URLs of individual products that are the in the
    search results of given search URL
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    pages_count = int(soup.find(class_='last-page-marker').text)
    urls = []
    for i in range(1, pages_count + 1):
        search_page = url + '&page=' + str(i)
        urls.extend(short_list_of_urls(search_page))

    return urls


def make_category_df(urls):
    """
    Returns a pandas dataframe containing the product info and ingredients
    of all products in a given list of URLs of products' ingredients pages
    on the Skincarisma website. Dataframe is in tidy format.
    """
    category_df = pd.DataFrame()
    for product_page in urls:
        page = requests.get(product_page)
        soup = BeautifulSoup(page.content, 'html.parser')
        if soup.find(class_='error-message') is None:
            info = product_info(soup)
            ingredients = product_ingredients(soup)
            product_df = make_product_df(info, ingredients)
            category_df = pd.concat([category_df, product_df],
                                    ignore_index=True)

    return category_df


def catgories_dict(url):
    """
    Returns a dictionary of categories for skincare for Skincarisma's menu.
    The category names are keys, and the html
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    categories = soup.find(id='mainMenuCategories')
    categories = categories.find_all(class_=('p-2 pl-5 border-bottom '
                                             'font-090 text-grey'))
    category_dict = dict()

    for category in categories:
        name = category.text
        url_ext = category['href']
        category_dict[name] = url_ext

    return category_dict


def make_data_file(categories, dictionary):
    """
    Creates a pandas dataframe of product data for all the products in the
    desired categories on the Skincarisma website and saves it to a csv
    file. Needs a dictionary of the URL extension for each category.
    """
    website_url = 'https://www.skincarisma.com'
    big_df = pd.DataFrame()

    for category in categories:
        category_url = website_url + dictionary[category]
        product_urls = long_list_of_urls(category_url)

        category_df = make_category_df(product_urls)
        n = len(category_df.index)
        category_df['Category'] = [category] * n

        big_df = pd.concat([big_df, category_df], ignore_index=True)

    big_df.to_csv('skincare_data.csv', index=False, header=True)


def main():
    url_dictionary = catgories_dict('https://www.skincarisma.com')
    categories = ['Toners', 'Serums, Essence & Ampoules', 'Moisturizers',
                  'Sheet Masks', 'Leave-On & Sleeping Masks/Packs',
                  'Facial Oils']
    make_data_file(categories, url_dictionary)


if __name__ == '__main__':
    main()
