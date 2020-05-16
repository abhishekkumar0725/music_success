import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from dateutil import parser

#TO FIX
#WILL RELY ON BILLBOARD LIBRARY UNTIL THEN

START_DATE = date(1958,8,9)
END_DATE = date(2020,5,10)

def generateUrls(start, end):
    link = 'https://www.billboard.com/charts/hot-100/'
    dates = []
    while start < end:
        dates.append(start)
        start += timedelta(days=7)
    
    urls = [link + str(date) for date in dates]
    return urls

def generateSoup(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    return BeautifulSoup(page, 'html.parser')

def generateData(soup):
    containers = soup.select('article[class*=chart]')
    songs, artists = [], []
    for container in containers:
        row = container.find('div', {'class': 'chart-row__title'})
        songs.append(row.h2.text)
        artists.append(row.a.text.strip())
    print(songs)
    return songs, artists

def cleanData(data):
    try:
        data = data.decode('utf-8')
    except:
        None
    return data

def generateCSV(start, end):
    urls = generateUrls(START_DATE, END_DATE)
    artists, tracks, dates = [], [], []
    iteration = 0
    for url in urls:
        soup = generateSoup(url)
        data = generateData(soup)
        artist = data[0]
        track = data[1]
        date = [parser.parse(url.split('/')[5])]*len(artist)
        
        artists.extend(artist)
        tracks.extend(track)
        dates.extend(date)

        iteration += 1
        if(iteration%100==0):
            print(iteration)
    print(artists)
    merge = pd.DataFrame(list(zip(dates,artists, tracks)), columns=['Date', 'Artist', 'Track'])
    df = merge.drop_duplicates(['Track'], keep='first').reset_index(drop=True)
    df = df.applymap(cleanData)
    df.to_csv("BillBoardData.csv", encoding="utf-8", index = False)

if __name__ == "__main__":
    generateCSV(START_DATE, END_DATE)