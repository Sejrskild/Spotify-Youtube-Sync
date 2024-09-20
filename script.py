import requests
import time
import logging
import os
from dotenv import dotenv_values, find_dotenv
from ytmusicapi import YTMusic
env_file = find_dotenv('.env')
if env_file:
    env = dotenv_values(env_file)
    os.environ.update(env)
else:
    print("No .env file found")
    exit()



# Setup logging in file
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', filename='sync.log')

ytmusic = YTMusic('./oauth.json')

# Replace these values with your actual Spotify client credentials
SPOTIFY_CLIENT_ID = dotenv_values('.env')['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = dotenv_values('.env')['SPOTIFY_CLIENT_SECRET']

# Spotify Token
def get_spotify_token():
    url = "https://accounts.spotify.com/api/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


# Spotify misc.
# Change this to the playlist you want to sync from (Spotify)
top50_denmark_id = "37i9dQZEVXbL3J0k32lWnN"

# YouTube Music misc.
# Change this to the playlist you want to sync to (YouTube Music)
playlist_id = "PLmoB_LRT1Xea76KWjNt1oDr9BQ5yHWWdA"


def get_spotify_playlist_songs(playlist_id):
    token_data = get_spotify_token()
    access_token = token_data['access_token']

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()

    songs = [{
        'name': item['track']['name'],
        'artist': item['track']['artists'][0]['name']
    } for item in data['items']]

    return songs


def sync_spotify_to_youtube():
    logging.info("Sync has started")
    # Delete all songs from playlist before adding new ones
    playlist = ytmusic.get_playlist(playlist_id)
    # Log how many songs are being removed
    logging.info(f"Removing {len(playlist['tracks'])} songs from the playlist")
    count = 0
    for song in playlist['tracks']:
        # Object with videoId and setVideoId
        temp = {
            'videoId': song['videoId'],
            'setVideoId': song['setVideoId']
        }
        try:
            ytmusic.remove_playlist_items(playlist_id, [temp])
            print(f"Removed {song['title']} from the playlist")
            time.sleep(2)
            count += 1
        except Exception as e:
            print(f"Failed to remove {song['title']} from the playlist")
            logging.exception(f"Failed to remove {song['title']} from the playlist, error: {e}")
            print(e)

    logging.info(f"Removed {count} songs from the playlist")

    songs = get_spotify_playlist_songs(top50_denmark_id)
    logging.info(f"Adding {len(songs)} songs to the playlist")
    addedSongs = 0
    try:
        for song in songs:
            search_results = ytmusic.search(
                song['name'] + ' ' + song['artist'])
            song_id = search_results[0]['videoId']
            ytmusic.add_playlist_items(
                playlist_id, [song_id], duplicates='False')
            addedSongs += 1
            time.sleep(2)
    except Exception as e:
        print(f"Failed to add {song['name']} by {song['artist']} to the playlist")
        logging.exception(f"Failed to add {song['name']} by {song['artist']} to the playlist, error: {e}")
    logging.info(f"Added {addedSongs} songs to the playlist - Sync has ended")

sync_spotify_to_youtube()
