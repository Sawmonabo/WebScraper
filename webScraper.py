# -*- coding: utf-8 -*-
"""
Spyder Editor
Program that scrapes a website w/request library simulated against a
website that is going to search for job advertisements. It will bring all job
listings from specific website that their main skill requirement is python prog.
language.
Also wrtie a program that is going to pull the latest published job ads from
specific websites.
"""

from bs4 import BeautifulSoup
import requests
import time

print('Please enter skill you are not familair with')
unfamiliar_skill = input('>')
print(f'Filtering out {unfamiliar_skill}')

def find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')

    # Only takes jobs from first page
    # jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

    # Working with one job element - use 'job' instead of 'jobs'

    # Use only soup.find to get first tag - 'li' - then the class name.
    # Gets one job post at a time.
    # job = soup.find('li', class_ = 'clearfix job-bx wht-shd-bx')


    jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
    for index, job in enumerate(jobs):
        published_date = job.find('span', class_ = 'sim-posted').span.text
        if 'few' in published_date:
            # Search for specific element inside the job itself. Inside h3 tag, use class
            # name to search entire page for job name. Also add replace method to remove
            # white space.
            company_name = job.find('h3', class_ = 'joblist-comp-name').text.replace(' ', '')

            # Bring skill requirements other than python programming language. Since only
            # for people who are good with python language.
            skills = job.find('span', class_ = 'srp-skills').text.replace(' ', '')
            more_info = job.header.h2.a['href']
            if unfamiliar_skill not in skills:
                with open(f'posts/{index}.txt', 'w') as f:
                    f.write(f"Company Name: {company_name.strip()} \n")
                    f.write(f"Required Skills: {skills.strip()} \n")
                    f.write(f'More Info: {more_info} \n')
                print(f'File saved: {index}')


# To not overload the server we check every 10 minutes
if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
