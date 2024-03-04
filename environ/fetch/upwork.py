"""
Class to fetch data from Upwork
"""

import re
import time

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import Any
from tqdm import tqdm

from environ.constants import HEADERS, PASSWORD, USERNAME, WEBDRIVER_PATH

class Upwork:
    """
    Class to fetch data from Upwork
    """

    def __init__(self, username: str, password: str, headers: dict, webdriver_path: str) -> None:
        self.username = username
        self.password = password
        self.webdriver_path = webdriver_path

    def implicit_wait(driver: Any, xpath:str) -> None:
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

    def login(driver: Any, username: str, password:str) -> None:
        """
        Function to login to the website
        """
        driver.find_element(By.XPATH, "//a[@class='up-n-link nav-item login-link d-none d-md-block px-6x']").click()
        print("Wait login")
        driver.find_element("name", "login[username]").send_keys(username)
        driver.find_element("id", "login_password_continue").click()
        # wait until the password input is visible
        self.implicit_wait(driver, "//input[@name='login[password]']")
        driver.find_element("name", "login[password]").send_keys(password)
        driver.find_element("id", "login_control_continue").click()
        print("Login clicked")
        # wait until botton is visible
        self.implicit_wait(driver, "//div[@id='user-top-navigation-container']")