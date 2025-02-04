from src.agents.job_search_agent import JobSearchAgent
import time
import os
from dotenv import load_dotenv


def main():
    # Load environment variables
    load_dotenv()

    # Get LinkedIn credentials from environment variables
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")

    if not email or not password:
        print("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables")
        return

    agent = JobSearchAgent()
    try:
        print("Logging in to LinkedIn...")
        if agent.login(email, password):
            print("Login successful!")

            print("Searching for jobs...")
            jobs = agent.search_jobs("Python Developer", "San Francisco")

            print(f"\nFound {len(jobs)} jobs:")
            for job in jobs:
                print("\n-------------------")
                print(f"Title: {job.title}")
                print(f"Company: {job.company}")
                print(f"Location: {job.location}")
                print(f"Link: {job.link}")
        else:
            print("Login failed!")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(2)
        agent.close()


if __name__ == "__main__":
    main()
