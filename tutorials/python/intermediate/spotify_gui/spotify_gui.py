import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import PySimpleGUI as sg
import os

def settings_window():
    layout = [[sg.Text('Spotify API Settings')],
              [sg.Text('Client ID'), sg.InputText(key='client_id')],
              [sg.Text('Client Secret'), sg.InputText(key='client_secret')],
              [sg.Button('OK'), sg.Button('Cancel')]]

    window = sg.Window('Settings', layout)

    event, values = window.read()
    window.close()

    if event in (None, 'Cancel'):
        return None, None

    return values['client_id'], values['client_secret']

def write_credentials(client_id, client_secret):
    with open('.cache/credentials', 'w') as f:
        f.write(f'{client_id}\n{client_secret}')

def get_spotify_client():
    if not os.path.exists('.cache'):
        os.makedirs('.cache')
        client_id = sg.popup_get_text('Enter your Spotify client ID:')
        client_secret = sg.popup_get_text('Enter your Spotify client secret:')
        write_credentials(client_id, client_secret)
    else:
        with open('.cache/credentials', 'r') as f:
            client_id = f.readline().strip()
            client_secret = f.readline().strip()
    spotipy_cred = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret)

    return spotipy.Spotify(client_credentials_manager=spotipy_cred)


def search_song(client):
    """
    Use the Spotify client to search for a song and retrieve the list of results
    """
    search_query = sg.popup_get_text(
        'Enter the name of the song you want to search:')
    results = client.search(search_query, type='track', limit=10)
    tracks = results['tracks']['items']
    return [
        f"{track['name']} by {track['artists'][0]['name']} - {track['id']}"
        for track in tracks
    ]


def display_song_features(client, track_id):
    """
    Use the Spotify client to retrieve the features of the selected song
    """
    features = client.audio_features(track_id)
    sg.popup_scrolled(
        f"Track ID: {track_id}\n"
        f"Acousticness: {features[0]['acousticness']}\n"
        f"Danceability: {features[0]['danceability']}\n"
        f"Energy: {features[0]['energy']}\n"
        f"Instrumentalness: {features[0]['instrumentalness']}\n"
        f"Liveness: {features[0]['liveness']}\n"
        f"Loudness: {features[0]['loudness']}\n"
        f"Speechiness: {features[0]['speechiness']}\n"
        f"Tempo: {features[0]['tempo']}\n"
        f"Valence: {features[0]['valence']}\n")


client = get_spotify_client()
song_list = []
layout = [
    [sg.Button('Search', key='search'), sg.Button('Settings', key='settings')],
    [sg.Listbox(song_list, key='song_list', size=(40, 10))],
    [sg.Button('OK'), sg.Button('Cancel')]]

window = sg.Window('Spotify GUI', layout)
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    elif event == 'settings':
        client_id, client_secret = settings_window()
        if client_id is not None:
            spotipy_cred = SpotifyClientCredentials(
                client_id=client_id, client_secret=client_secret)
            client = spotipy.Spotify(client_credentials_manager=spotipy_cred)
            write_credentials(client_id, client_secret)
    elif event == 'search':
        song_list = search_song(client)
        window['song_list'].update(song_list)
    elif event == 'OK':
        display_song_features(client, values['song_list'][0].split(' - ')[1])

window.close()