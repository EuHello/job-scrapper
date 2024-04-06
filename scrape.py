import requests
from bs4 import BeautifulSoup
import pandas as pd


url_all = ("https://www.efinancialcareers.sg/jobs/in-singapore?"
           "location=Singapore&latitude=1.35208&longitude=103.81983&"
           "countryCode=SG&locationPrecision=Country&radius=40&radiusUnit=km&"
           # "pageSize=15&currencyCode=SGD&language=en&includeUnspecifiedSalary=true")
           "pageSize=100&currencyCode=SGD&language=en&includeUnspecifiedSalary=true")

url_analyst = ("https://www.efinancialcareers.sg/jobs/analyst/in-singapore?"
               "q=analyst&"
               "location=Singapore&latitude=1.35208&longitude=103.81983&"
               "countryCode=SG&locationPrecision=Country&radius=40&radiusUnit=km&"
               "pageSize=15&"
               "currencyCode=SGD&language=en&includeUnspecifiedSalary=true")

singapore_location = ('location=Singapore&latitude=1.35208&longitude=103.81983&'
                      'countryCode=SG&locationPrecision=Country&radius=40&radiusUnit=km')
my_page_size = 50
url_generic = (f'https://www.efinancialcareers.sg/jobs/in-singapore?'
               f'{singapore_location}&'
               f'pageSize={my_page_size}&currencyCode=SGD&language=en&includeUnspecifiedSalary=true')

page = requests.get(url_generic)
soup = BeautifulSoup(page.content, "html.parser")

find_divs = soup.body.find_all('div', class_='job-search-results')[0].find_all('div', class_='card-info')

job_titles = []
companies = []
for card in find_divs:
    if card is not None:
        job_titles.append(card.div.div.a.h3.string)
        companies.append(card.find_all('div', class_='company')[0].string)

df = pd.DataFrame(data={'job_title': job_titles, 'company': companies})
print(df)
