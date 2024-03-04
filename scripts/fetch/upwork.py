"""
Script to fetch data from Upwork
"""

import multiprocessing

from environ.constants import ACCT_DICT, CATEGORY_DICT
from environ.fetch.upwork import Upwork


def crawl_category_account(category_id, account_info):
    username = account_info["username"]
    password = account_info["password"]

    upwork_instance = Upwork(username, password)
    upwork_instance.fetch_talent(category_id)

if __name__ == "__main__":

    # Number of processes (you can adjust this based on your system and requirements)
    num_processes = len(ACCT_DICT)

    # Create a multiprocessing pool
    pool = multiprocessing.Pool(processes=num_processes)

    # Iterate over categories and corresponding accounts to crawl in parallel
    for (_, category_id), account_info in zip(CATEGORY_DICT.items(), ACCT_DICT):
        pool.apply_async(crawl_category_account, args=(category_id, account_info))

    # Close the pool and wait for the processes to finish
    pool.close()
    pool.join()