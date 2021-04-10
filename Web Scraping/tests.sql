CREATE TABLE novelsdetails (
novelID INT AUTO_INCREMENT PRIMARY KEY,
title VARCHAR(200),
author VARCHAR(200),
chapters INT,
genre VARCHAR(100),
description VARCHAR(5000),
url VARCHAR(300),
image VARCHAR(300)
);


CREATE TABLE chapters (
  novelID INT,
  chapterno INT,
  chapter_title VARCHAR(200),
  chapter_link VARCHAR(300),
  FOREIGN KEY (novelID) REFERENCES novelsdetails(novelID)
);


ALTER TABLE chapters
  MODIFY chapter_title VARCHAR(300);
