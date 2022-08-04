from bs4 import BeautifulSoup as bs
import requests
import csv 
import json


headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"}
jsondata = {'jobs':[]}


search = input("Enter the search term: ")
want = True if input("Do you want the qualification? <y/n>").lower() == 'y' else False



url= f"https://www.simplyhired.com/search?q={search}&l="
page = requests.get(url, headers=headers).text
soup = bs(page, 'lxml')

div_list = soup.find_all('div')
job_list = soup.find_all('div', class_='SerpJob-jobCard card')

csv_fields = {'job_name', 'company', 'location', 'qualification', 'salary'}
csv_filename = f'simplyhired_{search}.csv'

with open(csv_filename, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_fields)

    for jobs in job_list:
        name = jobs.find('a').text
        link = jobs.find('a').get('href')
        company = jobs.find('span', 'jobposting-company').text
        location = jobs.find('span', class_='JobPosting-labelWithIcon jobposting-location').text
        try:
            salary=jobs.find('div', class_="Jobposting-salary").text
        except:
            salary= 'not available'      
            
        qualifications = []
        link = f'https://www.simplyhired.com/job/{link}' 
        if want:
            html_jobdetail = requests.get(link, headers= headers).text
            details = bs(html_jobdetail, 'lxml') 
            for qualification in details.find_all('li', class_='viewjob-qualification'):
                qualifications.append(qualification.text)
        jsondata['jobs'].append({'Name':name, 'company':company, 'Location': location, 'Qualifications': qualifications, 'link': link})
        writer.writerow([name, company, location, qualifications, link])   
        
        print(name, '/',  company, '/', link)
with open(f'simplyhired_{search}.json', 'w') as jsonfile:
    json.dump(jsondata, jsonfile, indent=5)