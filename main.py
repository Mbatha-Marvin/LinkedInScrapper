import polars as pl
import pandas as pd 
# from pprint import pprint
from scrapper import job_fetching
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint
import re
from decouple import config

USER_NAME = config("USER_NAME")
USER_PASSWORD = config("USER_PASSWORD")

companies = ["Pitchly", "Tweed"]


browser = webdriver.Chrome(executable_path="./chromedriver_linux64/chromedriver")
sleep(1)
browser.maximize_window()
sleep(1)
browser.get("https://www.linkedin.com")
sleep(5)

username = browser.find_element(By.ID,"session_key")
username.send_keys(USER_NAME)
sleep(7)
password = browser.find_element(By.ID, "session_password")
password.send_keys(USER_PASSWORD)
sleep(7)
login_button = browser.find_element(By.CLASS_NAME, "sign-in-form__submit-btn--full-width")
login_button.click()
sleep(5)

company_id_list = []
# companies = ["google", "facebook", "apple"]

for company in companies:
    print(f"Scraping data for {company}")
    sleep(5)
    browser.get(f"https://www.linkedin.com/company/{company}/jobs")

    jobs_card = browser.find_element(By.CLASS_NAME, "job-card-square__link")
    link = jobs_card.get_attribute("href")

    begin_pattern = '&f_C='
    end_pattern = "&geoId="

    match_end = (re.search(end_pattern, link))
    match_begin=(re.search(begin_pattern, link))

    url_start_index = match_begin.end()
    url_end_index = match_end.start()

    company_id = link[url_start_index:url_end_index]
    company_id_list.append([company, company_id])
    # company_id_list.append({
    #     "company" : company,
    #     "company_id" : company_id
    # })
    
    sleep(20)

    print(company_id)
    

pprint(company_id_list, indent=4)
company_id_dataframe = pl.DataFrame(pd.DataFrame(company_id_list,columns=["Company", "Company_Id"]))
print(company_id_dataframe.head())
company_id_dataframe.write_excel(workbook="company_Ids.xlsx")

sleep(9000)

browser.close()

