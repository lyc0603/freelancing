"""
Script to fetch data from Upwork
"""

from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import datetime
from environ.constants import PASSWORD, USERNAME, WEBDRIVER_PATH


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
    driver.find_element("name", "login[username]").send_keys(username)
    driver.find_element("id", "login_password_continue").click()
    # wait until the password input is visible
    implicit_wait(driver, "//input[@name='login[password]']")
    driver.find_element("name", "login[password]").send_keys(password)
    driver.find_element("id", "login_control_continue").click()
    # wait until botton is visible
    implicit_wait(driver, "//button[@class='air3-btn air3-btn-link mt-2x span-12 span-lg-7 p-md-4x justify-md-start mt-lg-4x px-lg-2x']")


url = "https://www.upwork.com/nx/search/talent/?category_uid=531770282580668418&subcategory_uid=531770282584862733" 

# get the chrome driver from the path
service = Service(executable_path=f"{WEBDRIVER_PATH}/chromedriver")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()


driver.get(url)
login(driver, USERNAME, PASSWORD)

freelancer_list = []

# bs4 to parse the page
driver.get(url)

# click each article to get the details

for artile in tqdm(driver.find_elements(By.TAG_NAME, "article")):
    # sleep until the article is load
    implicit_wait(driver, "//article")
    artile.click()
    implicit_wait(driver, "//div[@class='air3-tab-pane is-active']")
    soup = BeautifulSoup(driver.page_source, "html.parser")

    work_history_dict = {}


    # subsubcategory
    for subsubcategory in driver.find_elements(By.XPATH, "//a[@class='air3-list-nav-link' and @href='javascript:']")[0:-1]:
        implicit_wait(driver, "//a[@class='air3-list-nav-link' and @href='javascript:']")
        driver.execute_script("return arguments[0].scrollIntoView(true);", driver.find_element(By.XPATH, "//a[@class='air3-list-nav-link' and @href='javascript:']"))
        subsubcategory.click()

        subsubcategory_name = subsubcategory.text
        print(subsubcategory_name)
        work_history_dict[subsubcategory_name] = []

        # iterate through the work history pages
        while True:
            print("next page")
            soup = BeautifulSoup(driver.page_source, "html.parser")
            completed_jobs = soup.find('div', {'class': 'air3-tab-pane is-active'})
            work_history = completed_jobs.find_all('div', {'class': 'assignments-item', 'data-v-5ae367c1': True})
            for work in work_history:
                # click the completed jobs tab
                completed_jobs_xpath_expression = "//button[@data-ev-tab='jobs_completed_mobile']"
                if len(driver.find_elements(By.XPATH, completed_jobs_xpath_expression)) != 0:
                    driver.find_element(By.XPATH, completed_jobs_xpath_expression).click()

                job = work.find("a", {"class": "up-n-link cursor-pointer no-underline"}).text if work.find("a", {"class": "up-n-link cursor-pointer no-underline"}) else work.find("h5", {"data-v-5ae367c1":True, "role": "presentation"}).text
                period = work.find("div", {"data-v-1129f253":True, "class": "text-base-sm text-stone", "data-test":"assignment-date"}).text if work.find("div", {"data-v-1129f253":True, "class": "text-base-sm text-stone", "data-test":"assignment-date"}) else work.find("span", {"class": "text-stone text-base-sm"}).text
                price = work.find("div", {"class":"span-4"}).find("strong").text
                work_history_dict[subsubcategory_name].append(
                    {
                        "jobs": job,
                        "period": period,
                        "price": price
                    }
                )
                print(job, period, price)


            # click the next button for jobs and explicitly wait for the next page to load
            botton_xpath_expression = "//section[@class='air3-card-section work-history-section']//button[@class='air3-pagination-next-btn air3-btn air3-btn-circle air3-btn-tertiary']"
            if len(driver.find_elements(By.XPATH,botton_xpath_expression)) != 0:
                if len(driver.find_elements(By.XPATH, "//section[@class='air3-card-section work-history-section']//button[@class='air3-pagination-next-btn air3-btn air3-btn-circle air3-btn-tertiary is-disabled']")) == 0:
                    implicit_wait(driver, botton_xpath_expression)
                    driver.find_element(By.XPATH, botton_xpath_expression).click()
                    implicit_wait(driver, "//section[@class='air3-card-section work-history-section']")
                else:
                    break
            else:
                break

    freelancer_list.append(
        {
            "name": soup.find("h2", itemprop="name").text,
            "country-name": soup.find("span", itemprop="country-name").text,
            "locality": soup.find("span", itemprop="locality").text,
            "completed_jobs": work_history_dict
        }
    )
    driver.find_element(By.XPATH, "//div[@class='mr-3x flex-none air3-icon md']").click()


