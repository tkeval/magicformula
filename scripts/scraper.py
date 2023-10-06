""" This script is a web-scraper for www.magicformulainvesting. """

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from config import magic_dict

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH = "chromedriver"
driver = webdriver.Chrome(PATH)


# Define the URL of the website
url = magic_dict['logOn']

# Replace with your actual username and password
username = magic_dict['email'],
password = magic_dict['password']

# Create a new instance of the Chrome web driver (you can use other drivers like Firefox or Edge)


# Open the login page
driver.get(url)

# Find the username and password input fields and the login button by their HTML attributes
username_field = driver.find_element_by_id("Email")
password_field = driver.find_element_by_id("Password")
login_button = driver.find_element_by_name("Login")

# Fill in the username and password fields
username_field.send_keys(username)
password_field.send_keys(password)

# Submit the login form by clicking the login button
login_button.click()

# Close the web browser when done
driver.quit()