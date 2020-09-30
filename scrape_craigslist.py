'''
Functions used to scrape Craigslist postings: 
* Scrapes a single listing row on a page: get_listing_details(post)
* Scrape all listing rows on a page: get_page_listings(page)
* Compile all listing rows from a page into a Pandas DataFrame: clpage_to_df(soup)
'''


from bs4 import BeautifulSoup
import requests

import numpy as np
import pandas as pd


def get_listing_details(post):
    '''
    Function to main posting details from an individual line-item post on craiglist
    Returns as a list of post elements: 
        [date, title, post url (link), price, neighborhood, # bedrooms, square footage]
    '''
    
    # These items are present in every post
    date = post.find('time', class_='result-date').text
    title = post.find('a', class_='result-title hdrlnk').text
    link = post.find('a', class_='result-title hdrlnk')['href']
    price = int(post.find('span', class_='result-price').text.strip().replace("$","").replace(",",""))
    
    # Neighborhood, # BRs, and sqft are all optional fields
    # use series of if/else statements to find value or assign as np.nan

    # Test for neighborhood field
    if post.find('span', class_='result-hood') is None:
        hood = np.nan
    else:
        hood = post.find('span', class_='result-hood').text.strip()[1:][:-1]
    
    # Test to for BR and SQFT info
    if post.find('span', class_='housing') is None:
        # Set both BRs and sq-ft to np.nan
        brs = np.nan
        sqft = np.nan
        
    elif len(post.find('span', class_='housing').text.split()) < 3:
        # test to see if we have BR
        if post.find('span', class_='housing').text.split()[0][-2:] == 'br':
            brs = int(post.find('span', class_='housing').text.split()[0][:-2])
            sqft = np.nan
        else:
            sqft = int(post.find('span', class_='housing').text.split()[0][:-3])
            brs = np.nan
             
    else:
        # We have both BRs and sq-ft      
        brs = post.find('span', class_='housing').text.split()[0][:-2]
        sqft = int(post.find('span', class_='housing').text.split()[2][:-3])     
    
    # Order of elements to be returned
    post_elements = [date, title, link, price, brs, sqft, hood]
    
    return post_elements


def get_page_listings(page):
    '''
    Function to scrape an entire page of craigslist postings
    Calls on `get_listing_details()` function to scrape indvidual post elements
    Returns a list of lists (of post elements)

    (A full page of postings on CL contains 120 listings)
    '''
    post_counter = 0
    page_results = []
    
    for post in page:
        listing = get_listing_details(post)
        page_results.append(listing)
        post_counter += 1
        
    print("Scrape Complete!")
    print("Number of Postings Scraped: {}".format(post_counter))        
    return page_results    


def clpage_to_df(soup):
    '''
    Function to create a Pandas DataFrame from one entire craiglist page
    calls on `get_page_listings(postings)`, which calls on `get_listing_details(post)`

    Returns a Pandas DataFrame containing a page of listings
    '''
    
    headers = ['date', 'title', 'link', 'price', 'brs', 'sqft', 'hood']

    postings = soup.find_all('li', class_='result-row')
    data = get_page_listings(postings)
    df = pd.DataFrame(data, columns=headers)
    
    return df
