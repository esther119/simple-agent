from src.agents.job_search_agent import JobSearchAgent
import time


def main():
    agent = JobSearchAgent()
    try:
        print("Searching for jobs on Y Combinator's job board...")
        jobs = agent.search_jobs()

        print(f"\nFound {len(jobs)} jobs:")
        for job in jobs:
            print("\n-------------------")
            print(f"Title: {job.title}")
            print(f"Company: {job.company}")
            print(f"Location: {job.location}")
            print(f"Link: {job.link}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(2)
        agent.close()


if __name__ == "__main__":
    main()
