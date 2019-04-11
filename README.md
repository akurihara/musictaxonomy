# musictaxonomy

Music Taxonomy lets you express your musical taste in a way that's visual, organized, and delightful!

It was inspired an [infographic](https://turnerkarl.wordpress.com/2012/10/11/finished-music-infographic) created by artist Karl Turner.

## Set Up

Create a virtual environment and install dependencies.
```
$ pyenv install 3.7.2
$ pyenv virtualenv 3.7.2 music-taxonomy 
$ pyenv activate music-taxonomy
(music-taxonomy) $ pip install --upgrade -r requirements.txt
```

## Running Locally

1. Build the React frontend using:
   ```
   $ npm run build
   ```

2. Set environmental variables

   - `SPOTIFY_CLIENT_ID` - The client ID of your Spotify application. This can be found at the Spotify [developer dashboard](https://developer.spotify.com/dashboard/applications).
   - `SPOTIFY_CLIENT_SECRET` - The client secret of your Spotify application.

2. Run the server locally from the root directory with:
   ```
   $ python server.py --port=8100
   ```

## Running Tests

Run tests with:
```
nosetests test
```
