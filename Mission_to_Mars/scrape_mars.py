import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(5)

    html = browser.html
    soup = bs(html, 'html.parser')
    mars_title = soup.select_one("div.list_text").find("div", class_="content_title").get_text()
    # data = {"News Title":mars_title}
    mars_paragraphs = soup.select_one("div.list_text").find('div', class_="article_teaser_body").get_text()
    featured_image_url = 'https://spaceimages-mars.com/'
    browser.visit(featured_image_url)
    browser.find_by_tag('button')[1].click()
    featured_image=browser.find_by_css('img.fancybox-image')[0]['src']
    url = 'https://galaxyfacts-mars.com/'
    mars_facts_tables = pd.read_html(url)
    mars_info_df = mars_facts_tables[0]
    mars_html = mars_info_df.to_html()
    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)
    num_of_thumb = len(browser.find_by_css("a.product-item img"))
    mars_hemisphere_image = []

    for i in range(num_of_thumb):
        browser.find_by_css("a.product-item img")[i].click()
        temp = {}
        temp["title"] = browser.find_by_css("h2.title")[0].text
        temp["img_url"] = browser.find_by_text("Sample")[0]["href"]
        mars_hemisphere_image.append(temp)
        browser.back()
        
    mars_hemisphere_image
    data = {"News_Title":mars_title,
    "news_paragraphs": mars_paragraphs,"featured_image":featured_image,"mars_tables":mars_html,"mars_hemis":mars_hemisphere_image}
    print(data)
    browser.quit()
    return data
