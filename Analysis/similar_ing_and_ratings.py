"""
Impletements and executes functions that analyzes skincare data scraped
from the Skincarisma website
"""
import question_1 as q1
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def calc_rating_difference(current_df, other_df):
    """
    Returns the rating differences between two given similar products.
    Rounds to 3 decimal places.
    Returns None if the products are not similar.
    """
    current_df = current_df.reset_index()
    other_df = other_df.reset_index()
    current_ingred_count = len(current_df)
    other_ingred_count = len(other_df)

    matching_ingred_count = len(
        current_df.merge(other_df, left_on='Ingredients',
                         right_on='Ingredients')
    )

    # Products are similar if they share at least 50% of the same ingredients
    if ((matching_ingred_count >= (current_ingred_count / 2)) and
            (matching_ingred_count >= (other_ingred_count / 2))):
        current_product_rating = current_df.loc[0, 'Rating']
        other_product_rating = other_df.loc[0, 'Rating']
        difference = abs(current_product_rating - other_product_rating)
        return round(difference, 1)
    else:
        return None


def similar_products_ratings(data):
    """
    Returns dict of products and products that are similar to them (50% of
    ingredients are similar).
    Only uses products that having at least 1 rating.
    """
    data = data[data['Ratings_Count'] != 0]

    unique_products = q1.unique_products(data)
    mean_rating = unique_products['Rating'].mean()

    products = data['product_id'].unique()
    rating_differences = {
        'Product': [],
        'Mean Rating Difference from All': [],
        'Mean Rating Difference from Similar': []
    }
    for product in products:
        current_df = data[data['product_id'] == product]

        other_products = products[products != product]
        similar_product_rating_differences = []
        for other in other_products:
            other_df = data[data['product_id'] == other]
            rating_difference = calc_rating_difference(current_df, other_df)
            if rating_difference is not None:
                similar_product_rating_differences.append(rating_difference)

        if similar_product_rating_differences != []:
            current_product_rating = current_df['Rating'].mean()
            rating_differences['Product'].append(current_df.loc[0, 'Product'])
            rating_differences['Mean Rating Difference from All'].append(
                round(abs(mean_rating - current_product_rating), 2)
            )
            rating_differences['Mean Rating Difference from Similar'].append(
                round((sum(similar_product_rating_differences) /
                       len(similar_product_rating_differences)), 2)
            )

        print(product)

    return pd.DataFrame(data=rating_differences)


def calculate_mse(data, label):
    """
    Returns the MSE of the model using the overall mean predictor
    for all products
    """
    n = len(data)

    squared_diff = (data[label]) ** 2
    mse = (1 / n) * sum(squared_diff)

    return mse


def plot_accuracy(data):
    """
    Plots the percentages prodcuts where the average rating of similar products
    was closer to the rating of a product than the mean.
    """
    n = len(data)
    model_worse = len(data[data['Mean.Rating.Difference.from.All'] <
                      data['Mean.Rating.Difference.from.Similar']]) / n
    model_better = len(data[data['Mean.Rating.Difference.from.All'] >
                       data['Mean.Rating.Difference.from.Similar']]) / n
    model_same = len(data[data['Mean.Rating.Difference.from.All'] ==
                     data['Mean.Rating.Difference.from.Similar']]) / n

    model_performance = {
        'Model Perfomance': ['Worse', 'Better', 'Same'],
        'Percentage': [model_worse * 100, model_better * 100, model_same * 100]
    }
    model_performance = pd.DataFrame(data=model_performance)

    plot = sns.catplot(x='Model Perfomance', y='Percentage',
                       data=model_performance, kind='bar')

    plt.xlabel('Model Performance Compared to Mean')
    plt.title('Similar Ingredients Model Performance Compared to Mean')

    plot.savefig('similar_ingredients_model.png')


def main():
    skincare = pd.read_csv('skincare_id.csv')

    similar_ratings = similar_products_ratings(skincare)
    similar_ratings.to_csv('similar_ratings.csv', index=False, header=True)
    similar_ratings = pd.read_csv('similar_ratings.csv')
    plot_accuracy(similar_ratings)

    print(calculate_mse(similar_ratings, 'Mean.Rating.Difference.from.All'))
    print(calculate_mse(similar_ratings,
                        'Mean.Rating.Difference.from.Similar'))


if __name__ == '__main__':
    main()
