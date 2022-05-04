"""
Implements functions that cleans and manipulates the raw skincare porducts data 
scraped from the Soko Glam website
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

    filtered_df = df[~df['ingredients'].str.contains(',', na=False)]
    sku_ingredients = filtered_df.loc[:,['sku', 'ingredients']]
    sku_ingredients.to_csv('incomplete_ingredients.txt', 
        header=None, index=None, sep=',')


def create_junction_table(df):
    """
    Creates and returns junction table of ingredients, with each product's sku 
    as the key
    """
    # rename 1,2-Hexanediol, 2,3-Butanediol without comma
    fixed_comma = df['ingredients'].str.replace('1,2', 'placeholder1')
    fixed_comma = fixed_comma.str.replace('2,3', 'placeholder2')
    seperated_ingred = fixed_comma.str.split(',').apply(list_strip)
    seperated_ingred = seperated_ingred.apply(list_replace, args=('placeholder1', '1,2'))
    seperated_ingred = seperated_ingred.apply(list_replace, args=('placeholder2', '2,3'))
    
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

    # drop empty rows
    junction_table['ingredient'].replace('', np.nan, inplace=True)
    junction_table.dropna(subset=['ingredient'], inplace=True)

    return junction_table


def find_unique_skus(df):
    """
    Returns list of skus of skincare products that appear in the data only once
    """
    unique_df = df.drop_duplicates(subset=list(df.columns).remove('category'))
    unique_skus = list(unique_df['sku'])
    return unique_skus


def find_duplicated_skus(df):
    """
    Creates a .txt file containing the names, skus, and categories of products 
    that are duplicated
    """
    is_duplicated = df['sku'].duplicated(keep=False)
    filtered_df = df[is_duplicated]
    duplicated_skus = set(filtered_df['sku'])

    duplicated_rows = []
    for sku in duplicated_skus:
        product_rows = filtered_df[filtered_df['sku'] == sku]
        product_rows = product_rows.reset_index(drop=True)
        product_name = product_rows['product_name'][0]
        categories = list(product_rows['subcategory'])
        duplicated_rows.append([product_name, sku, categories])
        
    duplicated_products = pd.DataFrame(duplicated_rows)
    duplicated_products.to_csv('duplicated_products.txt', 
        header=None, index=None, sep=':')


def clean_data(data, incomplete_ingred_skus=None):
    """
    Clean the ingredients lists of products and drop products given a text file 
    of skus of products that have incompelte ingredient lists
    """
    cleaned_ingred = clean_ingredients(data, file_path='not_ingredients.txt')

    cleaned_ingred['ingredients'] = cleaned_ingred['ingredients'].str.replace(
        'Citrus Aurantium Dulcis (Orange) Flower Oil  Farnesol', 
        'Citrus Aurantium Dulcis (Orange) Flower Oil, Farnesol', regex=False)
    cleaned_ingred['ingredients'] = cleaned_ingred['ingredients'].str.replace(
        'Water, Eau', 'Water/Eau', regex=False)
    cleaned_ingred['ingredients'] = cleaned_ingred['ingredients'].str.replace(
        '1, 2', '1,2', regex=False)
    cleaned_ingred['ingredients'] = cleaned_ingred['ingredients'].str.replace(
        ',000ppm', '000ppm', regex=False)

    # Certain products has dash seperated ingredients lists
    cleaned_ingred['ingredients'] = cleaned_ingred['ingredients'].str.replace(
        ' - ', ', ')
    
    # Drop products with incomplete ingredients lists
    if incomplete_ingred_skus is not None:
        with open(incomplete_ingred_skus) as skus:
            bad_skus = [sku.strip() for sku in skus.readlines()]
            cleaned_ingred = cleaned_ingred.loc[~cleaned_ingred['sku'].isin(bad_skus)]

    return cleaned_ingred.reset_index(drop=True)


def make_ingredients_group_dict():
    """
    Returns a dict containing the aliases, chemical derivatives, or names of
    subtypes of desirable skincare ingredients
    """
    ingred_aliases = dict()
    ingred_aliases['BHA'] = ['salicylic acid', 'capryloyl salicylic acid']
    ingred_aliases['AHA'] = [
        'glycolic acid', 'lactic acid', 'lactic acid/glycolic acid copolymer',
        'tartaric acid', 'citric acid', 'malic acid', 'mandelic acid'
    ]
    ingred_aliases['PHA'] = [
        'gluconolactone', 'delta gluconolactone', 'galactose',
        'lactobionic acid'
    ]
    ingred_aliases['Vitamin C'] = [
        '2-O-ethyl ascorbic acid', 'ascorbic acid',
        'ascorbic acid polypeptide',
        'ascorbic acid/orange/citrus limon/citrus aurantifolia polypeptides',
        'ascorbyl glucoside', 'ascorbyl palmitate',
        'trisodium ascorbyl palmitate phosphate', 'vitamin c-ester',
        'ascorbyl tetraisopalmitate', 'magnesium ascorbyl phosphate',
        'sodium ascorbyl phosphate', 'tetrahexyldecyl ascorbate',
        'sodium ascorbate', 'calcium ascorbate'
    ]
    ingred_aliases['Ceramides'] = [
        'ceramide', 'ceramide 1', 'ceramide 2', 'ceramide 3', 'ceramide 4',
        'ceramide 5', 'ceramide 6', 'ceramide 6 ii', 'Ceramide 9',
        'ceramide eop', 'ceramide eos', 'glucosyl ceramide',
        'cetyl-pg hydroxyethyl palmitamide',
        'hydroxypropyl bispalmitamide mea',
        'wheat germ oil/palm oil aminopropanediol esters',
        'safflower oil/palm oil aminopropanediol esters',
        'olive oil aminopropanediol esters',
        'linseed oil/palm oil aminopropanediol esters',
        'cottonseed oil/palm oil aminopropanediol esters',
        'camellia sinensis seed oil/palm oil aminopropanediol esters',
        'hydroxypalmitoyl sphinganine',
        'myristoyl/palmitoyl oxostearamide/arachamide mea'
    ]
    ingred_aliases['Squalane'] = ['olive squalane', 'phytosqualane']
    ingred_aliases['Snail Mucin'] = [
        'snail secretion filtrate', 'snail secretion filtrate extract',
        'saccharomyces/snail Secretion filtrate ferment filtrate'
    ]
    ingred_aliases['Madecassoside'] = [
        'centella asiatica', 'asiaticoside', 'asiatic acid', 'madecassic acid'
    ]
    ingred_aliases['hyaluronic acid'] = [
        'sodium hyaluronate', 'sodium acetylated hyaluronate'
    ]
    ingred_aliases['green tea'] = ['camellia sinensis']
    return ingred_aliases


def get_contains_ingredient(df, ingredient, group=None):
    """
    Given an ingredient and a list of an ingredient's aliases, adds a boolean 
    column to the dataframe describing whether each product contains the 
    ingredient or not and returns the new df 
    """
    contains_ingredient = df['ingredients'].str.contains(
        pat=ingredient, case=False)
    if group is not None:
        for element in group:
            contains_element = df['ingredients'].str.contains(
                pat=element, case=False)
            contains_ingredient = contains_ingredient | contains_element
    
    return contains_ingredient


def get_ingredient_count(df, ingredient, group=None):
    """
    Given a dataframe, an ingredient and a list of the group that ingredient 
    belongs to, returns a series describing how many of that ingredient [group] 
    each product has
    """
    ingredient_count = df['ingredients'].str.count(pat=ingredient, flags=re.I)
    if group is not None:
        for element in group:
            element_count = df['ingredients'].str.count(
                pat=element, flags=re.I)
            ingredient_count = ingredient_count + element_count

    return ingredient_count


def add_contains_ingredient(df):
    """
    Add boolean columns indicating whether the skincare product contains a 
    important ingredient and returns the dataframe
    """
    # Single ingredients
    single_ingredients = ['niacinamide', 'azelaic acid', 'urea', 'retinol']
    for ingredient in single_ingredients:
        contains_ingredient = get_contains_ingredient(df, ingredient)
        column_name = str('contains_' + ingredient.lower().replace(' ', '_'))
        df = pd.concat([df, contains_ingredient.rename(column_name)], axis=1)

    # Group of ingredients
    ingredient_groups = make_ingredients_group_dict()
    for ingredient in ingredient_groups.keys():
        contains_ingredient = get_contains_ingredient(
            df, ingredient, ingredient_groups[ingredient])
        column_name = str('contains_' + ingredient.lower().replace(' ', '_'))
        df = pd.concat([df, contains_ingredient.rename(column_name)], axis=1)

    return df


def add_ingredient_portion(df):
    """
    Add a column indicating the portion of ingredients that are important
    """
    # Single Ingredients
    single_ingredients = ['niacinamide', 'azelaic acid', 'retinol']
    star_ingredients = np.zeros(len(df))
    for ingredient in single_ingredients:
        star_ingredients = star_ingredients + get_ingredient_count(df, ingredient)

    # Group of ingredients
    ingredient_groups = make_ingredients_group_dict()
    for ingredient in ingredient_groups.keys():
         star_ingredients = star_ingredients + get_ingredient_count(
            df, ingredient, ingredient_groups[ingredient])
    
    star_ingred_counts = star_ingredients / df['ingredient_counts']
    df = pd.concat([df, star_ingred_counts.rename('star_ingred_counts')], axis=1)
    return df


def get_total_ingredient_count(df, junction_table):
    """
    Returns a list of counts for the number of ingredients a product has for 
    every product the dataframe has in order
    """
    counts = []
    for sku in df['sku']:
        sku_ingredients = junction_table[junction_table['sku'].str.match(sku)]
        counts.append(len(sku_ingredients.index))

    return counts


def add_top_ingredient_count(df, junction_table, top_percentile=0.5):
    quantile_ingredients = []
    for sku in df['sku']:
        sku_ingredients = junction_table[junction_table['sku'].str.match(sku)]
        index = round(len(sku_ingredients.index) * top_percentile)
        sku_ingredients.drop(sku_ingredients.index[:index])

        ingredients = ','.join(list(sku_ingredients['ingredient']))
        quantile_ingredients.append([sku, ingredients])
        
    quantile_ingredients = pd.DataFrame(quantile_ingredients)
    quantile_ingredients.columns = ['sku', 'ingredients']
    
    # Single Ingredients
    single_ingredients = ['niacinamide', 'azelaic acid', 'retinol']
    star_ingredients = np.zeros(len(df))
    for ingredient in single_ingredients:
        star_ingredients = star_ingredients + get_ingredient_count(
            quantile_ingredients, ingredient)

    # Group of ingredients
    ingredient_groups = make_ingredients_group_dict()
    for ingredient in ingredient_groups.keys():
         star_ingredients = star_ingredients + get_ingredient_count(
            quantile_ingredients, ingredient, ingredient_groups[ingredient])
    
    df['top_ingredient_count'] = star_ingredients.astype(int)

    return df
