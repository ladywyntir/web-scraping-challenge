 # Automates browser actions
from splinter import Browser

# Parses the HTML
from bs4 import BeautifulSoup as soup

# For scraping with Chrome
from webdriver_manager.chrome import ChromeDriverManager

# import time module
import datetime as dt


def scrape_all():
    # setup ChromeDriverManager
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # scrape the info from the news page
    news_date, news_title, news_paragraph = scrape_mars_news(browser)
    
    # add scraped info to a dictionary
    mars_dict = {
        "newsDate": news_date,
        "newsTitle": news_title,
        "newsParagraph": news_paragraph,
        "featuredImg": scrape_imgs(browser),
        "facts": scrape_facts(browser),
        "hemispheres": scrape_hemis(browser),
        "last_updated": dt.datetime.now()
    }

    # stop the web driver
    browser.quit()

    # print the output
    return mars_dict


# scrape the mars news page
def scrape_mars_news(browser):

    # set a variable for the MARS Planet Science news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # delay for loading the page to give content time to populate - I updated this to 3 seconds
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=3)

    # use Beautiful Soup to select an article and parse the data 
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    # find the selected article's date
    news_date = slide_elem.find("div", class_='list_date').get_text()
    
    # find the selected article's title
    news_title = slide_elem.find("div", class_='content_title').get_text()
    
    # find the selected article's title
    news_p = slide_elem.find("div", class_='article_teaser_body').get_text()

    # print the Date, Title and Paragraph
    return news_date, news_title, news_p

# scrape the Featured Image page
def scrape_imgs(browser):
    # go to the image website
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    # search for the full image button and click it
    full_image = browser.find_by_tag('button')[1]
    full_image.click()

    # use Beautiful Soup to get the html and parse the data 
    img_html = browser.html
    img_soup = soup(img_html, 'html.parser')

    # find the selected image URL
    img_url_cur = img_soup.find('img', class_='fancybox-image').get('src')
    
    # use the base URL to create an abosulte URL
    img_url = f'https://spaceimages-mars.com/{img_url_cur}'
    
    # print the Featured Image URL
    return img_url

# scrape through the Facts page
def scrape_facts(browser):
    # goes to the Facts website
    facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(facts_url)

    # use Beautiful Soup to select an article and parse the data 
    facts_html = browser.html
    facts_soup = soup(facts_html, 'html.parser')

    # find the location of the info on the webpage
    facts_loc = facts_soup.find('div', class_="diagram mt-4")
    facts_tab = facts_loc.find('table')

    # create an empty string
    mars_facts = ""

    # add our facts_tab info into the string
    mars_facts += str(facts_tab)

    # print the table
    return mars_facts

# scrape through the Hemisphere pages
def scrape_hemis(browser):
    # 1. Use browser to visit the URL 
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=3)

    # create a list to hold images and titles
    hemi_image_data = []

    # Parse the html with beautifulsoup
    hemi_html = browser.html
    hemi_soup = soup(hemi_html, 'html.parser')

    # new list to hold the titles and images
    hemi_images_urls = []

    # make a list of hemispheres
    hemi_links = browser.find_by_css('a.product-item img')

    # loop through each link, click on it and return the href 
    for h in range(len(hemi_links)):
        # dictionary for each hemisphers' info
        hemi_info = {}
        
        # search for the elements so we avoid exceptions
        browser.find_by_css('a.product-item img')[h].click()
        
        # find the image url and extract href
        hemi_img_sample = browser.links.find_by_text('Sample').first
        hemi_info["img_url"]= hemi_img_sample['href']
        #print(hemi_img_sample['href'])
        
        # throw in the titles
        hemi_info['title'] = browser.find_by_css('h2.title').text
        
        # add hemisphere objects and titles to the list
        hemi_images_urls.append(hemi_info)
        
        # adding code to return to the previous web page
        browser.back()

    # print the Hemispheres info
    return hemi_images_urls


# set up as flask app
if __name__ == "__main__":
    print(scrape_all())