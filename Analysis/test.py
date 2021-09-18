"""
Tests functions for data analysis of skincare data
"""
import question_1 as q1
import question_2 as q2
import question_3 as q3
import pandas as pd


def test_mean_ingredient_rating(data, aliases):
    """
    Test the mean_ingredient_rating function from question 1 analysis
    """
    print('Testing mean_ingredient_rating():')
    print(q1.mean_ingredient_rating(data, 'Niacinamide', aliases))  # 1
    print(q1.mean_ingredient_rating(data, 'Squalane', aliases))  # 4


def test_unique_products(data):
    """
    Tests unique_products function from question 1 analysis
    """
    print('Testing unique_products():')
    print(q1.unique_products(data))  # [10 rows x 6 columns]


def test_percent_containing_ingredient(data, aliases):
    """
    Tests percent_containing_ingredient function from question 1 analysis
    """
    print('Testing percent_containing_ingredient():')
    print('Niacinamide:',  # 40%
          q1.percent_containing_ingredient(data, 'Niacinamide', aliases))
    print('Madecassoside:',  # 10%
          q1.percent_containing_ingredient(data, 'Madecassoside', aliases))


def test_ingredients_in_top_rated(data, aliases):
    """
    Tests ingredients_in_top_rated function from question 1 analysis
    """
    print('Testing ingredients_in_top_rated_function():')
    # 'BHA': 10.0, 'AHA': 50.0, 'AHA': 50.0, 'Niacinamide': 40.0,
    # 'Vitamin C': 20.0, 'Vitamin A': 10.0, 'Hyaluronic Acid': 30.0,
    # 'Ceramides': 10.0, 'Squalane': 30.0, 'Madecassoside': 10.0 and rest is 0
    print(q1.ingredients_in_top_rated(data, aliases, 0))
    # 'BHA': 100, 'AHA': 100, 'Niacinamide': 33.33, 'Hyaluronic Acid': 100.0,
    # 'Squalane': 10.0
    print(q1.ingredients_in_top_rated(data, aliases, 3))


def test_models(data):
    """
    Tests the ML model functions for rating and rating count from question 2
    analysis
    """
    print(q2.predict_rating(data, 5))
    print(q2.predict_rating_count(data, 5))


def test_mse(data):
    """
    Tests the no_other_info_mse function for rating and rating count from
    question 2 analysis
    """
    print(q2.no_other_info_mse(data, 'Rating'))
    print(q2.no_other_info_mse(data, 'Ratings_Count'))


def test_calc_rating_difference(data):
    """
    Tests the calc_rating_difference function for from question 3 analysis
    """
    current = data[data['Product_Name'] == 'Gokujyun Lotion']
    other = data[data['Product_Name'] == 'Gokujyun Lotion Light']
    print(q3.calc_rating_difference(current, other))  # 0.2


def main():
    small_skincare = pd.read_csv('small_skincare.csv')
    medium_skincare = pd.read_csv('medium_skincare.csv')
    skincare_id = pd.read_csv('skincare_id.csv')
    aliases = q1.make_ingredients_alias_dict()

    test_unique_products(small_skincare)
    test_mean_ingredient_rating(small_skincare, aliases)
    test_percent_containing_ingredient(small_skincare, aliases)
    test_ingredients_in_top_rated(small_skincare, aliases)

    test_models(medium_skincare)
    test_mse(small_skincare)

    test_calc_rating_difference(skincare_id)


if __name__ == '__main__':
    main()
