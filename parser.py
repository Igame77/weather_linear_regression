import requests
from bs4 import BeautifulSoup

def Search(city, month, year):
    try:
        url = f'https://pogoda.mail.ru/prognoz/{city}/{month}-{year}/'
        html_source = requests.get(url)
        html_source = BeautifulSoup(html_source.text)

        html_el = html_source.find_all(class_ = 'day day_calendar')
    except: return None
    
    data = []

    for el in html_el:
        try:
            if 'На основе статистики' in el.find(class_ = 'day__alternative').text:
                break
        except: pass

        txt = el.find(class_ = 'day__temperature').text[0:3]
        txt = txt.replace('+','').replace('°','')
        data.append(int(txt))
    if data == []: return None
    
    return data

