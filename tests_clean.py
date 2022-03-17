"""
Tests functions for cleaning raw data scraped from the Soko Glam website
"""
import clean
import pandas as pd

def test_clean_ingredients():
    """
    Test the clean_ingredients function
    """
    print('Testing clean_ingredients():')
    data = pd.read_csv('sokoglam_data.csv')

    print('Testing without .txt file')
    df1 = clean.clean_ingredients(data)

    print(df1.loc[df1['sku'] == 'COC-OTMC-17'].values[0])
    print(df1.loc[df1['sku'] == 'MF-BBAT-25'].values[0])
    print(df1.loc[df1['sku'] == 'JTC-WWB-33'].values[0])

    print('Testing with .txt file')
    df2 = clean.clean_ingredients(data, 'not_ingredients.txt')

    print(df2.loc[df2['sku'] == 'COC-OTMC-17'].values[0])
    print(df2.loc[df2['sku'] == 'MF-BBAT-25'].values[0])
    print(df2.loc[df2['sku'] == 'JTC-WWB-33'].values[0])
    

def main():
    test_clean_ingredients()



if __name__ == '__main__':
    main()