import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, \
    OnSiteOrRemoteFilters
from pprint import pprint
import pandas as pd

# Change root logger level (default is WARN)
logging.basicConfig(level=logging.INFO)



def job_fetching(Job_title: str, 
                    locations: str | list[str] = ['United States'], 
                    limit : int = 15, 
                    job_types : list[TypeFilters] = [TypeFilters.FULL_TIME, 
                                                        TypeFilters.INTERNSHIP,
                                                        TypeFilters.CONTRACT,
                                                        TypeFilters.PART_TIME,
                                                        TypeFilters.TEMPORARY,
                                                        TypeFilters.VOLUNTEER,
                                                        TypeFilters.OTHER
                                                    ],
                    on_site_or_remote : list[OnSiteOrRemoteFilters] = [OnSiteOrRemoteFilters.REMOTE, 
                                                                        OnSiteOrRemoteFilters.HYBRID, 
                                                                        OnSiteOrRemoteFilters.ON_SITE
                                                                    ],
                    experience : list[ExperienceLevelFilters] = [ExperienceLevelFilters.ENTRY_LEVEL,
                                                                    ExperienceLevelFilters.INTERNSHIP,
                                                                    ExperienceLevelFilters.MID_SENIOR,
                                                                    ExperienceLevelFilters.ASSOCIATE,
                                                                    ExperienceLevelFilters.DIRECTOR,
                                                                    ExperienceLevelFilters.EXECUTIVE
                                                                ],
                    time:TimeFilters = TimeFilters.MONTH,
                    relevance : RelevanceFilters = RelevanceFilters.RECENT,
                    skip_promoted_jobs: bool = False,
                    get_apply_link: bool = True,
                    # company_jobs_url : str = "https://www.linkedin.com/jobs/search/?currentJobId=3521159118&f_C=1441%2C16140%2C17876832%2C10440912%2C791962&geoId=92000000&originToLandingJobPostings=3521159118%2C3550985546%2C3550984843%2C3550982818%2C3404160280%2C3513158174%2C3514770286%2C3550983761%2C3550985544"
                ):
    
    queries = [
        Query(
            query=Job_title,
            options=QueryOptions(
                locations=locations,
                apply_link=get_apply_link,  # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page mus be navigated. Default to False.
                skip_promoted_jobs=skip_promoted_jobs,  # Skip promoted jobs. Default to False.
                limit=limit,
                filters=QueryFilters(
                    # company_jobs_url=company_jobs_url,  # Filter by companies.                
                    relevance=relevance,
                    time=time,
                    type=job_types,
                    on_site_or_remote=on_site_or_remote,
                    experience=experience
                )
            )
        ),
    ]
    
    querry_results = []

    # Fired once for each successfully processed job
    def on_data(data: EventData):
        print(data.date, data.location, data.title, data.company)
        output = {
            "title" : data.title,
            "company" : data.company,
            # "company_link" : data.company_link,
            "date" : data.date,
            # "link" : data.link,
            # "insights" : data.insights,
            # "description" : data.description,
            # "apply_link" : data.apply_link,
            # "job_id" : data.job_id,
            # "location" : data.location,
            # "place" : data.place
        }

        querry_results.append(output)


    # Fired once for each page (25 jobs)
    def on_metrics(metrics: EventMetrics):
        print('[ON_METRICS]', str(metrics))


    def on_error(error):
        
        print('[ON_ERROR]', error)


    def on_end():
        print('[ON_END]')

    scraper = LinkedinScraper(
        chrome_executable_path="./chromedriver_linux64/chromedriver",  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver) 
        chrome_options=None,  # Custom Chrome options here
        headless=True,  # Overrides headless mode only if chrome_options is None
        max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
        slow_mo=10,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
        page_load_timeout=40  # Page load timeout (in seconds)    
    )

    # Add event listeners
    scraper.on(Events.DATA, on_data)
    scraper.on(Events.ERROR, on_error)
    scraper.on(Events.END, on_end)

    scraper.run(queries)

    return querry_results

