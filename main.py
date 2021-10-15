import requests
import json


def main():
    CLIENT_ID = ''
    CLIENT_SECRET = ''

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    auth_response = requests.post(AUTH_URL, {'grant_type': 'client_credentials',
                                             'client_id': CLIENT_ID,
                                             'client_secret': CLIENT_SECRET,
                                             })

    auth_response_data = auth_response.json()

    access_token = auth_response_data['access_token']

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/playlists/'

    # Track ID from the URI
    playlist_id = ''

    # Gets the total number of tracks
    r = requests.get(f'{BASE_URL}{playlist_id}', headers=headers)
    r = r.json()
    total_count = r['tracks']['total']

    # Writes to a file
    with open('spotify_playlist_tippy.txt', 'a+') as outfile:
        items = []
        json_list = {}
        for i in range((total_count // 100) + 1):
            r = requests.get(
                f'{BASE_URL}{playlist_id}/tracks?market=US&fields=items(track(name), track(artists(name)), track(external_ids))&offset={i * 100}',
                headers=headers)
            r = r.json()
            items += list(r['items'])
        json_list['items'] = items
        
        json.dump(json_list, outfile, indent=4)


def read_json_file():
    with open('spotify_playlist.txt') as json_file:
        data = json.load(json_file)

        count = 0
        for p in data['items']:
            print(f"Track: {p['track']['name']}")
            for i in p['track']['artists']:
                print(f'Artists: {i["name"]}')
            count += 1

    print(count)


def create_itunes_playlist(playlist):
    # TODO
    pass


if __name__ == '__main__':
    main()
    # read_json_file()
