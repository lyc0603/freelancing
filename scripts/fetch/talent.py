"""
Script to fetch talent data from the API
"""

import json
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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
    """
    Function to login to the website
    """

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

# get the chrome driver from the path
service = Service(executable_path=f"{WEBDRIVER_PATH}/chromedriver")
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--window-size=1920,1080")
options.add_argument(f'user-agent={HEADERS["User-Agent"]}')
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

url = f"https://www.upwork.com/nx/search/talent/?category_uid=531770282580668418&subcategory_uid=531770282584862733" 
driver.get(url)

login(driver, USERNAME, PASSWORD)

driver.get(url)
talent_page = BeautifulSoup(driver.page_source, "html.parser")
Page_max_info = talent_page.find("div", {"aria-atomic": "true", "aria-live": "polite", "class": "sr-only"}).text
match = re.search(r'of (\d+)', Page_max_info)
max_page_number = int(match.group(1))

for page_num in tqdm(range(1, max_page_number + 1)):
    url = f"https://www.upwork.com/nx/search/talent/?category_uid=531770282580668418&subcategory_uid=531770282584862733&page={page_num}" 

    driver.get(url)
    talent_page = BeautifulSoup(driver.page_source, "html.parser")

    talent_id_set = set([_["href"].split("?")[0].split("~")[-1] for _ in talent_page.find_all("a", {"class" : "up-n-link profile-link"})])

    for talent_id in talent_id_set:

        talent_data = {}

        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(f"https://www.upwork.com/freelancers/api/v1/freelancer/profile/~{talent_id}/details?excludeAssignments=true")
        details = driver.page_source
        talent_details = json.loads(driver.find_element(By.TAG_NAME, 'pre').text)

        talent_data["details"] = talent_details

        talent_identity_uid = talent_details["profile"]["identity"]["uid"]
        specialized_profiles = talent_details["profile"]["specializedProfilesInfo"]

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        for occupation_info in specialized_profiles:
            occupationUID = occupation_info["occupationInfo"]["occupationUID"]
            prefLabel = occupation_info["occupationInfo"]["prefLabel"]

            talent_data[prefLabel] = []

            occp_page_num = 0
            total_items = 100

            while occp_page_num * 10 < total_items:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(f"https://www.upwork.com/freelancers/api/v3/freelancer/profile/{talent_identity_uid}/work-history/completed?specializedProfileUid={occupationUID}&page=1&limit=10&sortByAsNumber=1&filterPtc=0")
                details = driver.page_source
                job_completed = json.loads(driver.find_element(By.TAG_NAME, 'pre').text)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                talent_data[prefLabel].append(job_completed)
                occp_page_num += 1
                total_items = job_completed["totalItems"]
                print(talent_id, prefLabel, occp_page_num * 10, total_items)

        break