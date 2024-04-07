import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_colwidth', 80)
pd.set_option('display.width', 100)

sg_locale = ('location=Singapore&latitude=1.35208&longitude=103.81983&'
             'countryCode=SG&locationPrecision=Country&radius=40&radiusUnit=km')


def main():
    args = sys.argv[1:]

    if len(args) == 2 and args[0] == '-t':
        search_term = args[1]
        term_1 = f'/{search_term}'
        term_2 = f'q={search_term}&'
        print(search_term)
    else:
        search_term = 'analyst'
        term_1 = f'/{search_term}'
        term_2 = f'q={search_term}&'

    my_page_size = 50

    print(f'Searching for {search_term}, size={my_page_size}')

    url_generated = (f'https://www.efinancialcareers.sg/jobs{term_1}/in-singapore?{term_2}'
                     f'{sg_locale}&'
                     f'pageSize={my_page_size}&currencyCode=SGD&language=en&includeUnspecifiedSalary=true')

    page = requests.get(url_generated)
    soup = BeautifulSoup(page.content, "html.parser")

    find_divs = soup.body.find_all('div', class_='job-search-results')[0].find_all('div', class_='card-info')

    job_titles, companies, period = [], [], []

    for card in find_divs:
        if card is not None:
            companies.append(card.find_all('div', class_='company')[0].string)
            job_titles.append(card.div.div.a.h3.string)
            period.append(card.find_all('div', class_='meta-section')[0].span.string)

    df = pd.DataFrame(
        data={
            'company': companies,
            'job_title': job_titles,
            'period': period
        }
    )

    # df.sort_values(by=['company'])
    print("\nGrouping by companies")
    print(df.groupby('company').count())
    print("\n")
    print(df)

    # df.to_csv('data_scrapped.csv', sep=';', index=False)


if __name__ == "__main__":
    main()
