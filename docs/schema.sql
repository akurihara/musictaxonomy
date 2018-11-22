DROP TABLE IF EXISTS `artist_genres`;

CREATE TABLE `artist_genres` (
	`id`	INTEGER NOT NULL,
	`artist_id`	INTEGER NOT NULL,
	`genre_id`	INTEGER NOT NULL,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`artist_id`) REFERENCES `artists`(`id`),
	FOREIGN KEY(`genre_id`) REFERENCES `genres`(`id`)
);

DROP TABLE IF EXISTS `artists`;

CREATE TABLE `artists` (
	`id`	INTEGER NOT NULL,
	`spotify_id`	VARCHAR ( 255 ) NOT NULL,
	`name`	VARCHAR ( 255 ) NOT NULL,
	PRIMARY KEY(`id`)
);


DROP TABLE IF EXISTS `genres`;

CREATE TABLE `genres` (
	`id`	INTEGER NOT NULL,
	`spotify_name`	VARCHAR ( 255 ) NOT NULL,
	`display_name`	VARCHAR ( 255 ) NOT NULL,
	PRIMARY KEY(`id`)
);


DROP TABLE IF EXISTS `spotify_authorization`;

CREATE TABLE `spotify_authorization` (
	`id`	INTEGER NOT NULL,
	`access_token`	VARCHAR ( 255 ) NOT NULL,
	`refresh_token`	VARCHAR ( 255 ) NOT NULL,
	PRIMARY KEY(`id`)
);
