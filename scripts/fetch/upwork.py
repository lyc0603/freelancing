"""
Script to fetch data from Upwork
"""

import re
import time
import json

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

from environ.constants import HEADERS, PASSWORD, USERNAME, WEBDRIVER_PATH


def implicit_wait(driver, xpath:str) -> None:
    """
    Function to wait until the element is visible
    """
    def load_complete(driver, xpath:str) -> bool:
        """
        Function to check if the element is visible
        """
        if len(driver.find_elements(By.XPATH, xpath)) != 0:
            return True
        else:
            return False
        
    _ = WebDriverWait(driver, 60).until(lambda driver:load_complete(driver, xpath))

def login(driver, username: str, password:str) -> None:
    driver.find_element(By.XPATH, "//a[@class='up-n-link nav-item login-link d-none d-md-block px-6x']").click()
    print("Wait login")
    driver.find_element("name", "login[username]").send_keys(username)
    driver.find_element("id", "login_password_continue").click()
    # wait until the password input is visible
    implicit_wait(driver, "//input[@name='login[password]']")
    driver.find_element("name", "login[password]").send_keys(password)
    driver.find_element("id", "login_control_continue").click()
    print("Login clicked")
    # wait until botton is visible
    implicit_wait(driver, "//div[@id='user-top-navigation-container']")


url = "https://www.upwork.com/nx/search/talent/?category_uid=531770282580668418&subcategory_uid=531770282584862733" 

# get the chrome driver from the path
service = Service(executable_path=f"{WEBDRIVER_PATH}/chromedriver")
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--window-size=1920,1080")
options.add_argument(f'user-agent={HEADERS["User-Agent"]}')
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()


driver.get(url)
# driver.get_screenshot_as_file("screenshot.png")
login(driver, USERNAME, PASSWORD)

freelancer_list = []

# bs4 to parse the page
driver.get(url)
talent_list = BeautifulSoup(driver.page_source, "html.parser")


# click each article to get the details
for talent in tqdm(talent_list.find_all('a', {"class" : "up-n-link profile-link"})):

    talent_href = "https://www.upwork.com" + talent["href"]
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(talent_href)
    implicit_wait(driver, "//div[@class='air3-tab-pane is-active']")
    soup = BeautifulSoup(driver.page_source, "html.parser")

    work_history_list = []

    # subsubcategory
    for subsubcategory in driver.find_elements(By.XPATH, "//a[@class='air3-list-nav-link' and @href='javascript:']")[0:-1]:
        # driver.execute_script("return arguments[0].scrollIntoView(true);", driver.find_element(By.XPATH, "//h2[@itemprop='name']"))
        while True:
            try:
                subsubcategory.click()
                break
            except:
                time.sleep(1)
                pass

        subsubcategory_name = subsubcategory.text

        # iterate through the work history pages
        while True:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            completed_jobs = soup.find('div', {'class': 'air3-tab-pane is-active'})
            work_history = completed_jobs.find_all('div', {'class': 'assignments-item', 'data-v-5ae367c1': True})


            id = re.search(r'~([^/]+)', driver.current_url).group(1)
            try:
                name = soup.find("h2", itemprop="name").text
            except:
                name = np.nan

            try:
                country_name = soup.find("span", itemprop="country-name").text
            except:
                country_name = np.nan

            try:
                locality = soup.find("span", itemprop="locality").text
            except:
                locality = np.nan



            for work in work_history:
                # click the completed jobs tab
                completed_jobs_xpath_expression = "//button[@data-ev-tab='jobs_completed_mobile']"
                if len(driver.find_elements(By.XPATH, completed_jobs_xpath_expression)) != 0:
                    # check if the completed jobs tab is clickable
                    _ = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, completed_jobs_xpath_expression)))
                    driver.find_element(By.XPATH, completed_jobs_xpath_expression).click()

                job = work.find("a", {"class": "up-n-link cursor-pointer no-underline"}).text if work.find("a", {"class": "up-n-link cursor-pointer no-underline"}) else work.find("h5", {"data-v-5ae367c1":True, "role": "presentation"}).text
                period = work.find("div", {"data-v-1129f253":True, "class": "text-base-sm text-stone", "data-test":"assignment-date"}).text if work.find("div", {"data-v-1129f253":True, "class": "text-base-sm text-stone", "data-test":"assignment-date"}) else work.find("span", {"class": "text-stone text-base-sm"}).text
                try:
                    price = work.find("div", {"class":"span-4"}).find("strong").text if ("$" in work.find("div", {"class":"span-4"}).find("strong").text) else np.nan
                except:
                    price = np.nan

                work_history_list.append(
                    {
                        "id": id,
                        "name": name,
                        "country": country_name,
                        "locality": locality,
                        "job_category": subsubcategory_name,
                        "jobs": job,
                        "period": period,
                        "price": price
                    }
                )


            # click the next button for jobs and explicitly wait for the next page to load
            botton_xpath_expression = "//section[@class='air3-card-section work-history-section']//button[@class='air3-pagination-next-btn air3-btn air3-btn-circle air3-btn-tertiary']"
            if len(driver.find_elements(By.XPATH,botton_xpath_expression)) != 0:
                if len(driver.find_elements(By.XPATH, "//section[@class='air3-card-section work-history-section']//button[@class='air3-pagination-next-btn air3-btn air3-btn-circle air3-btn-tertiary is-disabled']")) == 0:

                    next_button = driver.find_element(By.XPATH, botton_xpath_expression)
                    # driver.execute_script("return arguments[0].scrollIntoView(true);",  driver.find_elements(By.XPATH,"//div[contains(@class, 'assignments-item') and @data-v-5ae367c1]")[-1])
                    while True:
                        try:
                            next_button.click()
                            break
                        except:
                            time.sleep(1)
                            pass
                    implicit_wait(driver, "//section[@class='air3-card-section work-history-section']")
                else:
                    break
            else:
                break
    print(
        pd.DataFrame(work_history_list)
    )
    driver.switch_to.window(driver.window_handles[0])
    driver.close()



