import requests
import json
import os
from pathlib import Path
from utils.FileIO import Config


BASE_URL = 'https://api.spotify.com/v1/playlists/'

def api_hook(client_id, client_secret):
    AUTH_URL = 'https://accounts.spotify.com/api/token'
        
    auth_response = requests.post(AUTH_URL, {'grant_type' : 'client_credentials',
                                             'client_id' : client_id,
                                             'client_secret' : client_secret,
                                             })
    access_token = auth_response.json()['access_token']
    headers = {
        'Authorization' : f'Bearer {access_token}'
    }
    
    return headers

def get_track_count(playlist_id):
    r = requests.get(f'{BASE_URL}{playlist_id}', headers=headers)
    r = r.json()
    return r['tracks']['total']
    

def get_playlist(headers, playlist_id):
    # This will be needed later
    total_count = get_track_count(playlist_id)\
    
    playlist_name = requests.get(
        f'{BASE_URL}{playlist_id}?market=US&fields=name', headers=headers
    ).json()['name'].replace(" ", "_")
    
    save_file = f'{playlist_name}_playlist.txt'
    
    print(f'Now looking at {playlist_name}.\n'\
          f'Total Number of tracks expected = {total_count}')
    
    if Path(save_file).is_file():
        print(f'Previous instance of file found, will now delete.')
        os.remove(save_file)
        print(f'{save_file} has been deleted.')

    with open(save_file, 'a+') as outfile:
        items = []
        json_list = {}
        
        # Spotify only allows you to grab 100 songs at a time so you have to split it up
        for i in range((total_count // 100) + 1):
            r = requests.get(
                f'{BASE_URL}{playlist_id}/tracks?market=US&fields=items(track(name), track(artists(name)), track(external_ids))&offset={i * 100}',
                headers=headers)
            r = r.json()
            items += list(r['items'])
        json_list['items'] = items
        
        json.dump(json_list, outfile, indent=4)     
        
    print(f'Completed the grab of {playlist_name} and saved to {save_file}')   


if __name__ == '__main__':
    configs = Config()
    APP_CONFIG = configs.open_yaml()
    
    # List your playlists you would like and it will go through them and download it
    playlist_id = ['']
    headers = api_hook(APP_CONFIG.get("CLIENT_ID"), APP_CONFIG.get("CLIENT_SECRET"))
    
    for id in playlist_id:
        get_playlist(headers, id)
    
    print('COMPLETED')