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

## Installation

1. Clone this repository to your computer
2. Navigate to the project directory `cd skincare` from your terminal
3. Install the requirements using `pip install -r requirements`
    * The python version is Python 3.8
    * You may want to use a virtual environment for this


## Usage 

### Web Scraping

**web_scrape.py** scrapes the Soko Glam website for product info, ratings, 
and ingredients lists of skincare products using the Beautiful Soup library 
(as of Feb 2022), which creates the sokoglam_data.csv file.

**test_scrape.py** tests the functions in the **sokoglam_scrape.py** file.

**sokoglam_data.csv** contains the raw data scraped from the Soko Glam website 
in Feb 2022.

### Cleaning

**clean.py** implements functions to clean the raw data scraped from the Soko 
Gram website.

**test_clean.py** tests the functions in the **clean.py** file.
