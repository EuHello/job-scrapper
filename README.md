## job-scrapper
Simple web scraper of job postings for efin******careers.sg. Only for SG location.  

## Pre-requisites 
- Python 3+

## Get started
To search for keyword 'engineer'

```bash
$ python3 scrape.py -t "engineer"
```

### Output:
1. List of Companies found, ranked by # of postings
2. List of mapped job postings found, ranked by # of postings
3. List of Jobs - Company, Job Title, Keyword 


### Further configs in scrape.py
1. max period to search. I.e. job postings up to x days ago
2. search size. default 100
3. default search term