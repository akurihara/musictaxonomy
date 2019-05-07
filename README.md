[![Build Status](https://travis-ci.org/akurihara/musictaxonomy.svg?branch=master)](https://travis-ci.org/akurihara/musictaxonomy)

# musictaxonomy

Music Taxonomy lets you express your musical taste in a way that's visual, organized, and delightful! See a live demo [here](http://musictaxonomy.herokuapp.com).

It was inspired an [infographic](https://turnerkarl.wordpress.com/2012/10/11/finished-music-infographic) created by artist Karl Turner.

## Set Up

1. Create a virtual environment and install dependencies.
   ```
   $ pyenv install 3.7.2
   $ pyenv virtualenv 3.7.2 music-taxonomy
   $ pyenv activate music-taxonomy
   (music-taxonomy) $ pip install --upgrade -r requirements.txt
   ```

2. Set up environmental variables
   ```
   touch .env
   ```

   Add the following variables to the .env file:
   - `SPOTIFY_CLIENT_ID` - The client ID of your Spotify application. This can be found at the Spotify [developer dashboard](https://developer.spotify.com/dashboard/applications).
   - `SPOTIFY_CLIENT_SECRET` - The client secret of your Spotify application.
   - `DATABASE_URL` - Database URL specifying which database to connect to locally (e.g. `sqlite:///database.db`).

3. Install SQLite, create a new database, and initialize tables.
  ```
  $ brew install sqlite3
  $ sqlite3 database.db
  $ source .env && scripts/initialize_database.py
  ```

4. Build the React frontend using:
   ```
   $ npm install
   $ npm run build
   ```

## Running Locally

Run the server locally from the root directory with:
```
$ python server.py --port=8080
```
Then, nagivate to `localhost:8080` in your browser.

## Running Tests

Create a test database if you haven't done so already:
```
$ sqlite3 test_database.db
$ source .env.test && scripts/initialize_database.py
```

Run tests with:
```
source .env.test && nosetests test
```
