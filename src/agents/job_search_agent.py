from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List
from ..models.job_listing import JobListing


class JobSearchAgent:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def search_jobs(self, query: str, location: str) -> List[JobListing]:
        try:
            # Navigate to LinkedIn Jobs
            self.driver.get("https://www.linkedin.com/jobs")

            # Find and fill search fields
            keyword_input = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "[aria-label='Search by title, skill, or company']",
                    )
                )
            )
            keyword_input.send_keys(query)

            location_input = self.driver.find_element(
                By.CSS_SELECTOR, "[aria-label='City, state, or zip code']"
            )
            location_input.clear()
            location_input.send_keys(location)
            location_input.send_keys(Keys.RETURN)

            return self._extract_jobs()

        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def _extract_jobs(self) -> List[JobListing]:
        jobs = []
        # Wait for job cards to load
        job_cards = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".job-card-container")
            )
        )

        for card in job_cards[:10]:  # Limit to first 10 results
            try:
                title = card.find_element(By.CSS_SELECTOR, ".job-card-list__title").text
                company = card.find_element(
                    By.CSS_SELECTOR, ".job-card-container__company-name"
                ).text
                location = card.find_element(
                    By.CSS_SELECTOR, ".job-card-container__metadata-item"
                ).text
                link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                jobs.append(JobListing(title, company, location, link))
            except Exception as e:
                print(f"Error extracting job: {e}")
                continue

        return jobs

    def close(self):
        self.driver.quit()
