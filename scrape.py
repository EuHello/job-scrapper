import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_colwidth', 80)
pd.set_option('display.width', 500)

sg_locale = ('location=Singapore&latitude=1.35208&longitude=103.81983&'
             'countryCode=SG&locationPrecision=Country&radius=40&radiusUnit=km')

my_page_size = 100
default_search = 'analyst'


def job_scope(title: str):
    title = title.lower()
    if 'quant' in title:
        return 'Quant'
    if 'business analyst' in title:
        return 'BA'
    if 'software' in title:
        return 'SWE/Dev'
    if 'scientist' in title:
        return 'Scientist'
    if 'developer' in title:
        return 'SWE/Dev'
    if 'risk' in title:
        return 'Risk'
    if 'support' in title:
        return 'Support'
    if 'fraud' in title:
        return 'Fraud'
    if 'project' in title:
        return 'Project'
    if 'analytic' in title:
        return 'Analytics'
    if 'product' in title:
        return 'Product'
    if 'operation' in title:
        return 'Ops'
    if 'cyber' in title:
        return 'Cyber'
    else:
        return ''


def period_inclusion(phrase: str):
    if phrase is not None:
        phrase_arr = phrase.strip().split(' ')
        if 'month' in phrase_arr[1]:
            return False
        if 'hour' in phrase_arr[1]:
            return True
        if 'day' in phrase_arr[1]:
            if int(phrase_arr[0]) < 7:
                return True
            else:
                return False
        print(f'Unknown value found = {phrase}')
        return True
    else:
        return True


def search_term_to_url(inputs: str):
    input_arr = inputs.split(' ')
    return '-'.join(input_arr), '+'.join(input_arr)


def main():
    args = sys.argv[1:]

    if len(args) == 2 and args[0] == '-t':
        search_inputs = args[1]
        t1, t2 = search_term_to_url(search_inputs)
        # print(f't1={t1}, t2={t2}')
        term_1 = f'/{t1}'
        term_2 = f'q={t2}&'
    else:
        print('Args not invalid. please specify with -t search term')
        print('Searching with default term')
        search_inputs = default_search
        term_1 = f'/{search_inputs}'
        term_2 = f'q={search_inputs}&'

    print(f'Searching for {search_inputs}, size={my_page_size}')
    url_generated = (f'https://www.efinancialcareers.sg/jobs{term_1}/in-singapore?{term_2}'
                     f'{sg_locale}&'
                     f'pageSize={my_page_size}&currencyCode=SGD&language=en&includeUnspecifiedSalary=true')

    page = requests.get(url_generated)
    soup = BeautifulSoup(page.content, "html.parser")

    find_divs = soup.body.find_all('div', class_='job-search-results')[0].find_all('div', class_='card-info')

    job_titles, companies, periods = [], [], []

    for card in find_divs:
        if card is not None:
            if len(card.find_all('div', class_='company')) > 0:
                companies.append(card.find_all('div', class_='company')[0].string.strip())
            else:
                companies.append("non-disclosed")
            job_titles.append(card.div.div.a.h3.string.strip())
            periods.append(card.find_all('div', class_='meta-section')[0].span.string)

    keywords = map(job_scope, job_titles)
    periods_to_include = map(period_inclusion, periods)

    df = pd.DataFrame(
        data={
            'Company': companies,
            'Job_Title': job_titles,
            'Keyword': keywords,
            'Period': periods,
            'Period_Include': periods_to_include
        }
    )

    df = df.loc[df['Period_Include'] == True]
    print(f'Found {df.shape[0]} postings out of {my_page_size} searched')

    df = df.sort_values(by=['Keyword'])
    print("\nTop Companies:")
    print(df['Company'].value_counts())
    print("\nTop Job Keywords:")
    print(df['Keyword'].value_counts())
    print("\n")
    print(f'Found {df.shape[0]} postings out of {my_page_size} searched')
    print(df)
    # df.to_csv('data_scrapped.csv', sep=';', index=False)


if __name__ == "__main__":
    main()
