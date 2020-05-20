import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import re

#exports
SPOTIPY_CLIENT_ID = 'b20d381d35b14f969d322536d1bdb148'
SPOTIPY_CLIENT_SECRET = '7fbb1329aa3c494cbfe4f1828bebc034'
USERNAME = '22ppfuwrvchpbjx4aoznl7rcq'

def getArtist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None
    
def getArtistAlbums(artist):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    unique = set()  # skip duplicate albums
    for album in albums:
        name = album['name'].lower()
        if name in unique:
            albums.remove(album)
        unique.add(name)
    return albums
    
def getAlbumTracks(album):
    tracks = []
    results = sp.album_tracks(album['id'])
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def getBBArtists(df):
    fromDF = df['Artist']
    artists = set(fromDF)
    for artist in fromDF:
        artist = artist.replace('"', '')
        listOfArtists = re.split('Featuring |, |&', artist)
        artists.add(listOfArtists[0])
        #Uses all featured artists
        #for newArtist in listOfArtists:
        #    artists.add(newArtist)
    return artists



def main():
    billboard = pd.read_csv('BillBoardData.csv')
    artists = getBBArtists(billboard)
    tracksBB = billboard['Track']
    logisticDF = pd.DataFrame(list(zip(tracksBB, billboard['Artist'], [1.0]*len(tracksBB))), columns=['Tracks', 'Artist', 'Success'])
    completedData = pd.read_csv('SpotifyData3000.csv')
    completedArtists = set(completedData['Artist'])
    #included this because my internet crashed halfway through
    for artist in completedArtists:
        if artist in artists:
            artists.remove(artist)
    for i, artist in enumerate(artists):
        if i%100 == 0:
            print(i)
        if i % 1000 == 0:
            df = logisticDF.drop_duplicates(['Tracks'], keep='first').reset_index(drop=True)
            df.to_csv("SpotifyData" + str(i) + "Version2.csv", encoding="utf-8", index = False)
    
        artistID = getArtist(artist)
        if artistID is None:
            continue

        albums = getArtistAlbums(artistID)
        artistTracks = []
        for album in albums:
            artistTracks.extend([track['name'] for track in getAlbumTracks(album)])
        
        tracks = list(set(artistTracks))
        if len(tracks) == 0:
            continue
        for track in tracks:
            logisticDF = logisticDF.append({'Tracks':track, 'Artist':artist, 'Success':0.0}, ignore_index=True)        
    df = logisticDF.drop_duplicates(['Tracks'], keep='first').reset_index(drop=True)
    df.to_csv("SpotifyData.csv", encoding="utf-8", index = False)
if __name__ == '__main__':
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=None)
    main()