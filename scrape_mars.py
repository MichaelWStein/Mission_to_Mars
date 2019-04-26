def scrape():
    
    #Defining the Dictionary to be returned. All data will be stored / appended here.
    mars_data = {}

    #Importing the required functions:
    from bs4 import BeautifulSoup as bs
    import requests
    from splinter import Browser
    import pandas as pd


    #News from Mars
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    
    executable_path = {'executable_path' : 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find('div', class_='content_title')
    results_des = soup.find('div', class_= 'rollover_description_inner')

    results2 = results.a.text
    results2_des = results_des.text

    news_headline = results2
    news_text = results2_des
    mars_data = {"News": [news_headline, news_text]}


    #The latest picture from Mars
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    subtitle = soup.find_all('div', class_='article_teaser_body')
    pict_text = subtitle[1].text.strip()

    picture = []
    for link in soup.find_all('a', class_="fancybox", limit=2):
        picture.append(link.get("data-fancybox-href"))

    # The Mars image is the second 'fancybox' in the website.
    pict_url = ("https://www.jpl.nasa.gov" + picture[1])
    mars_data.update({"Picture": [pict_text, pict_url]})

    browser.quit()

    # Mars Weather

    # Getting the Weather report from twitter
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    w_results = soup.find('p', class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

    # Storing the weather as a string
    w_results2 = w_results.text
    w_results2 = w_results2[:-26]
    mars_weather = w_results2    
    mars_data.update({"Weather": mars_weather})


    #Adding Mars facts (as html-table)

    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)

    #Transform table into an html-table
    df = tables[0]
    df.columns=['Category', 'Data']
    df.set_index('Category', inplace=True)
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')

    mars_data.update({"Facts": html_table})


    #Adding Overview pictures
    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiapararelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
        {"title": "Valles Marineri Hemisphere", "img_url" : "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"} 
    ]
    mars_data.update({"Hemispheres": hemisphere_image_urls})

    return(mars_data)