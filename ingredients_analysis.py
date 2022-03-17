"""
Data Exploration
"""

import pandas as pd
import clean as cl

def preprocess_data(df, incomplete_ingred_skus = None):
    """
    Clean the ingredients lists of products and drop products given a text file 
    of skus of products that have incompelte ingredient lists
    """
    cleaned_ingred = cl.clean_ingredients(df, file_path='not_ingredients.txt')

    cleaned_ingred['ingredients'] = cleaned_ingred['ingredients'].str.replace(
        'Citrus Aurantium Dulcis (Orange) Flower Oil  Farnesol', 
        'Citrus Aurantium Dulcis (Orange) Flower Oil, Farnesol', regex=False)
    
    # Certain products has dash seperated ingredients lists
    cleaned_ingred['ingredients'] = cleaned_ingred['ingredients'].str.replace(
        ' - ', ', ')
    
    # Drop products with incomplete ingredients lists
    if incomplete_ingred_skus is not None:
        with open(incomplete_ingred_skus) as skus:
            bad_skus = [sku.strip() for sku in skus.readlines()]
            cleaned_ingred = cleaned_ingred.loc[~cleaned_ingred['sku'].isin(bad_skus)]

    return cleaned_ingred


def main():
    df = pd.read_csv('sokoglam_data.csv')
    # Find skus of products with incomplete ingredients lists with 
    # cl.find_incomp_ingred_lists(df)
    cleaned_data = preprocess_data(
        df, incomplete_ingred_skus='incomplete_ingredients_skus.txt')
    junction_table = cl.create_junction_table(cleaned_data)

    cleaned_data.to_csv('cleaned_data.csv', index=None, sep=',')
    junction_table.to_csv('junction_table.csv', index=None, sep=',')


if __name__ == '__main__':
    main()
