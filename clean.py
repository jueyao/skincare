"""
Implements functions that cleans the raw skincare porducts data scraped from 
the Soko Glam website
"""

import pandas as pd
import numpy as np
import re


def clean_ingredients(df, file_path = None):
    """
    Returns a new dataframe with special characters that don't belong in 
    ingredient names removed. Also removes undesirable phrases that were 
    scraped along with the ingredients lists, given a text file of 
    undesireable phrases
    Note: each phrase should be on a new line
    """
    clean_ingredients =  df['ingredients']

    # removes undesirable phrases (ex. organic ingredients)
    if file_path is not None:
        with open(file_path) as bad_substrings:
            for string in bad_substrings.readlines():
                regex = r'' + re.escape(string.strip())
                clean_ingredients = clean_ingredients.str.replace(
                    regex, '', regex=True, case=False)
    
    # remove special characters not used in ingredients lists
    special_char = ['*', '"', '.', '[', ']', '\\n', '\\r']
    for char in special_char:
        clean_ingredients = clean_ingredients.str.replace(char, '')

    df['ingredients'] = clean_ingredients
    return df


def list_replace(strings, pattern, replacement):
    """
    Replace each occurrence of pattern/regex in the given list of strings
    """
    new_strings = [s.replace(pattern, replacement) for s in strings]
    return new_strings


def list_strip(strings):
    """
    Strip the white space from each element of the given list
    """
    stripped = [string.strip() for string in strings]
    return stripped


def find_incomp_ingred_lists(df):
    """
    Creates a .txt file containing the sku and ingredients lists of products 
    that seem to have incomplete ingredients lists (lack of comma)
    """
    df['ingredients'] = df['ingredients'].str.replace('1,2', '1.2')

    filtered_df = df[~df['ingredients'].str.contains(',')]
    sku_ingredients = filtered_df.loc[:,['sku', 'ingredients']]
    sku_ingredients.to_csv('incomplete_ingredients.txt', 
        header=None, index=None, sep=',')



def create_junction_table(df):
    """
    Creates and returns junction table of ingredients, with each product's sku 
    as the key
    """
    # rename 1,2-Hexanediol without comma
    fixed_hexanediol = df['ingredients'].str.replace('1,2', 'placeholder')
    seperated_ingred = fixed_hexanediol.str.split(',').apply(list_strip)
    seperated_ingred = seperated_ingred.apply(list_replace, args=('placeholder', '1,2'))
    
    junction_table = []
    products_added = set()
    df = df.reset_index(drop=True)
    for i in range(len(df.index)):
        product = df.loc[i]
        if product['sku'] not in products_added:
            ingredients_list = seperated_ingred.iloc[i]
            for j in range(len(ingredients_list)):
                new_row = [product['sku'], ingredients_list[j]]
                junction_table.append(new_row)
            products_added.add(product['sku'])
    
    junction_table = pd.DataFrame(junction_table)
    junction_table.columns = ['sku', 'ingredient']

    return junction_table


def find_duplicates(df):
    """
    Returns list of skus of skincare products that appear in the data multiple 
    times under mutiple categories
    """
    unique_df = df.drop_duplicates(subset=list(df.columns).remove('category'))
    unique_skus = list(unique_df['sku'])
    return unique_skus
