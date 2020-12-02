from bs4 import BeautifulSoup
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    components = {}

    # Scrape title and description paragraph from nasa news site

    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    step1 = news_soup.find('ul', class_='item_list')

    # Error says NoneType object has no attribute 'find', NoneType = step1

    step2 = step1.find('li', class_='slide')
    title = step2.find('div',class_='content_title').text

    target = "div[class='article_teaser_body']"
    news_p_raw = browser.find_by_tag(target)

    news_p = news_p_raw.text.strip()

    components['title'] = title
    components['news_p'] = news_p

    browser.quit()

    # Scrape featured image url from nasa spaceimages

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    target = "a[class='button fancybox']"
    browser.find_by_tag(target).click()

    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_soup = soup.find('figure', class_='lede')
    image_url = image_soup.a['href']

    feature_image_url = 'https://www.jpl.nasa.gov' + image_url

    components['feature_image_url'] = feature_image_url

    browser.quit()

    # Scrape mars facts table from space-facts

    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    mars_facts_db = tables[0]

    mars_facts_db.rename({0: 'Descripter', 1: 'Values'}, axis=1)

    mars_facts = mars_facts_db.to_html(index=False)

    components['mars_facts'] = mars_facts

    browser.quit()

    # Scrape titles and image urls for each mars hemisphere

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Cerberus Hemisphere

    browser.click_link_by_partial_text('Cerberus')

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_soup = soup.find('li')
    image_url = image_soup.a['href']
    image_url

    title = soup.find('h2', class_="title").text

    cerb_dict = {'title': title, 'image_url': image_url}

    # Schiaparelli Hemisphere

    browser.click_link_by_partial_text('Schiaparelli')

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_soup = soup.find('li')
    image_url = image_soup.a['href']
    
    title = soup.find('h2', class_="title").text

    schiap_dict = {'title': title, 'image_url': image_url}

    # Syrtis Major Hemisphere

    browser.click_link_by_partial_text('Syrtis')

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_soup = soup.find('li')
    image_url = image_soup.a['href']

    title = soup.find('h2', class_="title").text

    syrtis_dict = {'title': title, 'image_url': image_url}

    # Valles Marineris Hemisphere

    browser.click_link_by_partial_text('Valles')

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_soup = soup.find('li')
    image_url = image_soup.a['href']

    title = soup.find('h2', class_="title").text

    valles_dict = {'title': title, 'image_url': image_url}

    # List of all hemisphere dictionaries

    hemisphere_image_urls = [cerb_dict, schiap_dict, syrtis_dict, valles_dict]

    components['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()

    return components

