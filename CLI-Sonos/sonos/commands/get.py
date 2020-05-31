import click

import sys
sys.path.append('c:\\Users\\José\\Skydrive\\Documents\\Programming\\Python\\CLI-Sonos')

from sonos.api import control
from sonos.config import active_household_store
from sonos.decorators import output_option, format_result, login_required

# @auto_refresh_token(client)
def get_households():
    response = client.get(_url('/households'))
    return _json(response)


# @auto_refresh_token(client)
def get_groups(household_id):
    response = client.get(_url(f'/households/{household_id}/groups'))
    print ('response.url : ',response.url)
    return _json(response)

@click.group()
def get():
    pass


@get.command()
@output_option()
@login_required
@format_result(headers=['id'])
def households():
    result = control.get_households()
    return result['households']


@get.command()
@output_option()
@login_required
@format_result(headers=['coordinatorId', 'id', 'name', 'playbackState'])
def groups():
    household_id = active_household_store.get_active_household()
    result = control.get_groups(household_id)
    return result['groups']


@get.command()
@output_option()
@login_required
@format_result(headers=['id', 'name'])
def playlists():
    household_id = active_household_store.get_active_household()
    result = control.get_playlists(household_id)
    return result['playlists']


@get.command()
@click.option('--playlist-id', '-p', required=True)
@output_option()
@login_required
@format_result(headers=['name', 'album', 'artist'])
def tracks(playlist_id):
    household_id = active_household_store.get_active_household()
    result = control.get_tracks(household_id, playlist_id)
    return result['tracks']
