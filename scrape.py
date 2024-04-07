import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.width', 700)

sg_locale = ('location=Singapore&latitude=1.35208&longitude=103.81983&'
             'countryCode=SG&locationPrecision=Country&radius=40&radiusUnit=km')

my_page_size = 100
default_search = 'analyst'
max_period_days = 7


def job_scope(title: str):
    title = title.lower()
    if 'quant' in title:
        return 'Quant'
    if 'business analyst' in title:
        return 'BA'
    if 'business intelligence' in title:
        return 'BI'
    if 'treasury' in title:
        return 'Treasury'
    if 'scientist' in title:
        return 'Scientist'
    if 'fraud' in title or 'crime' in title or 'laundering' in title or 'aml' in title:
        return 'Fraud/Crime'
    if 'risk' in title:
        return 'Risk'
    if 'compliance' in title:
        return 'Compliance'
    if 'support' in title:
        return 'Support'
    if 'investment' in title or 'portfolio' in title:
        return 'Investments'
    if 'developer' in title or 'devops' in title or 'software' in title or 'data engineer' in title:
        return 'SWE/Dev'
    if 'project' in title:
        return 'Project'
    if 'analytic' in title:
        return 'Analytics'
    if 'product' in title:
        return 'Product'
    if 'cyber' in title:
        return 'Cybersecurity'
    if 'intern' in title:
        return 'Intern'
    if 'operation' in title:
        return 'Ops'
    if 'fund' in title:
        return 'Funds'
    if ('actuarial' in title or 'actuary' in title or 'marketing' in title or 'procurement' in title or
            'relationship' in title or 'tax' in title or 'audit' in title or 'recruit' in title):
        return 'z-Others'
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
            if int(phrase_arr[0]) < max_period_days:
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
    total_postings = df.shape[0]
    print(f'Found {total_postings} postings in total')

    df = df.loc[df['Period_Include'] == True]

    df = df.sort_values(by=['Company'])
    df = df.sort_values(by=['Keyword'])
    print("\nTop Companies:")
    print(df['Company'].value_counts())
    print("\nTop Job Keywords:")
    print(df['Keyword'].value_counts())
    print("\n")
    print(f'After filtering up to {max_period_days} days ago, found {df.shape[0]} postings out of {total_postings}')
    print(df)


if __name__ == "__main__":
    main()
