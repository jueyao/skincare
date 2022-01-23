"""
Impletements and executes functions that analyzes skincare data scraped
from the Skincarisma website
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


sns.set()


def make_ingredients_alias_dict():
    """
    Returns a dict containing the aliases, chemical derivatives, or names of
    subtypes of desirable skincare ingredients
    """
    ingred_aliases = dict()
    ingred_aliases['BHA'] = [
        'bha', 'salicylic acid', 'capryloyl salicylic acid'
    ]
    ingred_aliases['AHA'] = [
        'glycolic acid', 'lactic acid', 'lactic acid/glycolic acid copolymer',
        'tartaric acid', 'citric acid', 'malic acid', 'mandelic acid'
    ]
    ingred_aliases['PHA'] = [
        'gluconolactone', 'delta gluconolactone', 'galactose',
        'lactobionic acid'
    ]
    ingred_aliases['Niacinamide'] = ['niacinamide']
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
    ingred_aliases['Vitamin A'] = ['retinol']
    ingred_aliases['Hyaluronic Acid'] = ['hyaluronic acid']
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
    ingred_aliases['Azelaic Acid'] = ['azelaic acid']
    ingred_aliases['Squalane'] = [
        'squalane', 'olive squalane', 'phytosqualane']
    ingred_aliases['Snail Mucin'] = [
        'snail secretion filtrate', 'snail secretion filtrate extract',
        'saccharomyces/snail Secretion filtrate ferment filtrate'
    ]
    ingred_aliases['Madecassoside'] = [
        'centella asiatica', 'centella asiatica extract',
        'centella asiatica callus extract',
        'centella asiatica leaf cell extract',
        'centella asiatica leaf extract', 'centella asiatica leaf water',
        'centella asiatica meristem cell culture', 'madecassoside'
    ]
    ingred_aliases['Urea'] = ['urea']
    return ingred_aliases


def unique_products(data):
    """
    Returns a dataframe of unique products without the ingredients column
    given a dataframe of products and their ingredients stored in tidy
    format
    """
    unique = data.copy()
    unique.drop('Ingredients', inplace=True, axis=1)
    unique = unique.drop_duplicates()

    return unique


def assign_product_id(data):
    """
    Assigns a unique product ID to each product in dataframe where each
    ingredient of a product results in an otherwise identical, duplicate row
    """
    unique = unique_products(data).reset_index()

    product_id = []
    for i in range(0, len(data)):
        same_name = unique['Product_Name'] == data.loc[i, 'Product_Name']
        same_brand = unique['Brand'] == data.loc[i, 'Brand']
        same_category = unique['Category'] == data.loc[i, 'Category']
        same_rating = unique['Rating'] == data.loc[i, 'Rating']
        same_ratings_count = unique['Ratings_Count'] == \
            data.loc[i, 'Ratings_Count']
        product = unique[same_name & same_brand & same_category & same_rating &
                         same_ratings_count]
        product_id.append(product.index[0])

    with_product_id = data.copy()
    with_product_id['product_id'] = product_id

    return with_product_id


def mean_ingredient_rating(data, ingredient, aliases):
    """
    Returns the mean rating for all skincare products containing the given
    ingredient. Only uses products with at least 1 rating for calculation.
    Ignores capitalization.
    Returns None if the ingredient is not in the dict of popular ingredients
    and their aliases.
    Each product is only counted once even if it contains multiple subtypes of
    the ingredient.
    """
    if ingredient not in aliases.keys():
        return None

    one_or_more_rating = data[data['Ratings_Count'] != 0]

    contains_ingred = one_or_more_rating[
        one_or_more_rating['Ingredients'].str.lower().isin(aliases[ingredient])
    ]
    contains_ingred = unique_products(contains_ingred)

    return contains_ingred['Rating'].mean()


def plot_mean_ratings(data, ingred_aliases):
    """
    Plots the mean rating for skincare products containing popular ingredients,
    as well as the mean for all products in the data.
    """
    all_rated_products = data[data['Ratings_Count'] != 0]
    ingredients_ratings = {
        'Ingredients': ['All'],
        'Mean Ratings': [all_rated_products['Rating'].mean()]
    }

    for ingredient in ingred_aliases.keys():
        ingredients_ratings['Ingredients'].append(ingredient)
        ingredients_ratings['Mean Ratings'].append(
            mean_ingredient_rating(data, ingredient, ingred_aliases)
        )

    ingredients_ratings = pd.DataFrame(data=ingredients_ratings)

    plot = sns.catplot(x='Mean Ratings', y='Ingredients',
                       data=ingredients_ratings, kind='bar', color='#a1e6f7')

    plt.xlabel('Mean Rating (Out of 5)')
    plt.title('Mean Ratings of Products Containing Popular Ingredients')
    plt.xlim(0, 5)
    plot.set(ylabel=None)

    plot.savefig('bar_chart_mean_ratings.png')


def percent_containing_ingredient(data, ingredient, aliases):
    """
    Returns the percent of products in the given dataset that contains the
    given ingredient.
    Uses all names/subcategories of the ingredient as given in the dict of
    aliases.
    Rounds to 2 decimal places.
    """
    contains_ingred = data[
        data['Ingredients'].str.lower().isin(aliases[ingredient])
    ]
    contains_ingred = contains_ingred['product_id'].unique()

    contains_ingred_count = len(contains_ingred)
    total_products_count = len(data['product_id'].unique())

    return round((contains_ingred_count / total_products_count) * 100, 2)


def ingredients_in_top_rated(data, aliases, lowest_rating):
    """
    Returns a dataframe containing popular ingredients and the percent of top
    rated products that contains them.
    """
    top_products = data[data['Rating'] >= lowest_rating]

    percentages = {'Ingredients': [], 'Percentage': []}

    for ingredient in aliases.keys():
        percentages['Ingredients'].append(ingredient)
        percentages['Percentage'].append(
            percent_containing_ingredient(top_products, ingredient, aliases)
        )

    percentages = pd.DataFrame(data=percentages)
    return percentages


def plot_ingredients_percentages(data, aliases, lowest_rating):
    """
    Plots the percentages of top rated products that contains popular
    ingredients
    """
    percentages = ingredients_in_top_rated(data, aliases, lowest_rating)

    plot = sns.catplot(x='Percentage', y='Ingredients',
                       data=percentages, kind='bar', color='#a1e6f7')

    plt.xlabel('Percentages')
    plt.title('Percentages of ' + str(lowest_rating) +
              '+ Rated Products Containing Popular Ingredients')
    plt.xlim(0, 30)
    plot.set(ylabel=None)

    plot.savefig(str(lowest_rating) + 'plus_percentages' + '.png')


def main():
    skincare = pd.read_csv('skincare_data.csv')
    skincare_id = assign_product_id(skincare)
    skincare_id.to_csv('skincare_id.csv', index=False, header=True)
    skincare_id = pd.read_csv('skincare_id.csv')

    aliases = make_ingredients_alias_dict()

    plot_mean_ratings(skincare, aliases)
    plot_ingredients_percentages(skincare_id, aliases, 0)
    plot_ingredients_percentages(skincare_id, aliases, 4)
    plot_ingredients_percentages(skincare_id, aliases, 4.5)


if __name__ == '__main__':
    main()
