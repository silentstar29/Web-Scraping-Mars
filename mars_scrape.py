# Import BeautifulSoup
from bs4 import BeautifulSoup
import pandas as pd
import time
from splinter import Browser

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # create surf_data dict that we can insert into mongo
    mars_data = {}

    
    # # NASA Mars News
    url= "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    

    news_title= soup.find('div',class_="content_title").text
    print(news_title)
    time.sleep(3)
    news_p=soup.find('div', class_="article_teaser_body").text
    print(news_p)

# Add the news title and summary to the dictionary
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p


    # # JPL Mars Space Image

    image_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    button= browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(3)
    button= browser.click_link_by_partial_text('more info')
    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_path = soup.find('figure',class_="lede").a['href']
    url= "https://www.jpl.nasa.gov"
    featured_img_url = url + featured_image_path
    featured_img_url

# Add the featured image url to the dictionary
    mars_data["featured_img_url"] = featured_img_url


    # # Twitter Mars Weather

    weather_url= "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scrape the latest Mars weather tweet from the page. 
    # Save the tweet text for the weather report as a variable called `mars_weather`.

    mars_weather= soup.find('div',class_="js-tweet-text-container").p.text
    print(mars_weather)

    # Add the weather to the dictionary
    mars_data["mars_weather"] = mars_weather



    # # Space Facts Mars

    import pandas as pd

    facts_url= "https://space-facts.com/mars/"

    tables=pd.read_html(facts_url)
    tables

    type(tables)

    facts_df=tables[0]
    facts_df.columns= ['description','value']
    facts_df.head()

    facts_df.set_index('description', inplace=True)
    facts_df

    facts_to_html=facts_df.to_html()
    facts_to_html

    facts_table= facts_to_html.replace('\n', '')
    facts_table

    type(facts_table)

# Add the Mars facts table to the dictionary
    mars_data["facts_table"] = facts_table

    # # Mars Hemispheres

    mars_hem_url= "https://usgs.gov/"
    browser.visit(mars_hem_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_head=soup.find('h1', class_="page-header").text
    print(mars_head)

    time.sleep(3)

    mars_hem=soup.find('p', class_="alert alert-danger").text
    print(mars_hem)

#Add USGS info to the dictionary:
    mars_data["mars_head"]= mars_head
    mars_data["mars_hem"]= mars_hem

    
    mars_url="https://www.jpl.nasa.gov/spaceimages/search_grid.php?sort=target&instrument=Wide+Field+Planetary+Camera+2&currentpage=3"
    browser.visit(mars_url)

    button= browser.click_link_by_partial_href('PIA01252')
    time.sleep(3)
    button= browser.click_link_by_partial_text('jpg')
    time.sleep(3)

    mars_hemispheres_image_url=browser.url
    mars_hemispheres_image_url

    # Add the alternative image url to the dictionary
    mars_data["mars_hemispheres_image_url"] = mars_hemispheres_image_url
    browser.quit()
# Return the dictionary
    return mars_data

  




