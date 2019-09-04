import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}
base_url = 'https://krasnoyarsk.hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=python&area=1146&from=cluster_area&showClusters=false'


def hh_parse(headers, base_url):
    jobs = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content,'html.parser')
        divs = soup.find_all('div', attrs={'data-qa':'vacancy-serp__vacancy'})
        for div in divs:
            title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            employer = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            compensation = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
            if compensation == None:  # Если зарплата не указана
                compensation = 'None'
            else:
                compensation = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            jobs.append({
                'title': title,
                'href': href,
                'employer': employer,
                'compensation': compensation,
            })
            print(title, '\t', href, '\t', compensation)
    else:
        print('Error')
hh_parse(headers, base_url)