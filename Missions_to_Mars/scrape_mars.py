# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_info():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # # NASA Mars News
    # ### Scrape the "Mars News Site" and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(1)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # scrape the first title
    news_title = soup.find('div', class_='content_title').text

    # scrape the first paragraph
    news_p = soup.find('div', class_='article_teaser_body').text

    # # JPL Mars Space Images - Featured Image

    # URL of page to be scraped
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # scrape for URL
    featured_image_url = url + soup.find('a', class_='showimg fancybox-thumbs')['href']

    # # Mars Facts
    # ### Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

    # URL of page to be scraped
    url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(url)

    # ### Use Pandas to convert the data to a HTML table string.

    df = tables[1]

    html_table = df.to_html(header=False, index=False)

    # # Mars Hemispheres

    # URL of page to be scraped
    list_url = ['https://marshemispheres.com/cerberus.html', 'https://marshemispheres.com/schiaparelli.html', 'https://marshemispheres.com/syrtis.html', 'https://marshemispheres.com/valles.html']

    mars_hemi_list = []

    for x in list_url:
        browser.visit(x)
        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')
        
        # scrape the title
        title = soup.find('h2', class_='title').text
        #scrape the full size image url
        href = 'https://marshemispheres.com/' + soup.find('img', class_='wide-image')['src']

        # Dictionary to be inserted as a MongoDB document    
        v={'title': title, 'img_url': href}
        mars_hemi_list.append(v)

    mars_dict ={
        "Title" : news_title,
        "Summary" : news_p,
        "ImageURL" : featured_image_url,
        "MarsStats" : html_table,
        "MarsHemi" : mars_hemi_list
    }

    print(mars_dict)

    # Quit the browser
    browser.quit()

    return mars_dict