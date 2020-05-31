from requests_oauthlib import OAuth2Session

import sys
sys.path.append('c:\\Users\\José\\Skydrive\\Documents\\Programming\\Python\\CLI-Sonos')

from sonos.config import creds_store
from sonos.decorators import auto_refresh_token
from sonos.settings import SONOS_CLIENT_ID, SONOS_CONTROL_API_BASE_URL

import click

token = creds_store.get_access_token()
print (SONOS_CLIENT_ID)
print ('Token = ',token)
client = OAuth2Session(SONOS_CLIENT_ID, token=token)
print ("entête : ",client)
client.headers['Content-Type'] = 'application/json'


def _url(path):
    return SONOS_CONTROL_API_BASE_URL + path


def _playback_url(group_id, path=None):
    return _url(f'/groups/{group_id}/playback') + (path or '')


def _json(response):
    response.raise_for_status()
    return response.json()


@auto_refresh_token(client)
def get_households():
    response = client.get(_url('/households'))
    print ('response.url : ',response.url)
    print ('response.headers : ',response.headers)
    print ('response.text : ',response.text)
    return _json(response)


@auto_refresh_token(client)
def get_groups(household_id):
    print ('Get Group Before Request : ',client.params)
    response = client.get(_url(f'/households/{household_id}/groups'))
    print ('response.url : ',response.url)
    print ('response.headers : ',response.headers)
    print ('response.text : ',response.text)
    return _json(response)


@auto_refresh_token(client)
def status(group_id):
    response = client.get(_playback_url(group_id))
    return _json(response)


@auto_refresh_token(client)
def play(group_id):
    response = client.post(_playback_url(group_id, '/play'))
    print ('response.url : ',response.url)
    print ('response.headers : ',response.headers)
    print ('response.text : ',response.text)
    return _json(response)


@auto_refresh_token(client)
def pause(group_id):
    response = client.post(_playback_url(group_id, '/pause'))
    return _json(response)


@auto_refresh_token(client)
def skip_to_next_track(group_id):
    response = client.post(_playback_url(group_id, '/skipToNextTrack'))
    return _json(response)


@auto_refresh_token(client)
def skip_to_previous_track(group_id):
    response = client.post(_playback_url(group_id, '/skipToPreviousTrack'))
    return _json(response)


@auto_refresh_token(client)
def get_playlists(household_id):
    response = client.get(_url(f'/households/{household_id}/playlists'))
    return _json(response)


@auto_refresh_token(client)
def get_tracks(household_id, playlist_id):
    response = client.post(_url(f'/households/{household_id}/playlists/getPlaylist'), json={'playlistId': playlist_id})
    return _json(response)


@auto_refresh_token(client)
def load_playlist(group_id, playlist_id, play_on_completion=None):
    response = client.post(_url(f'/groups/{group_id}/playlists'),
                           json={'playlistId': playlist_id, 'playOnCompletion': play_on_completion})
    return _json(response)


@auto_refresh_token(client)
def get_group_volume(group_id):
    response = client.get(_url(f'/groups/{group_id}/groupVolume'))
    return _json(response)


@auto_refresh_token(client)
def set_group_volume(group_id, value):
    response = client.post(_url(f'/groups/{group_id}/groupVolume'), json={'volume': value})
    return _json(response)
