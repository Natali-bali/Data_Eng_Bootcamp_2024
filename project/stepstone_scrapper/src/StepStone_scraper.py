from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime
import re
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
print('works1 bla bla')

# Activate web driver and set options
options = webdriver.ChromeOptions()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('start-maximized')# Create max window
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")

driver = webdriver.Chrome('/my_code/src/chromedriver', options=options)

# Activate Postgres engine
HOST = 'stepstone_psql'
PORT = '5432'
USERNAME = 'postgres'
PASSWORD = '89218921'
DB = 'finalproject'

conn_string = f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}'
engine = create_engine(conn_string)

# Search words and jobs (as global var to dont loose data if we get disconection
search_words = ['data science', 'data analyst']
jobs = []

#Close cookies window
def close_cookies():
    try:
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.element_to_be_clickable((By.ID, 'ccmgt_explicit_accept'))).click()
    except:
        pass
    time.sleep(2)

# Fill input field and submit
def enter_search(search_word):
    element = driver.find_element_by_name("ke")
    element.send_keys(search_word)
    driver.find_element_by_name("ke").submit()
    time.sleep(5)

# Select jobs for last 24 hrs
def links_for_today():
    links_24 = driver.find_elements_by_class_name("FacetsListItemLinkStyled-pyfpom-0")
    link_24 = links_24[3].get_attribute("href")
    link_24 = link_24 + '&ob=date&action=sort_publish'
    return(link_24)

# Close pop up window
def close_popup():
    try:
        driver.find_element_by_class_name("sc-pspzH").click()
    except:
        pass

# Scrape job page and get info
def get_info(link):
    j={}
    driver.get(link)
    close_cookies()

    collected_successfully = False
    attempts=0
    while not collected_successfully:
        try:
            j['link'] = link
            try:
                j['job_title'] = driver.find_element_by_class_name("at-header-company-jobTitle").text
            except:
                j['job_title']=''
                pass
            try:
                j['company_name'] = driver.find_element_by_class_name("at-listing-nav-company-name-link").get_attribute("innerHTML")
            except:
                j['company_name']=''
                pass
            try:
                j['location'] = driver.find_element_by_class_name("location-LocationWithCommuteTimeBlock-trigger").get_attribute("innerHTML")
            except:
                j['location']=''
                pass
            try:
                j['intro'] = driver.find_element_by_class_name("at-section-text-introduction-content").get_attribute("innerHTML")
            except:
                j['intro']=''
                pass
            try:
                j['description'] = driver.find_element_by_class_name("at-section-text-description-content").get_attribute("innerHTML")
            except:
                j['description']=''
                pass
            try:
                j['profile'] = driver.find_element_by_class_name("at-section-text-profile-content").get_attribute("innerHTML")
            except:
                j['profile']=''
                pass
            try:
                j['offer'] = driver.find_element_by_class_name("at-section-text-weoffer-content").get_attribute("innerHTML")
            except:
                j['offer']=''
                pass
            try:
                j['contact'] = driver.find_element_by_class_name("at-section-text-contact-content").get_attribute("innerHTML")
            except:
                j['contact']=''
                pass
            collected_successfully = True
        except:
            print(f'could not collect job title {attempts} times')
            attempts+=1
            if attempts == 3:
                collected_successfully = True
            close_popup()
            pass
        time.sleep(15)
    return j

#Get 'next' link for pagination pages
def next_link():
    nb_link=[]
    next_button = driver.find_elements_by_class_name("PaginationArrowLink-imp866-0")
    for nb in next_button:
        nb_link.append(nb.get_attribute("href"))
    return nb_link[1]

#Get number of pagination buttons
def number_paginations():
    pag_buttons = driver.find_elements_by_class_name("PageLink-sc-1v4g7my-0")
    pl=[]
    for pb in pag_buttons:
        pl.append(pb.get_attribute("innerHTML"))
    return int(pl[-1])

# Get time posted on page
def times_posted():
    times_posted = []
    times = driver.find_elements_by_tag_name("time")
    for t in times:
        times_posted.append(t.get_attribute("datetime"))
    return times_posted

#Get all job buttons on page
def job_links():
    links = []
    job_buttons = driver.find_elements_by_class_name("kHKUnG")
    for jb in job_buttons:
        l = jb.get_attribute("href")
        links.append(l)
    return links

# extract text from tags
def clean_daily(jobs):
    col_list = ['intro', 'description', 'profile', 'offer', 'contact']
    df = pd.DataFrame([jobs]).fillna('')
    for col in col_list:
        df[col] = df[col].apply(lambda x: re.sub('\\n',' ', BeautifulSoup(x).get_text()))
    df['location'] = df['location'].apply(lambda x: BeautifulSoup(x).get_text())
    col = ['job_title', 'company_name', 'location', 'intro', 'description', 'profile', 'offer', 'contact']
    for column in col:
        df[column] = df[column].apply(lambda x: re.sub(('\'|\"|\'\''),' ', x))
    return df

# Loop over all jobs and get info
def get_jobs(url):
    global jobs
    print('works2')
    driver.get(url)
    time.sleep(2)

    num_pages = number_paginations()
    j=1

    # Loop over all pagination pages
    for np in range(1, num_pages):
        next_page_link = next_link()

        links=job_links()
        time_posted = times_posted()

        for link, t in zip(links, time_posted):
            time.sleep(10)
            try:
                res = get_info(link)
                res['link'] = link
                res['datetime'] = datetime.datetime.now()
                res['timeposted'] = t
                df = clean_daily(res)
                df.to_sql('jobs_daily_stepstone', engine, if_exists='append', index=True)
                j+=1
            except:
                pass
        time.sleep(10)
        driver.get(next_page_link)
    return jobs

for search_word in search_words:
    driver.get('https://www.stepstone.de/')
    close_cookies()
    enter_search(search_word)
    link = links_for_today()
    result = get_jobs(link)


# df = pd.DataFrame(jobs,columns=['link', 'datetime', 'job_title','company_name', 'location','intro','description','profile','offer','contact'])
# filename = '../output_daily/output' + str(datetime.datetime.now()) + '.csv'
# df.to_csv(filename)


