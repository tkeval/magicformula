import os 
import tweepy
import time, datetime  #Sys date and time
 
from re import sub
from decimal import Decimal
from google.oauth2.service_account import Credentials

#Selenium library to interact with browser 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import gspread
from google.oauth2.service_account import Credentials

'''
Magic Investing Rules: 
1) Buy 20 to 30 stocks based on the magic formula filter (for the sake of 
simplicity will buy all of these stocks at once rather than accumulating over several months)

2) Replace all stocks on 366th day with the new list from magicformula site
'''

os.chdir("C:\\Python\\magic")

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    './credentials.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)
sh = gc.open("magicformula")
url = 'https://www.magicformulainvesting.com/Account/LogOn'

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)

def scrapeSite():

    # find all td elements, write needed elements to file
    trs=driver.find_elements_by_xpath('//table[@class="divheight screeningdata"]/tbody/tr')

    names = []
    tikrs = []

    for tr in trs:
        td = tr.find_elements_by_xpath(".//td")

        company_name=td[0].get_attribute("innerHTML")
        company_tikr=td[1].get_attribute("innerHTML")
        

        names.append(company_name)
        tikrs.append(company_tikr)
        

    return names, tikrs

driver.get(url)

#username = driver.find_element_by_xpath(".//*[@id='Email ID']")
#password = driver.find_element_by_xpath(".//*[@id='Password']")
username=driver.find_element_by_name("Email")
password=driver.find_element_by_name("Password")

my_email = str("abc")
my_password = str("def")

time.sleep(1)

username.send_keys(my_email)
password.send_keys(my_password)

button = driver.find_element_by_name("login")
button.click()
print('logging in')
time.sleep(1)

#radio = driver.find_element_by_name('30')#xpath('//input[@value="false" and contains(@name,"30")]')
#radio.click()

button2=driver.find_element_by_name("stocks")
button2.click()
time.sleep(3)

names, tikrs = scrapeSite()

driver.quit()

date1 =sh.sheet1.acell('D2').value

def updateGSheet():

    company_names = names #sh.sheet1.col_values(1)
    tikr_names = tikrs #sh.sheet1.col_values(2)
    stock_price = sh.sheet1.col_values(3)


    tikr_names_filtered = tikr_names[1:]
    company_names_filtered = company_names[1:]
    stock_price_filtered = stock_price[1:]

    initial_funds = sh.sheet1.acell('N2').value
    print(initial_funds)
    funds = Decimal(sub(r'[^\d.]', '', initial_funds))
    print(funds)

    units = []
    fund_array = []
    fund_single_stock = int(funds)/len(stock_price_filtered)    
    print(fund_single_stock)

    #fund_array[1:30] = fund_single_stock
    #print(fund_array)

    units = [int(fund_single_stock)/ float(x) for x in stock_price_filtered]
    for i in range(0,len(units)):
        units[i] = int(units[i])

    #units = fund_array/stock_price_filtered
    print(units)

    for i in range(0,30):
        sh.sheet1.update_cell(i+2,6, units[i])

    #compare dates prior to updating anything in gsheet
    d1 = initial_funds = sh.sheet1.acell('N2').value

    for i in range(0,30): 
        sh.sheet1.update_cell(i+2,1,names[i])

    for i in range(0,30): 
        sh.sheet1.update_cell(i+2,2,tikrs[i])


def tweet(): 
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler("refer", "to")
    auth.set_access_token("tweepy", "docs")

    # Create API object
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    year = 2021
    performance = str('10%')
    api.update_status("{} Performance Was {}".format(year,performance))
    print("done")


def checkDate(): 

    date1 = sh.sheet1.acell('D2').value ## Excel Date
    date2 = datetime.date.today()       ##date from system
    date2 = str(date2)

    newdate1 = time.strptime(date1, "%m/%d/%Y")
    newdate2 = time.strptime(date2, "%Y-%m-%d")

    nd1 = datetime.datetime.strptime(date1, "%m/%d/%Y")
    nd2 = datetime.datetime.today()
    delta = (nd2-nd1).days

    
    if newdate2 > newdate1 and delta >= 0:
        print('Updating GoogleSheet with Names, Tikrs, Units')
        updateGSheet()
        #tweet()
    else:
        print("Today's Date is {} okay".format(date1))
        exit()

    
checkDate()
