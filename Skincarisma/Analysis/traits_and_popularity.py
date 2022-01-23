"""
Impletements and executes functions that analyzes skincare data scraped
from the Skincarisma website
"""
import pandas as pd
import question_1 as q1
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GroupShuffleSplit


def predict_rating(data, max_nodes=None):
    """
    Creates a simple ML model for predicting the rating of skincare products
    containing a certain ingredient in a given category from a specific brand,
    with a certain ratings count.
    Returns the train and test mean squared errors.
    """
    data = data.loc[:, ['Brand', 'Rating', 'Ratings_Count', 'Ingredients',
                        'Category', 'product_id']]
    features = data.loc[:, ['Brand', 'Ratings_Count', 'Ingredients',
                            'Category']]
    features = pd.get_dummies(features)
    labels = data['Rating']

    # Split data by product_id so all rows belonging to one product is in the
    # same dataset
    test_products_count = round(len(data['product_id'].unique()) * 0.3)
    train_inds, test_inds = next(
        GroupShuffleSplit(
            test_size=test_products_count, n_splits=2
        ).split(features, labels, groups=data['product_id'])
    )
    features_train, features_test = \
        features.iloc[train_inds], features.iloc[test_inds]
    labels_train, labels_test = \
        labels.iloc[train_inds], labels.iloc[test_inds]

    model = DecisionTreeRegressor(max_depth=max_nodes)
    if max_nodes is None:
        model = DecisionTreeRegressor()
    model.fit(features_train, labels_train)

    train_predictions = model.predict(features_train)
    train_error = mean_squared_error(labels_train, train_predictions)

    test_predictions = model.predict(features_test)
    test_error = mean_squared_error(labels_test, test_predictions)
    print(train_error, test_error)
    return train_error, test_error


def predict_rating_count(data, max_nodes):
    """
    Creates a simple ML model for predicting the rating of skincare products
    containing a certain ingredient in a given category from a specific brand,
    with a certain ratings count.
    Returns the train and test mean squared errors.
    """
    data = data.loc[:, ['Brand', 'Rating', 'Ratings_Count', 'Ingredients',
                        'Category', 'product_id']]
    features = data.loc[:, ['Brand', 'Rating', 'Ingredients', 'Category']]
    features = pd.get_dummies(features)
    labels = data['Ratings_Count']

    # Split data by product_id so all rows belonging to one product is in the
    # same dataset
    test_products_count = round(len(data['product_id'].unique()) * 0.3)
    train_inds, test_inds = next(
        GroupShuffleSplit(
            test_size=test_products_count, n_splits=2
        ).split(features, labels, groups=data['product_id'])
    )
    features_train, features_test = \
        features.iloc[train_inds], features.iloc[test_inds]
    labels_train, labels_test = \
        labels.iloc[train_inds], labels.iloc[test_inds]

    model = DecisionTreeRegressor(max_depth=max_nodes)
    model.fit(features_train, labels_train)

    train_predictions = model.predict(features_train)
    train_error = mean_squared_error(labels_train, train_predictions)

    test_predictions = model.predict(features_test)
    test_error = mean_squared_error(labels_test, test_predictions)

    print(train_error, test_error)
    return train_error, test_error


def train_and_test_mse(data, model, min_node, max_node):
    """
    Returns a dataframe of training and testing MSEs for a range of
    nodes
    """
    mse = {'Max Nodes': [], 'Train MSE': [], 'Test MSE': []}

    for i in range(min_node, max_node):
        train_error, test_error = None, None
        if model == 'Rating':
            train_error, test_error = predict_rating(data, i)
        else:
            train_error, test_error = predict_rating_count(data, i)
        mse['Max Nodes'].append(i)
        mse['Train MSE'].append(train_error)
        mse['Test MSE'].append(test_error)

    mse = pd.DataFrame(data=mse)
    print(mse)
    return mse


def line_plot_test_mse(data, model, min_node, max_node):
    """
    Plots the testing MSE over a range of max nodes
    """
    mse = train_and_test_mse(data, model, min_node, max_node)

    plot = sns.relplot(x='Max Nodes', y='Test MSE', data=mse, kind='line')

    plt.title("MSE for Different Max Nodes")
    plt.xlabel('Max Nodes for ML Model')
    plt.ylabel('MSE')

    plot.savefig(model + ' model.png', bbox_inches='tight')


def no_other_info_mse(data, label):
    """
    Returns the MSE of the mean of all product ratings/rating count were used
    as a predictor for all products with no other information
    """
    unique_products = q1.unique_products(data)
    mean = unique_products[label].mean()
    n = len(unique_products)

    squared_diff = (unique_products[label] - mean) ** 2
    mse = (1 / n) * sum(squared_diff)

    return mse


def main():
    id_skincare = pd.read_csv('skincare_id.csv')

    line_plot_test_mse(id_skincare, 'Rating', 3, 11)
    line_plot_test_mse(id_skincare, 'Ratings_Count', 2, 15)

    print(no_other_info_mse(id_skincare, 'Rating'))
    print(no_other_info_mse(id_skincare, 'Ratings_Count'))


if __name__ == '__main__':
    main()
