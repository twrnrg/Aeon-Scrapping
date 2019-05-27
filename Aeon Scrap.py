import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

url="https://aeon.co/essays"
def extract_source(url):
     agent = {"User-Agent":"Mozilla/5.0"}
     source=requests.get(url, headers=agent).text
     return source

def extract_data(source):
    soup=BeautifulSoup(source, 'lxml')
    return soup

def reading_from_page():
    f= open("page_source.txt","r")
    contents=f.read()
    soup=BeautifulSoup(contents, 'lxml')

def content_printing(url):
    global cleantext
    print("Request Number : ", request_number )
    soup=extract_data(extract_source(url))
    html=soup.find('div', class_="article__body__content")
    content=[html.text.strip()]
    cleantext.append(content)
    if (request_number%5==0):
        print("Sleeping for 10 seconds")
        sleep(10)
    request_number+=1

soup=extract_data(extract_source(url))

title=[]
article_link=[]
title_links=soup.find_all('a', class_="article-card__title")
for link in title_links:
    title.append(link.text.strip())
    article_link.append(link.get('href'))    
# links=soup.find_all('a', class_="article-card__link")  
link_content=["https://aeon.co" + str(link) for link in article_link]

cleantext=[]
request_number=1
for url in link_content:
	content_printing(url)
    
#Importing in Dataframe
aeon_essay=pd.DataFrame()
aeon_essay['Link']=article_link
aeon_essay['Title']=title
aeon_essay['content']=cleantext
aeon_essay.head()

#Download csv file
with open('aeon_essay.csv', 'a+') as f:        
    aeon_essay.to_csv(f, header=['Link','Title','Content'])

def selenium_scrap(url):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (Linux; Android 8.1.0; SM-M205F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36")
    driver = webdriver.Firefox(profile)
    driver.get(url)
    sleep(5)
    driver.find_elements_by_xpath("///html/body/div[8]/div/div/span").click()
    driver.find_element_by_class_name("sc-gmeYpB gAiddk")
    html=driver.page_source
    driver.quit()
    soup=BeautifulSoup(html, 'lxml')
    aricles=soup.find_all('div', class_="article-card__contents")
    print (articels)    
    
# selenium_scrap("https://aeon.co/essays")