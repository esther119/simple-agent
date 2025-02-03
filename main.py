from src.agents.job_search_agent import JobSearchAgent


def main():
    agent = JobSearchAgent()
    try:
        jobs = agent.search_jobs("Python Developer", "San Francisco")
        for job in jobs:
            print(f"\nTitle: {job.title}")
            print(f"Company: {job.company}")
            print(f"Location: {job.location}")
            print(f"Link: {job.link}")
    finally:
        agent.close()


if __name__ == "__main__":
    main()
