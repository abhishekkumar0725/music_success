import spotipy
import spotipy.util as util
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

def getFeatureNames(sp, df):
    results = sp.search(q=df.iloc[0]['Tracks'])
    id = results['tracks']['items'][0]['id']
    features = sp.audio_features(id)
    return features[0].keys()

def getFeatures(df, sp, index):
    results = sp.search(q=df.iloc[index]['Tracks'])
    if not results['tracks']['items']:
        return 0
    id = results['tracks']['items'][0]['id']
    features = sp.audio_features(id)
    if not features[0]:
        return 0
    return features[0].values()

def main(sp, df):
    features = getFeatureNames(sp, df)
    columns = list(df.columns)
    columns.extend(features)
    featureDF = pd.DataFrame(columns=columns)
    badSongs = pd.DataFrame(columns=['Tracks'])
    for index in range(df.shape[0]):
        if index % 100 == 0:
            print(index)
        if index%100000 == 0:            
            badSongs.to_csv("features/badSongs"+str(index)+".csv", encoding="utf-8", index = False)
            featureDF.to_csv("features/SongFeatures"+str(index)+".csv", encoding="utf-8", index = False)
        row = list(df.iloc[index].values)
        features = getFeatures(df, sp, index)
        if features == 0:
            badSongs = badSongs.append({'Tracks':row[0]}, ignore_index=True)
            continue
        row.extend(getFeatures(df, sp, index))
        appendDict = {}
        for i, header in enumerate(columns):
            appendDict[header] = row[i]
        featureDF = featureDF.append(appendDict, ignore_index=True)
    featureDF.to_csv("SongFeatures.csv", encoding="utf-8", index = False)
    badSongs.to_csv("features/badSongs.csv", encoding="utf-8", index = False)
if __name__ == '__main__':
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=None)
    df = pd.read_csv('SpotifyData.csv')
    main(sp, df)