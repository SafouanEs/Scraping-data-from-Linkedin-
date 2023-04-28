import csv
import requests
from bs4 import BeautifulSoup

# Links for each country to extract data analyst job listings
links = {"usa": {"onsite": "https://www.linkedin.com/jobs/search/?currentJobId=3351674810&f_WT=1&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=",
         "remote": "https://www.linkedin.com/jobs/search/?currentJobId=3205250146&f_WRA=true&f_WT=2&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=",
                 "hybrid": "https://www.linkedin.com/jobs/search/?currentJobId=3343518868&f_WRA=true&f_WT=3&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start="},
        "France":{"onsite": "https://www.linkedin.com/jobs/search/?currentJobId=3411194780&f_WT=1&geoId=105015875&keywords=data%20analyst&location=France&refresh=true",
        "remote":"https://www.linkedin.com/jobs/search/?currentJobId=3463860145&f_WT=2&geoId=105015875&keywords=data%20analyst&location=France&refresh=true",
        "hybrid":"https://www.linkedin.com/jobs/search/?currentJobId=3459099997&f_WT=3&geoId=105015875&keywords=data%20analyst&location=France&refresh=true"},
        "africa": {"onsite":"https://www.linkedin.com/jobs/search/?currentJobId=3463856886&f_WT=1&geoId=103537801&keywords=data%20analyst&location=Africa&refresh=true",
        "remote":"https://www.linkedin.com/jobs/search/?currentJobId=3448257178&f_WT=2&geoId=103537801&keywords=data%20analyst&location=Africa&refresh=true",
        "hybrid":"https://www.linkedin.com/jobs/search/?currentJobId=3396587660&f_WT=3&geoId=103537801&keywords=data%20analyst&location=Africa&refresh=true"}
        }
# Function to scrap job listings
def create_job_csv(country_links: dict, country: str):
    # create file or open file in write mode
    with open('Datasets'+country+'.csv', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file)
        # columns extracted
        writer.writerow(['title', 'company', 'description', 'onsite_remote',
                        'salary', 'location', 'criteria', 'posted_date', 'link'])

        # Moving from page to page
        def linkedin_scraper(webpage, page_number, onsite_remote):
            count = 0
            next_page = webpage + str(page_number)
            response = requests.get(str(next_page))
            soup = BeautifulSoup(response.content, 'html.parser')
            # print(response.content)
            jobs = soup.find_all(
                'div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
            for job in jobs:
                job_critere = []
                job_title = job.find(
                    'h3', class_='base-search-card__title').text.strip()
                job_company = job.find(
                    'h4', class_='base-search-card__subtitle').text.strip()
                job_location = job.find(
                    'span', class_='job-search-card__location').text.strip()
                job_datetime = job.find(
                    'time', class_='job-search-card__listdate')['datetime'] if job.find(
                    'time', class_='job-search-card__listdate') is not None else job.find(
                    'time', class_='job-search-card__listdate--new')['datetime']
                job_salary = job.find('span', class_='job-search-card__salary-info').text.strip(
                ) if job.find('span', class_='job-search-card__salary-info') is not None else "NaN"

                job_link = job.find('a', class_='base-card__full-link')['href']
                resp = requests.get(job_link)
                sp = BeautifulSoup(resp.content, 'html.parser')

                # Save requests as html pages to help view classes for scraping
                if count == 0 and country == 'africa':
                    with open('Visualisation_page/liste_of_jobs.html', mode='w', encoding="utf-8") as job_list:
                        job_list.write(str(response.content))
                        job_list.close()
                    with open('Visualisation_page/job.html', mode='w', encoding="utf-8") as job_detail:
                        job_detail.write(str(resp.content))
                        job_detail.close()
                count += 1

                job_desc = sp.find('div', class_='show-more-less-html__markup show-more-less-html__markup--clamp-after-5').text.strip(
                ) if sp.find('div', class_='show-more-less-html__markup show-more-less-html__markup--clamp-after-5') is not None else "Nan"

                critere = sp.find_all(
                    'li', class_='description__job-criteria-item')
                for criterion in critere:
                    feature = criterion.find(
                        'h3', class_='description__job-criteria-subheader').text.strip()
                    value = criterion.find(
                        'span', class_='description__job-criteria-text description__job-criteria-text--criteria').text.strip()
                    job_critere.append({feature: value})

                writer.writerow([job_title, job_company, job_desc, onsite_remote, job_salary,
                                job_location, job_critere, job_datetime, job_link])
                print(' Extraction des données')

            if page_number < 800:
                # Move to the next page
                page_number = page_number + 25
                linkedin_scraper(webpage, page_number, onsite_remote)

        for work_type in country_links:
            linkedin_scraper(country_links[work_type], 0, work_type)

for country in links:
    create_job_csv(links[country], country)
    
    
    
    
    