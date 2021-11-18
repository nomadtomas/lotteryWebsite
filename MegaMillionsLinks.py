from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re

chrome_options = Options()
chrome_options.add_argument("--headless")

def get_MegaMillions_links():
    """Creates a csv file of href links of Mega Millions winning numbers."""
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    url = 'https://www.megamillions.com/Winning-Numbers/Previous-Drawings.aspx'

    driver.get(url)
    driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div[4]/button').click()

    source = driver.page_source
    soup = bs(source,'html.parser')
    pg = soup.find_all("div","PagerControl")[0].button["name"]
    num = int(re.findall(r'\d+', pg)[0])
    start = 1
    # continue clicking load data until the end of list.
    while start != num:
        try:
            driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div[4]/button').click()
            source = driver.page_source
            soup = bs(source,'html.parser')
            pg = soup.find_all("div","PagerControl")[0].button["name"]
            num = int(re.findall(r'\d+', pg)[0])
            start += 1
        except:
            start += 1

    elems = driver.find_elements_by_xpath("//a[@href]")
    links = []
    for elem in elems:
        links.append(elem.get_attribute("href"))
    hrefs = pd.Series(links, name='links')
    ln = hrefs[hrefs.str.contains('Previous-Drawing-Page')]
    ln.to_csv('numberLinks.csv', index=False)
    driver.close()
    msg = 'CSV file created.'
    return print(msg)   

if __name__ == '__main__':
    get_MegaMillions_links()