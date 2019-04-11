# music-taxonomy

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

2. Run the server locally from the root directory with:
   ```
   $ python server.py --port=8100
   ```

## Running Tests

Run tests with:
```
nosetests test
```
