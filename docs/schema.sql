DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL,
    display_name VARCHAR (255) NOT NULL,
    external_source VARCHAR (255) NOT NULL,
    external_id INTEGER NOT NULL,
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS artist_genres;

CREATE TABLE artist_genres (
    id SERIAL,
    artist_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(artist_id) REFERENCES artists(id),
    FOREIGN KEY(genre_id) REFERENCES genres(id)
);

DROP TABLE IF EXISTS artists;

CREATE TABLE artists (
    id SERIAL,
    spotify_id VARCHAR (255) NOT NULL,
    name VARCHAR (255) NOT NULL,
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS genres;

CREATE TABLE genres (
    id SERIAL,
    spotify_name VARCHAR (255) NOT NULL,
    display_name VARCHAR (255) NOT NULL,
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS subgenres;

CREATE TABLE subgenres (
    id SERIAL,
    spotify_name VARCHAR (255) NOT NULL,
    display_name VARCHAR (255) NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY(id)
    FOREIGN KEY(genre_id) REFERENCES genres(id)
);

DROP TABLE IF EXISTS spotify_authorization;

CREATE TABLE spotify_authorization (
    id SERIAL,
    user_id INTEGER NOT NULL,
    access_token VARCHAR (255) NOT NULL,
    refresh_token VARCHAR (255) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);


INSERT INTO genres (id,spotify_name,display_name) VALUES ('1','pop','Pop');
INSERT INTO genres (id,spotify_name,display_name) VALUES ('2','rock','Rock');
INSERT INTO genres (id,spotify_name,display_name) VALUES ('3','hip hop','Hip Hop');
INSERT INTO genres (id,spotify_name,display_name) VALUES ('4','jazz','Jazz');
INSERT INTO genres (id,spotify_name,display_name) VALUES ('5','folk','Folk');
INSERT INTO genres (id,spotify_name,display_name) VALUES ('6','country','Country');
INSERT INTO genres (id,spotify_name,display_name) VALUES ('7','edm','Electronic');
INSERT INTO genres (id,spotify_name,display_name) VALUES ('8','classical','Classical');
INSERT INTO genres (id,spotify_name,display_name) VALUES ('9','blues','Blues');
INSERT INTO genres (id,spotify_name,display_name) VALUES ('10','reggae','Reggae');
INSERT INTO genres (id,spotify_name,display_name) VALUES ('11','r&b','R&B');
