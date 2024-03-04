"""This file contains the configuration settings for the market environment."""

from environ.settings import PROJECT_ROOT

# Paths
DATA_PATH = PROJECT_ROOT / "data"
FIGURE_PATH = PROJECT_ROOT / "figures"
PROCESSED_DATA_PATH = PROJECT_ROOT / "processed_data"
WEBDRIVER_PATH = PROJECT_ROOT / "webdriver"

# # Upwork password
# USERNAME = "ucesy34@ucl.ac.uk"
# PASSWORD = "Luoyichen110110!!"

# Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

# Categories
CATEGORY_DICT = {
    "Web, Mobile \u0026 Software Dev":"531770282580668418",
    "Data Science \u0026 Analytics":"531770282580668420",
    "Design \u0026 Creative":"531770282580668421",
    "Writing":"531770282580668423",
    "Sales \u0026 Marketing":"531770282580668422",
    "Admin Support":"531770282580668416",
    "Translation":"531770282584862720",
    "Engineering \u0026 Architecture":"531770282584862722",
    "Accounting \u0026 Consulting":"531770282584862721",
    "Customer Service":"531770282580668417",
    "IT \u0026 Networking":"531770282580668419",
    "Legal":"531770282584862723",
}

# Crawling accounts

ACCT_DICT = [
    {
        "username": "ucesy01@outlook.com",
        "password": "Luoyichen110110!!",
    },
    {
        "username": "ucesy02@outlook.com",
        "password": "Luoyichen110110!!",
    },
    {
        "username": "ucesy03@outlook.com",
        "password": "Luoyichen110110!!",
    },
    {
        "username": "ucesy04@proton.me",
        "password": "Luoyichen110110!!",
    },
    {
        "username": "ucesy05@proton.me",
        "password": "Luoyichen110110!!",
    },
    {
        "username": "ucesy06proton.me@proton.me",
        "password": "Luoyichen110110!!",
    },
    {
        "username": "ucesy07@proton.me",
        "password": "Luoyichen110110!!",
    },
    {
        "username": "ucesy08@proton.me",
        "password": "Luoyichen110110!!",
    },
    {
        "username": "ucesy09@proton.me",
        "password": "Luoyichen110110!!",
    },
    {
        "username": "ucesy10@proton.me",
        "password": "Luoyichen110110!!",
    },
    {
        "username": "ucesy11@proton.me",
        "password": "Luoyichen110110!!",
    },
    {
        "username": "869417783@qq.com",
        "password": "Luoyichen110110!!",
    },
]