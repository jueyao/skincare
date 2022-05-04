"""
Tests multiple classification models against a baseline model to predict the 
rating bin of skincare products
"""
import pandas as pd
import numpy as np
import re
import data_prep as prep

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import model_selection


def classification_preprocess(df):
    """
    Preprocess the data to prepare for classification models
    """
    # drop product_name, sku 
    # drop ingredients , assumes data already has boolean columns indicating 
    # whether the skincare product contains important ingredients
    df = df.drop(columns=['product_name', 'sku', 'ingredients'])
    #df = df.loc[df['subcategory'] != 'Spot Treatment']
    # drop category since random forest works better without too many columns
    df = df.drop(columns=['subcategory'])

    # drop products that don't having any ratings yet
    df = df[df['rating_count'] >= 3]
    #df = df.drop(columns=['rating_count'])

    # one-hot encode data
    df = pd.get_dummies(df)

    # partitions the ratings columns into 4 levels (Very Low, Low, Average, High) 
    bin_column = pd.cut(df['rating'],
       bins=[0, 3.85, 4.25, 4.65, 5.05], 
       labels=["Very Low", "Low", "Average", "High"])
    df = pd.concat([df, bin_column.rename('rating_bin')], axis=1)
    df = df.drop(columns=['rating'])

    return df


def majority_class_classifier(train_data, test_data, k):
    """
    Trains the majority class classifier given training data and k and prints 
    the mean k-fold cross validation accuracy
    """
    train_labels = train_data['rating_bin']
    train_features = train_data.loc[:, train_data.columns != 'rating_bin']
    test_labels = test_data['rating_bin']
    test_features = test_data.loc[:, test_data.columns != 'rating_bin']

    majority_class_model = DummyClassifier(strategy="most_frequent")
    majority_class_model.fit(train_features, train_labels)
    train_score = majority_class_model.score(train_features, train_labels)
    test_score = majority_class_model.score(test_features, test_labels)

    print("Majority Class Classifier Train Accuracy: ", round(train_score, 4))
    print("Majority Class Classifier Test Accuracy: ", 
          round(test_score, 4), "\n")


def logistic_regression(train_data , k):
    """
    Trains the logistic regression classifier given training data and k and 
    prints the mean k-fold cross validation accuracy
    """
    train_labels = train_data['rating_bin']
    train_features = train_data.loc[:, train_data.columns != 'rating_bin']

    hyperparameters = {'penalty': ['l1', 'l2'],
                       'C':[0.0001, 0.001,.009,0.01,.09,1,5,10,25,100]}
    logistic_model = LogisticRegression(solver='liblinear', random_state=1)
    grid_logistic_model = GridSearchCV(
        logistic_model, param_grid=hyperparameters)
    grid_logistic_model.fit(train_features, train_labels)

    print("Logistic Regression Best Hyperparameters:")
    print("penalty: ", grid_logistic_model.best_params_['penalty'], " | ", 
          "lambda: ", grid_logistic_model.best_params_['C'])
    scores = cross_val_score(
        grid_logistic_model, train_features, train_labels, cv=k)
    print("Logistic Regression Cross Validation Accuracy: ",
          [round(score, 4) for score in scores])
    print("Logistic Regression Average Cross Validation Accuracy: ", 
          round(scores.mean(), 4), "\n")


def decision_tree(train_data, k):
    """
    Trains the decision tree classifier given training data and k and 
    prints the mean k-fold cross validation accuracy
    """
    train_labels = train_data['rating_bin']
    train_features = train_data.loc[:, train_data.columns != 'rating_bin']

    hyperparameters = {'min_samples_leaf': [1, 2, 5, 10, 50, 100, 200],
                       'max_depth': [1, 5, 10, 15, 20]}
    tree_model = DecisionTreeClassifier(random_state=1)
    grid_tree_model = GridSearchCV(tree_model, param_grid=hyperparameters)
    grid_tree_model.fit(train_features, train_labels)

    print("Decision Tree Best Hyperparameters:")
    print("min_samples_leaf: ", 
          grid_tree_model.best_params_['min_samples_leaf'], " | ",
          "max_depth: ", grid_tree_model.best_params_['max_depth'])
    scores = cross_val_score(
        grid_tree_model, train_features, train_labels, cv=k)
    print("Decision Tree Cross Validation Accuracy: ",
          [round(score, 4) for score in scores])
    print("Decision Tree Average Cross Validation Accuracy: ", 
          round(scores.mean(), 4), "\n")


def k_nearest_neighbors(train_data, k):
    """
    Trains the knn classifier given training data and k and prints the mean 
    k-fold cross validation accuracy
    """
    train_labels = train_data['rating_bin']
    train_features = train_data.loc[:, train_data.columns != 'rating_bin']

    hyperparameters = {'n_neighbors': [1, 3, 5, 10, 15, 40, 50, 70, 100]}
    knn_model = KNeighborsClassifier()
    grid_knn_model = GridSearchCV(knn_model, param_grid=hyperparameters)
    grid_knn_model.fit(train_features, train_labels)

    print("k-Nearest Neighbors Best Hyperparameters:")
    print("n_neighbors: ", grid_knn_model.best_params_['n_neighbors'])
    scores = cross_val_score(
        grid_knn_model, train_features, train_labels, cv=k)
    print("k-Nearest Neighbors Cross Validation Accuracy: ", 
          [round(score, 4) for score in scores])
    print("k-Nearest Neighbors Average Cross Validation Accuracy: ", 
          round(scores.mean(), 4), "\n")


def random_forest(train_data, k):
    """
    Trains the random forest classifier given training data and k and prints 
    the mean k-fold cross validation accuracy
    """
    train_labels = train_data['rating_bin']
    train_features = train_data.loc[:, train_data.columns != 'rating_bin']

    hyperparameters = {'min_samples_leaf': [1, 2, 5],
                       'max_depth': [1, 5, 10, 20, 25, 26, 27, 28, 29, 30, 50]}
    random_tree_model = RandomForestClassifier(random_state=1)
    grid_random_tree_model = GridSearchCV(
        random_tree_model, param_grid=hyperparameters)
    grid_random_tree_model.fit(train_features, train_labels)

    print("Random Forest Best Hyperparameters:")
    print("min_samples_leaf: ", 
          grid_random_tree_model.best_params_['min_samples_leaf'], " | ", 
          "max_depth: ", grid_random_tree_model.best_params_['max_depth'])
    scores = cross_val_score(
        grid_random_tree_model, train_features, train_labels, cv=k)
    print("Random Forest Cross Validation Accuracy: ",
          [round(score, 4) for score in scores])
    print("Random Forest Average Cross Validation Accuracy: ", 
          round(scores.mean(), 4), "\n")


def adaboost(train_data, k):
    """
    Trains the adaboost classifier given training data and k and prints the 
    mean k-fold cross validation accuracy
    """
    train_labels = train_data['rating_bin']
    train_features = train_data.loc[:, train_data.columns != 'rating_bin']

    hyperparameters = {'n_estimators': [1, 2, 5, 10, 15, 20, 50, 100, 200]}
    adaboost_model = AdaBoostClassifier(random_state=1)
    grid_adaboost_model = GridSearchCV(
        adaboost_model, param_grid=hyperparameters)
    grid_adaboost_model.fit(train_features, train_labels)

    print("Adaboost Best Hyperparameters:")
    print("n_estimators: ", grid_adaboost_model.best_params_['n_estimators'])
    scores = cross_val_score(
        grid_adaboost_model, train_features, train_labels, cv=k)
    print("Adaboost Cross Validation Accuracy: ", 
          [round(score, 4) for score in scores])
    print("Adaboost Average Cross Validation Accuracy: ", 
          round(scores.mean(), 4), "\n")
    

def test_random_forest(train_data, test_data, min_samples_leaf, max_depth):
    train_labels = train_data['rating_bin']
    train_features = train_data.loc[:, train_data.columns != 'rating_bin']
    test_labels = test_data['rating_bin']
    test_features = test_data.loc[:, test_data.columns != 'rating_bin']

    random_tree_model = RandomForestClassifier(
        min_samples_leaf=min_samples_leaf, max_depth=max_depth, random_state=1)
    random_tree_model.fit(train_features, train_labels)
    test_score = random_tree_model.score(test_features, test_labels)
    print(test_score)


def main():
    df = pd.read_csv('skincare_data.csv')
    # Find skus of products with incomplete ingredients lists with 
    # cl.find_incomp_ingred_lists(df)
    df = prep.clean_data(
        df, incomplete_ingred_skus='incomplete_ingredients_skus.txt')
    junction_table = prep.create_junction_table(df)
    
    # Add features based on ingredients
    df['ingredient_counts'] = prep.get_total_ingredient_count(
        df, junction_table)
    df = prep.add_contains_ingredient(df)
    df = prep.add_ingredient_portion(df)
    #df = prep.add_top_ingredient_count(df, junction_table, top_percentile=0.25)

    df.to_csv('processed_data.csv', index=None, sep=',')  
    
    df = classification_preprocess(df)
    train_data, test_data = train_test_split(
        df, test_size=0.2, random_state=6)
    
    # Train classifiers
    majority_class_classifier(train_data, test_data, k=5)
    logistic_regression(train_data, k=5)
    decision_tree(train_data, k=5)
    k_nearest_neighbors(train_data, k=5)
    random_forest(train_data, k=5)
    adaboost(train_data, k=5)
    
    # Test best classifer
    test_random_forest(train_data, test_data, min_samples_leaf=1, max_depth=28)


if __name__ == '__main__':
    main()
