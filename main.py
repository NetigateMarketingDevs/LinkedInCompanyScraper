import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import requests
import random
import json

def post_webhook(webhook_url, data_dict):
    response = requests.post(webhook_url, data=json.dumps(data_dict),headers={'Content-Type':'application/json'})
    return print(response)


#Creates a list of company names from a csv file and returns the list
def create_list_of_companies_from_csv(input_file, company_column):
    df = pd.read_csv(input_file)
    company_list = df[company_column].values.tolist()
    return company_list

#Sets the webdriver for the operation as the firefox webdriver
def create_webdriver():
    #driver_path = "/usr/local/bin/geckodriver"
    ##driver = webdriver.Firefox(executable_path=driver_path)
    #return driver
    driver_path = "/usr/local/bin/chromedriver"
    options = Options()
    options.headless = False
    options.add_argument("user-agent=whatever you want")
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
    return driver

#Login into linkedin with your credentials and the defined webdriver
def linkedin_login(email, password, driver):
    driver.get('https://www.linkedin.com/login') #Opens the LinkedIn Login page
    time.sleep(random_time())
    driver.find_element('id','username').send_keys(email) #Enters the provided e-mail adress
    driver.find_element('id','password').send_keys(password) #Enters the provided password
    time.sleep(3)
    driver.find_element('id','password').send_keys(Keys.RETURN) #Sends the login Data
    return

#Go to the about page of the company on linkedin by searching for it in the searchbar and clicking the first hero card on the resuluts page
def linkedin_go_to_company_page(driver, linkedin_company_name):
    time.sleep(random_time())
    driver.find_element('id', 'global-nav-typeahead').click() #Clicks on the search bar
    time.sleep(random_time())
    driver.find_element('class name','search-global-typeahead__input').send_keys(linkedin_company_name) #Puts the provided company name into the search bar
    time.sleep(random_time())
    driver.find_element('class name','search-global-typeahead__input').send_keys(Keys.RETURN) #Presses enter to sent the provided company name
    time.sleep(random_time())
    page = driver.page_source
    soup = bs(page.encode('utf-8'),features='lxml') #Creates a soup from the results page
    company_link = soup.find('div',{'class':'search-nec__hero-kcard-v2-actions'}).find('a')['href']  #Finds the link to the page from the hero card
    if '/company/' in company_link: #If it is a company link
        driver.get(str(company_link)+'about/') #it goes to the about page directly
    time.sleep(random_time())
    return

def random_time():
    time = random.randint(0, 8)
    return time
#Gets the soup of a page from the currently active page in the driver
def get_page_soup(driver):
    company_page = driver.page_source
    soup = bs(company_page.encode('utf-8'),features='lxml')
    soup.prettify()
    return soup

#Creates a an overview of the company attributes from the page soup
def create_company_overview_from_soup(soup,company_name):
    company_name = company_name
    #company_name = soup.find('h1').find('span').text #Finds the company name by finding the first headline on the company about page
    company_info= soup.find("dl", {"class": "overflow-hidden"}) #Creates a soup object from the information box on the about page
    heading_soup = company_info.find_all('dt', {'class':'mb1 text-heading-small'}) #Creates a soup from all the headings in the company info soup
    company_size = company_info.find('dd', {'class':'text-body-small t-black--light mb1'}).text.strip() #finds the company size in the company info soup as a string
    company_attributes = company_info.find_all('dd', {'class':'mb4 text-body-small t-black--light'}) #Creates a soup object from all the remaining company attributes
    company_attributes_list =  [] #Empty list of company attributes
    heading_list = [] #Empty list of headings
    for i in company_attributes: #for each elemtn in the company attributes soup
        attribute = i.text.strip() #Extracts the text
        company_attributes_list.append(attribute) #Appends the text to the list
    for x in heading_soup: #For each of the elements in the heading soup
        heading = x.text.strip() #extracts the text
        heading_list.append(heading) #appends it to the heading list
    return build_company_dict(company_name,company_size,company_attributes_list,heading_list) #Returns the build dict function with the found values

#Builds a dictionary based on the provided information
def build_company_dict(company_name,company_size,company_attributes_list,heading_list):
    entry_dict = {}
    entry_dict['Company Name'] = company_name
    entry_dict['Company Size'] = company_size
    entry_dict['Company Website'] = company_attributes_list[heading_list.index('Website')]
    entry_dict['Company Industry'] = company_attributes_list [heading_list.index('Industry')]
    return entry_dict

def create_single_company_dict(company_name, driver):
    linkedin_go_to_company_page(driver=driver, linkedin_company_name=company_name)
    soup = get_page_soup(driver)
    entry_dict = create_company_overview_from_soup(soup,company_name)
    return entry_dict

#Creates an output dataframe with all the company information that was found on linkedin for each of the companies in the input list
def create_df_from_csv_of_companies(csv_file, company_column,driver):
    company_list = create_list_of_companies_from_csv(csv_file, company_column )
    df = pd.DataFrame()
    for i in company_list:
        linkedin_go_to_company_page(driver=driver,linkedin_company_name=i)
        soup = get_page_soup(driver)
        entry_dict = create_company_overview_from_soup(soup)
        entry_df = pd.DataFrame(entry_dict,index=[0])
        df= pd.concat([df,entry_df])
    return df

#Make sure the input company name is carried over trough the whole script