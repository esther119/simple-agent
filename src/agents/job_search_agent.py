from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict
from ..models.job_listing import JobListing
import time
import json
from bs4 import BeautifulSoup
import html
import traceback
from openai import OpenAI
import os
from dotenv import load_dotenv


class JobSearchAgent:
    def __init__(self):
        load_dotenv()
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def analyze_html_structure(self, html_content: str) -> str:
        """Use GPT to analyze HTML and generate parsing code"""
        prompt = f"""
        Analyze this HTML structure and generate Python code using BeautifulSoup to extract job listings.
        Each job listing should include: title, company, location, and URL.
        Return ONLY the Python code, no explanations.
        The code should be a function named 'parse_jobs_data' that takes html_content as parameter and returns a list of dictionaries.
        
        HTML sample:
        {html_content[:4000]}  # Send first 4000 chars as sample
        """

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Python expert. Generate only the code, no explanations or markdown.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )
        code = response.choices[0].message.content
        code = code.replace("python", "").replace("```", "").strip()
        return code

    def search_jobs(self, query: str = None) -> List[JobListing]:
        try:
            # Navigate to Work at a Startup jobs page
            self.driver.get("https://www.workatastartup.com/jobs")
            time.sleep(2)  # Wait for page to load

            # Get the page source
            html_content = self.driver.page_source

            # Get parsing code from GPT
            parsing_code = self.analyze_html_structure(html_content)
            print("parsing code", parsing_code)

            # Create a namespace and execute the parsing code
            namespace = {"BeautifulSoup": BeautifulSoup, "html_content": html_content}
            exec(parsing_code, namespace)

            # Call the generated parse_jobs_data function
            jobs = namespace["parse_jobs_data"](html_content)

            # Convert to JobListing objects
            job_listings = []
            for job in jobs:
                print("job", job)
                job_listings.append(
                    JobListing(
                        title=job["title"],
                        company=job["company"],
                        location=job["location"],
                        link=job["url"],
                    )
                )

            return job_listings

        except Exception as e:
            print(f"An error occurred during job search: {e}")
            traceback.print_exc()
            return []

    def _extract_jobs(self) -> List[JobListing]:
        jobs = []
        try:
            # Wait for job listings to load
            job_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-listing"))
            )

            for item in job_items[:10]:  # Limit to first 10 results
                try:
                    # Extract job details with updated selectors
                    title = item.find_element(
                        By.CSS_SELECTOR, ".job-listing-title"
                    ).text
                    company = item.find_element(
                        By.CSS_SELECTOR, ".job-listing-company"
                    ).text
                    location = item.find_element(
                        By.CSS_SELECTOR, ".job-listing-location"
                    ).text
                    link = item.find_element(
                        By.CSS_SELECTOR, "a.job-listing-link"
                    ).get_attribute("href")

                    jobs.append(JobListing(title, company, location, link))
                except Exception as e:
                    print(f"Error extracting job: {e}")
                    continue

        except Exception as e:
            print(f"Error finding job listings: {e}")

        return jobs

    def close(self):
        self.driver.quit()

    def parse_jobs_data(self, html_content: str) -> List[Dict]:
        soup = BeautifulSoup(html_content, "html.parser")
        jobs_list = soup.find("div", class_="jobs-list")

        if not jobs_list:
            print("No jobs div found")
            return []

        job_listings = []
        job_divs = jobs_list.find_all("div", recursive=False)

        for job_div in job_divs:
            try:
                # Find the main job details container
                details_div = job_div.find("div", class_="ml-5 my-auto grow")
                if not details_div:
                    continue

                # Get company info
                company_details = details_div.find("div", class_="company-details")
                company_name = company_details.find(
                    "span", class_="font-bold"
                ).text.strip()
                company_desc = company_details.find(
                    "span", class_="text-gray-600"
                ).text.strip()

                # Get job info
                job_link = details_div.find("a", class_="font-bold captialize")
                job_title = job_link.text.strip()
                job_url = f"https://www.ycombinator.com{job_link['href']}"

                # Get location and job type
                job_details = details_div.find("p", class_="job-details")
                job_type = job_details.find("span", class_="text-sm").text.strip()
                location = job_details.find_all("span", class_="text-sm")[
                    1
                ].text.strip()

                job_listings.append(
                    {
                        "title": job_title,
                        "company": company_name,
                        "company_description": company_desc,
                        "location": location,
                        "job_type": job_type,
                        "url": job_url,
                    }
                )

            except Exception as e:
                print(f"Error parsing job listing: {e}")
                continue

        return job_listings
