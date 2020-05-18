import billboard
import pandas as pd
from datetime import date, datetime, timedelta

START_DATE = date(1958, 8, 9)
END_DATE = date(2020, 5,10)

def generateDates(start, end):
    dates = []
    while start < end:
        dates.append(start)
        start += timedelta(days=7)
    
    return dates

def generateCSV(start, end):
    artists, tracks, dates = [], [], []
    iteration = 0
    for date in generateDates(start, end):
        day = str(date)
        chart = billboard.ChartData('hot-100', date=day, fetch=True, timeout=None)
        for song in chart:
            tracks.append(song.title)
            artists.append(song.artist)
        dates.extend([day for song in chart])
        if iteration % 5 == 0:
            print(day)
        iteration += 1

    merge = pd.DataFrame(list(zip(dates,artists, tracks)), columns=['Date', 'Artist', 'Track'])
    df = merge.drop_duplicates(['Track'], keep='first').reset_index(drop=True)
    df.to_csv("BillBoardData.csv", encoding="utf-8", index = False)

if __name__ == "__main__":
    generateCSV(START_DATE, END_DATE)