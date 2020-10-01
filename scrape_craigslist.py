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
        
    print("Listing page scrape complete!")
    print("Number of postings scraped: {}".format(post_counter))        
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


def get_post_amenities(url_list):
    '''
    Function to scrape a list of Craigslist URLs for # bathrooms & list of amenities. 
    
    Input:  List of urls to scrape   
    Output: (1) List of bathroom counts from scraped urls (bathrooms_list)
            (2) List of amenities lists from scraped urls (amenities_list)
    '''
    
    bathrooms_list = []
    amenities_list = []
    
    index = 0
    
    for url in url_list:
        
        response = requests.get(url)
        page = response.text
        soup = BeautifulSoup(page, 'html.parser')
        
        # Each post has 3 possible groupings: 
        # -- Group 1: Bathroom information (+ BRs, sqft, availability date)
        # -- Group 2: Open House dates
        # -- Group 3: List of amenities
        
        # None are required fields, so each post can be different
        
        # Test how many groups there are: 
        
        # If > 1 group: 
        if len(soup.find_all('p', class_='attrgroup')) > 1:
            
            group1 = soup.find_all('p', class_='attrgroup')[0].text.split('\n')
            item_list1 = [item for item in group1 if item != '']
            
            # Check to see if first grouping contains number of bathrooms
            
            if item_list1[0][-2:] == 'Ba':
                brba = item_list1[0].split(' / ')
                bath = brba[-1]
            
            # if not bathrooms, then NaN and move on
            else:
                bath = np.nan
    
            # Grouping 2 will be either open house dates or amenities:
        
            # If only 2 groups, then return amenities
            # If there are 3 groups, skip group 2 (Open House dates) and return amenities
            
            if len(soup.find_all('p', class_='attrgroup')) == 2:
            
                group2 = soup.find_all('p', class_='attrgroup')[1].text.split('\n')
                amenities = [item for item in group2 if item != '']
                
            else:
                group2 = soup.find_all('p', class_='attrgroup')[2].text.split('\n')
                amenities = [item for item in group2 if item != '']         
        
        # If only 1 group 
        
        elif len(soup.find_all('p', class_='attrgroup')) == 1:
            
            items = soup.find_all('p', class_='attrgroup')[0].text.split('\n')
            item_list = [item for item in group1 if item != '']
            
            # Check to see if that group contains number of bathrooms
            if item_list[0][-2:] == 'Ba':
                brba = item_list1[0].split(' / ')
                bath = brba[-1]
            
            # otherwise, we just have amenities
            else:
                amenities = item_list
        
        # If no details on post page, fill with NaN
        else:
            bath = np.nan
            amenities = np.nan
  
        # Append bathroom count and amenities to lists:
        bathrooms_list.append(bath)
        amenities_list.append(amenities)
        
        # For Testing Purposes -- remove later:
        #print("Index: ", index)      
        #print("Baths: ", bath)
        #print("Amens: ", amenities)
        #print("")
        
        index += 1
        
    print("Individual posts scrape complete!")
    print("Number of posts scraped: ", index)        
    
    return bathrooms_list, amenities_list


def full_page_scrape(url):
    '''
    Function to scrape Craigslist page of listings, and then scrape each post
    within that page for number of bathrooms and amenities. 
    
    Calls on `get_post_amenities()` function for second-level scrape
    
    Input:   url of Craigslist apt/housing rental listings
    Output:  DataFrame of listings
    '''
     
    response = requests.get(url)
    
    if response.status_code == 200:
        page = response.text

        # Create soup object from URL
        soup = BeautifulSoup(page, 'html.parser')
    
        # Create DF
        df = clpage_to_df(soup)
        
        # Scrape each listing URL for amenities: 
        post_urls = list(df.link)
        post_details = get_post_amenities(post_urls)
        
        # Add amenities to df
        baths = post_details[0]
        amenities = post_details[1]
        
        df['bath'] = baths
        df['amenities'] = amenities
        
        return df

