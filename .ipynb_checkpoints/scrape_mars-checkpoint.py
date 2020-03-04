import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from selenium import webdriver
import requests as req
import re

from splinter import browser
from selenium import webdriver


def scrape():
#scrape the NASA Mars News SIte, collect news title, paragraph text, assign
#to variables for later reference
    url = "https://mars.nasa.gov/news/"
    response = req.get(url)
    soup = bs(response.text, 'html5lib')

#scrape the title and accompanying paragraph
    news_title = soup.find("div", class_="content_title").text
    paragraph_text = soup.find("div", class_="rollover_description_inner").text

#Visit the URL for JPL's Space images
#splinter to navigate the site and find the image url for the current featured
#image and assign it to featured_image_url (use .jpg)

#set up splinter
    executable_path = {'executable_path' : 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

#stir soup for scraping
    html = browser.html
    soup = bs(html, "html.parser")

#have webdriver click links to get to the full image I want
    browser.click_link_by_partial_text('FULL IMAGE')

#had to add this, wasn't working and docs recommended waiting between clicks
    time.sleep(5)
    browser.click_link_by_partial_text('more info')

#stir new soup for scraping the image url
    new_html = browser.html
    new_soup = bs(new_html, 'html.parser')
    temp_img_url = new_soup.find('img', class_='main_image')
    back_half_img_url = temp_img_url.get('src')

    recent_mars_image_url = "https://www.jpl.nasa.gov" + back_half_img_url

#get mars weather. THE INSTRUCTIONS SAY SPECIFICALLY TO SCRAPE THE DATA
#stir soup
    twitter_response = req.get("https://twitter.com/marswxreport?lang=en")
    twitter_soup = bs(twitter_response.text, 'html.parser')

#use find_all to get all the tweets on the page, scan the 10 most recent for "Sol"
    tweet_containers = twitter_soup.find_all('div', class_="js-tweet-text-container")
    for i in range(10):
        tweets = tweet_containers[i].text
        if "Sol " in tweets:
            mars_weather = tweets
            break

#Mars Facts....visit webpage, use pandas to scrape the page for facts,
#convert pandas table to html table string.
    request_mars_space_facts = req.get("https://space-facts.com/mars/")

#use pandas to scrape html table data
    mars_space_table_read = pd.read_html(request_mars_space_facts.text)
    df = mars_space_table_read[0]

#set the index to the titles of each statistic/value
    df.set_index(0, inplace=True)
    mars_data_df = df

#convert new pandas df to html, replace "\n" to get html code
    mars_data_html = mars_data_df.to_html()
    mars_data_html.replace('\n', '')
    mars_data_df.to_html('mars_table.html')

#..Visit the USGS Astrogeology site to obtain hgih resolution images for
#....each of Mar's hemispheres
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    usgs_req = req.get(usgs_url)

#..You will need to click each of the links to the hemispheres in order
#....to find full res image

#had trouble doing this with splinter, decided to just do a bunch of loops for img urls
    soup = bs(usgs_req.text, "html.parser")
    hemi_attributes_list = soup.find_all('a', class_="item product-item")
#list to keep the dictionaries that have title and image url
    hemisphere_image_urls = []
    for hemi_img in hemi_attributes_list:
        #get the img title
        img_title = hemi_img.find('h3').text
        #print(img_title)
        #get the link to stir another soup, this is the page with the actual image url
        link_to_img = "https://astrogeology.usgs.gov/" + hemi_img['href']
        #print(link_to_img)
        img_request = req.get(link_to_img)
        soup = bs(img_request.text, 'lxml')
        img_tag = soup.find('div', class_='downloads')
        img_url = img_tag.find('a')['href']
        hemisphere_image_urls.append({"Title": img_title, "Image_Url": img_url})

    mars_data = {
     "News_Title": news_title,
     "Paragraph_Text": paragraph_text,
     "Most_Recent_Mars_Image": recent_mars_image_url,
     "Mars_Weather": mars_weather,
     "mars_h": hemisphere_image_urls
     }#Fix the title collection in the images scraper
#build the web page
#clean up the code

from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': r'\Users\patti\LearnPython\ClassGit\GWARL201902DATA3\02-Homework\Mission_to_Mars\chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}

    #visit url
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #pull html text and parse
    html_code = browser.html
    soup = BeautifulSoup(html_code, "html.parser")

    #grab needed info
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="rollover_description_inner").text




    # # Latest Featured Image

    # Featured Image URL & visit
    #Uncomment here##
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    #navigate to link
    #uncomment here
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')

    #get html code once at page
    #uncomment here
    image_html = browser.html

    #parse
    #uncomment
    soup = BeautifulSoup(image_html, "html.parser")

    #find path and make full path
    #uncomment
    image_path = soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov" + image_path




    # # Mars Weather
     #weather url and html
    marsweather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(marsweather_url)
    weather_html = browser.html

    #get lastest tweet
    soup = BeautifulSoup(weather_html, 'html.parser')
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text



    # # Mars Facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    #get html
    facts_html = browser.html
    soup = BeautifulSoup(facts_html, 'html.parser')

    #get the entire table
    table_data = soup.find('table', class_="tablepress tablepress-id-mars")

    #find all instances of table row
    table_all = table_data.find_all('tr')

    #set up lists to hold td elements which alternate between label and value
    labels = []
    values = []

    #for each tr element append the first td element to labels and the second to values
    for tr in table_all:
        td_elements = tr.find_all('td')
        labels.append(td_elements[0].text)
        values.append(td_elements[1].text)
            
#uncomment    #make a data frame
    mars_facts_df = pd.DataFrame({
        "Label": labels,
        "Values": values
    })

     # get html code for DataFrame
    fact_table = mars_facts_df.to_html(header = False, index = False, escape=False)
    fact_table


 

#Hemisphere Images Scraping
    hemispheres_url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    soup = BeautifulSoup(hemispheres_html, 'html.parser')
    mars_hemispheres = soup.find_all('h3')
	
	
    hemisphere_image_urls = []
	#Loop to scrape all hemispheres
    for row in mars_hemispheres:
        title= row.text
        browser.click_link_by_partial_text(title)
        time.sleep(1)
        img_html = browser.html
        soup_h = BeautifulSoup(img_html, 'html.parser')
        url_img = soup_h.find('div',class_='downloads').a['href']
        print ("Hemisphere Name :  "+ str(title))
        print ("Hemisphere URL:  " + str(url_img))

        img_dict = {}
        img_dict['title']= title
        img_dict['img_url']= url_img
        hemisphere_image_urls.append(img_dict)	
        
        browser.visit(hemispheres_url)



    listings = {
        "id": 1,
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
       "fact_table": fact_table,
       "hemisphere_images": hemisphere_image_urls
    }

    #return mars_dict

    return listings

    return mars_data