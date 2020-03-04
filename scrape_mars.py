#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from splinter import browser
from selenium import webdriver
import urllib.parse
import time #we will need it to add a sleep when scraping websites


# In[2]:

def scrape():
    #Scrape the NASA Mars News Site and collect the latest News Title 
    #and Paragraph Text. Assign the text to variables that you can reference later.

    #first set the URL

    url = 'https://mars.nasa.gov/news/'

    #retrieve the page

    response = requests.get(url)

    #check the response code


    # In[3]:


    #create a BeautifulSoup object and parse the page

    soup = BeautifulSoup(response.text, 'html.parser')

    #pretty print the results

    #print(soup.prettify())


    # In[4]:


    #get just the title
    news_title = soup.find('div', class_='content_title').text
    #we are going to put our results in a variable called news_title, and we are going to fetch the text of the 'content_title' div tag

    news_title


    # In[5]:


    #then we are going to drop the Newline characters

    clean_title = str(news_title)
    #print (clean_title)


    # In[6]:


    #now we are going to fetch a paragraph
    #it's of the class 'rollover_description_inner'

    news_p = soup.find('div', class_='rollover_description_inner').text
    news_p


    # In[7]:


    #drop the Newline's and other formatting


    clean_p = str(news_p)
    #print (clean_p)


    # In[8]:


    # Connect to a url to grab NASA's featured Mars image
    # Use selenium to navegate to the page with the image
    driver = webdriver.Firefox()
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    driver.get(url_image)
    time.sleep(1)
    elem = driver.find_element_by_id("full_image")
    elem.click()
    time.sleep(1)
    # Navigate to "more info" web site, where the full image URL is
    elem = driver.find_element_by_link_text("more info")
    elem.click()
    time.sleep(1)
    # Get the "more info" page URL to parse and find the image in full resolution
    url_more_info = driver.current_url
    # Use requests and soup to return the image url
    r = requests.get(url_more_info)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    featured_image_url = (
        "https://www.jpl.nasa.gov" + soup.find("figure", class_="lede").a["href"]
    )
    #print(featured_image_url)
    # Close the driver
    driver.close()


    # In[ ]:


    url_twitter = "https://twitter.com/marswxreport?lang=en"
    # Create a Beautiful Soup object
    r = requests.get(url_twitter)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    mars_weather = soup.find_all("div", class_="js-tweet-text-container")
    # find the first actual weather tweet
    mars_weather = mars_weather[0].text[:-26]
    #print(mars_weather)


    # In[ ]:





    # In[ ]:


    #Use Pandas to Scrape the Mars facts website.
    url_facts = 'https://space-facts.com/mars/'

    mars_table = pd.read_html(url_facts)
    mars_table[0]

    #pandas will automatically grab the table contents if it sees a table at the URL


    # In[ ]:


    #make it into a dataframe and name the columns

    mars_df = mars_table[0]
    mars_df.columns = ['Facts','Value']
    mars_df


    # In[ ]:


    #then convert it to html so we can later embed it in our webpage

    mars_html = mars_df.to_html(header=True, index =False)
    mars_html


    # In[ ]:


    #scrape the hemisphere photo data
    driver = webdriver.Firefox()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    driver.get(url)
    html = driver.html
    soup = BeautifulSoup(html,'html.parser')
    hemispheres = soup.find('div',class_='collapsible results')
    results = hemispheres.find_all('a')
    #print(results)


    # In[ ]:





    # In[ ]:



    #count how many results we have

    len(results)


    # In[ ]:


    #create an empty list

    hemispheres = []

    #populate it with the images data

    for result in results:
        if result.h3:
            title = result.h3.text
            link = 'https://astrogeology.usgs.gov' + result['href']
            #print(title,link)    
            browser.visit(link)
            time.sleep(5)
            image_html = browser.html
            soup = BeautifulSoup(image_html,'html.parser')
            soup_image = soup.find('div', class_='downloads').find('li').a['href']
            #print(soup_image)
            mars_images = {'title':title, 'img_url':soup_image}
            hemispheres.append(mars_images)


    # In[ ]:


    #print the list

    #print(hemispheres)

    listings = {
        "id": 1,
        "news_title": clean_title,
        "news_p": clean_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
       "fact_table": mars_df,
       "hemisphere_images": hemispheres
    }


    return listings
print(scrape())