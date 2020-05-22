import spotipy
import spotipy.util as util
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

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
    print(results)
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    unique = set()  # skip duplicate albums
    print(albums)
    for album in albums:
        name = album['name'].lower()
        if name in unique:
            albums.remove(album)
        unique.add(name)
    return albums

def getAlbumTracks(album):
    tracks = []
    singles = sp.artist_albums(artist['id'], album_type='single')
    while singles['next']:
        singles = sp.next(singles)
        tracks.extend(singles['items'])
    results = sp.album_tracks(album['id'])
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

if __name__ == '__main__':
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=None)
    zeros = pd.read_csv('Zeros.csv')
    artists = zeros['Artist']
    for artist in artists:
        artistID = getArtist(artist)
        tracks = []
        for album in getArtistAlbums(artistID):
            tracks.extend(getAlbumTracks)
        print(artist + ': ' + str(len(tracks)))
