
CREATE TABLE categories
(
  category_id    INT      NOT NULL,
  category_name  TEXT     NOT NULL,
  category_color TEXT     NOT NULL,
  category_exp   LONGTEXT NULL    ,
  PRIMARY KEY (category_id)
);

CREATE TABLE languages
(
  lang_id   INT  NOT NULL,
  lang_name TEXT NOT NULL,
  PRIMARY KEY (lang_id)
);

CREATE TABLE users
(
  user_id  INT  NOT NULL,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  email    TEXT NOT NULL,
  PRIMARY KEY (user_id)
);

CREATE TABLE words
(
  word_id       INT      NOT NULL,
  user_id       INT      NULL     COMMENT 'creator',
  lang_id       INT      NULL    ,
  word_name     TEXT     NOT NULL,
  hebrew_trans  TEXT     NOT NULL,
  english_trans TEXT     NULL    ,
  image_path    TEXT     NULL    ,
  date_created  DATETIME NOT NULL,
  PRIMARY KEY (word_id)
);

CREATE TABLE words_categories
(
  word_id     INT NOT NULL,
  category_id INT NOT NULL
);

CREATE TABLE words_users
(
  word_id  INT  NOT NULL,
  user_id  INT  NOT NULL,
  is_known BOOL NOT NULL DEFAULT False
);

ALTER TABLE words
  ADD CONSTRAINT FK_users_TO_words
    FOREIGN KEY (user_id)
    REFERENCES users (user_id);

ALTER TABLE words
  ADD CONSTRAINT FK_languages_TO_words
    FOREIGN KEY (lang_id)
    REFERENCES languages (lang_id);

ALTER TABLE words_categories
  ADD CONSTRAINT FK_words_TO_words_categories
    FOREIGN KEY (word_id)
    REFERENCES words (word_id);

ALTER TABLE words_categories
  ADD CONSTRAINT FK_categories_TO_words_categories
    FOREIGN KEY (category_id)
    REFERENCES categories (category_id);

ALTER TABLE words_users
  ADD CONSTRAINT FK_words_TO_words_users
    FOREIGN KEY (word_id)
    REFERENCES words (word_id);

ALTER TABLE words_users
  ADD CONSTRAINT FK_users_TO_words_users
    FOREIGN KEY (user_id)
    REFERENCES users (user_id);
