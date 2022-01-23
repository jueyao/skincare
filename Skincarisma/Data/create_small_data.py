"""
Create small skincare data to be used for testing
"""
import pandas as pd
import random


def create_small_data(data, n):
    """
    Creates and returns a small skincare dataframe by randomly selecting n
    products from the given data
    """
    product_indexes = random.sample(range(0, len(data)), n)

    unique = data.copy()
    unique.drop('Ingredients', inplace=True, axis=1)
    unique.drop_duplicates()

    selected_products = pd.DataFrame()
    for index in product_indexes:
        same_name = data['Product_Name'] == unique.loc[index, 'Product_Name']
        same_brand = data['Brand'] == unique.loc[index, 'Brand']
        same_category = data['Category'] == unique.loc[index, 'Category']
        same_rating = data['Rating'] == unique.loc[index, 'Rating']
        same_ratings_count = data['Ratings_Count'] == \
            unique.loc[index, 'Ratings_Count']
        product_df = data[same_name & same_brand & same_category &
                          same_rating & same_ratings_count]
        selected_products = pd.concat([selected_products, product_df],
                                      ignore_index=True)

    return selected_products


def main():
    skincare = pd.read_csv('skincare_id.csv')
    small_skincare = create_small_data(skincare, 10)
    small_skincare.to_csv('small_skincare.csv', index=False, header=True)

    medium_skincare = create_small_data(skincare, 100)
    medium_skincare.to_csv('medium_skincare.csv', index=False, header=True)


if __name__ == '__main__':
    main()
