# Skincare Analysis

Many skincare products promise to address skincare concerns, from 
hyperpigmentation to acne to anti-aging. However, if the product doesn't 
contain the right ingredients that will have the desired effect on skin, no 
amount of marketing will make the product work. Thus, many skincare 
enthusiasts will compare and choose skincare products by looking at the 
ingredient lists. This is why websites that act as a reference for the 
ingredients of different skincare products like Skincarisma exists.

Certain ingredients have risen to a certain level of popularity among skincare 
communities and forums as many have found that products containing these highly 
desired ingredients have a relatively high rate of success. Thus, many skincare 
products now advertise high concentrations of these ingredients.

An analysis into the data from Skincarisma will give a deeper insight into the 
effects of these popular ingredients. It will help affirm (or not) these beliefs 
that the ingredients of skincare products matter the most, and whether popular 
ingredients are as effective as many believe them to be.

## Web Scraping

**webscrape.py** scrapes the Skincarisma website for ingredients lists, reviews, and 
other data about skincare products using the Beautiful Soup library (as of Feb 
2021), which creates the skincare_data.csv file.

**create_small_data.py** can be used to create smaller files by randomly selecting 
products from skincare_data.csv, which can be used for testing. This was used 
to create **small_skincare.csv** and **medium_skincare.csv**.

**skincare_id.csv** attaches a product ID number to each product in 
**skincare_data.csv**.

## Analysis

**ingredients_and_reviews.py** impletements and executes functions that 
analyzes skincare data to answer the question of whether products with certain 
ingredients more likely to be well-reviewed by users.

**similar_ing_and_ratings.py** analyzes skincare data to answer the question of 
how accurately are we able to predict popularity/likeability of a product based 
on its traits.

**traits_and_popularity.py** analyzes skincare data to answer the question of 
whether if products with similar ingredients have similar ratings.

**test.py** tests the functions in the previous three files.
