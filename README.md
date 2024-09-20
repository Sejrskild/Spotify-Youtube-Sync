![Logo for good fun](./assets/asset.png)

# Spotify to YouTube Music Sync

This program syncs a Spotify playlist with a YouTube Music playlist.

It removes all existing songs from a specified YouTube Music playlist and then adds songs from a Spotify playlist. The program runs as a scheduled task on my computer, with a delay between each song to reduce errors, as running it without pauses would sometimes result in failures.

## Requirements

- **Spotify Client Credentials**: To use the program, create a `.env` file with the following content:

  ```plaintext
  SPOTIFY_CLIENT_ID=your_spotify_client_id
  SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
  ```

  You can get these credentials from the [Spotify Developer Portal](https://developer.spotify.com/dashboard/).

- **YouTube OAuth Credentials**: You also need YouTube OAuth credentials, which you can set up by following the instructions here: [YouTube Music API OAuth Setup](https://ytmusicapi.readthedocs.io/en/stable/setup/oauth.html).

## How It Works

1. The program retrieves songs from a Spotify playlist (e.g., Top 50 Denmark) using Spotify's API.
2. It removes all songs from the specified YouTube Music playlist.
3. It searches for each song from Spotify on YouTube Music and adds it to the YouTube playlist.
4. A 2-second delay is added between each song addition to minimize errors.

## How to Run

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Ensure you have the `.env` file set up with your Spotify credentials and that you have YouTube Music OAuth credentials (`oauth.json`).

3. Run the script:
   ```bash
   python sync.py
   ```

## Disclaimer

This program is not entirely error-free, and issues may arise occasionally. For instance:

- Some songs might not be found on YouTube Music.
- The API requests may fail intermittently.

## Improvements and Troubleshooting

- The script is designed with logging enabled to track the sync process (`sync.log`).
- You can adjust the Spotify playlist or YouTube Music playlist IDs as needed in the code.

## License

Feel free to modify and use the code as needed. Any contributions are welcome!
