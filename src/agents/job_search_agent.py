from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from typing import List

from ..models.job_listing import JobListing
from ..utils.selenium_utils import create_driver, safe_find_element


class JobSearchAgent:
    def __init__(self):
        self.driver, self.wait = create_driver()

    # ... rest of the agent implementation ...
