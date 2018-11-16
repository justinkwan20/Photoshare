-- CREATE DATABASE photoshare;
-- USE photoshare;
-- DROP TABLE Pictures CASCADE;
-- DROP TABLE Users CASCADE;
-- DROP TABLE Album CASCADE;
-- DROP TABLE Tags CASCADE;

CREATE TABLE Users (
    user_id int4 AUTO_INCREMENT,
    email varchar(255) UNIQUE,
    password varchar(255),
    imgdata longblob,
    homeTown varchar(255),
    firstName varchar(255),
    lastName varchar(255),
    dob varchar(255),
    gender varchar(255),
    bio varchar(255),
    CONSTRAINT users_pk PRIMARY KEY (user_id)
);

CREATE TABLE Pictures (
  picture_id int4 AUTO_INCREMENT,
  user_id int4,
  imgdata longblob,
  caption VARCHAR(255),
  INDEX upid_idx (user_id),
  aid int4,
  CONSTRAINT pictures_pk PRIMARY KEY (picture_id),
  CONSTRAINT album_pix_fk FOREIGN KEY (aid) REFERENCES Album(aid)
);

CREATE Table Album (
  aid int4 AUTO_INCREMENT PRIMARY KEY,
  user_id int,
  nameAlbum VARCHAR(255),
  dateAlbum date,
  CONSTRAINT album_fk FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Tags (
  tag varchar(255),
  picture_id INT NOT NULL,
  CONSTRAINT tags_fk Foreign KEY (picture_id) REFERENCES Pictures(picture_id)
);

CREATE TABLE Comment (
  comment_id int4 PRIMARY KEY AUTO_INCREMENT,
  user_id int,
  texts VARCHAR(500),
  dateRN date,
  picture_id int4,
  CONSTRAINT comment_fk FOREIGN KEY (user_id) REFERENCES Users(user_id),
  CONSTRAINT comment_fk2 FOREIGN KEY (picture_id) REFERENCES Pictures(picture_id)
);

CREATE TABLE Friends (
  user_id int4,
  user_id_friend int4,
  CONSTRAINT friends_fk FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Likes
(
  picture_id int4,
  user_id int4,
  CONSTRAINT likes_fk FOREIGN KEY (picture_id) REFERENCES Pictures(picture_id),
  CONSTRAINT likes_user_id_fk FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

INSERT INTO Users (email, password) VALUES ('test@bu.edu', 'test');
INSERT INTO Users (email, password) VALUES ('test1@bu.edu', 'test');
INSERT INTO Users (email, password) VALUES ('Master@Master.com', 'password')
