"""
Tests functions for scraping data from the Soko Glam website
"""
import sokoglam_scrape as scrape
from bs4 import BeautifulSoup
import pandas as pd
import requests


def test_string_initials():
    """
    Test the string_initials function
    """
    print('Testing string_initials():')
    print(scrape.string_initials('Too Cool for School')) # TCFS
    print(scrape.string_initials('good (skin) days™'))  # GSD
    print(scrape.string_initials('A\'Pieu'))  # API
    print(scrape.string_initials('Peelosoft Eyes & Lip Cleansing Duo')) # PELCD



def test_get_product_info():
    """
    Test the get_product_info function
    """
    print('Testing get_product_info(soup):')

    page1 = requests.get('https://sokoglam.com/collections/skincare/products/then-i-met-you-living-cleansing-balm')
    soup1 = BeautifulSoup(page1.content, 'html.parser')
    page2 = requests.get('https://sokoglam.com/collections/cleansers/products/good-skin-days-a-new-leaf-cream-cleanser')
    soup2 = BeautifulSoup(page2.content, 'html.parser')
    page3 = requests.get('https://sokoglam.com/collections/cleansers/products/banila-co-clean-it-zero-classic')
    soup3 = BeautifulSoup(page3.content, 'html.parser')

    print(scrape.get_product_info(soup1))
    print(scrape.get_product_info(soup2))
    print(scrape.get_product_info(soup3))


def test_get_category_urls():
    """
    Test the get_category_urls function
    """
    print('Testing get_category_urls():')

    url = 'https://sokoglam.com/collections/cleansers'
    urls = scrape.get_category_urls(url)
    print(urls) 
    print(len(urls)) # 87 (as of Jan 22 2022)


def test_get_catgories_dict():
    """
    Test the get_catgories_dict function
    """
    print('Testing get_catgories_dict():')
    print(scrape.get_catgories_dict())


def main():
    test_string_initials()
    test_get_product_info()
    test_get_category_urls()
    test_get_catgories_dict()


if __name__ == '__main__':
    main()
