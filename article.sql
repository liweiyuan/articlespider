
#创建acrticle表
CREATE TABLE  article(
  title VARCHAR(200) not NULL,
  create_date datetime,
  url VARCHAR(300) not null,
  url_object_id VARCHAR(50) not NULL ,
  front_image_url VARCHAR(300),
  front_image_path varchar(200),
  comment_nums int(11) NOt null DEFAULT 0,
  fav_nums int(11) NOt null DEFAULT 0,
  praise_nums int(11) NOt null DEFAULT 0,
  tags VARCHAR(200),
  content text NOT NULL,
  PRIMARY key(url_object_id)
);

       Table: article
Create Table: CREATE TABLE `article` (
  `title` varchar(200) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  `url_object_id` varchar(50) NOT NULL,
  `front_image_url` varchar(300) DEFAULT NULL,
  `front_image_path` varchar(200) DEFAULT NULL,
  `comment_nums` int(11) NOT NULL DEFAULT '0',
  `fav_nums` int(11) NOT NULL DEFAULT '0',
  `praise_nums` int(11) NOT NULL DEFAULT '0',
  `tags` varchar(200) DEFAULT NULL,
  `content` text NOT NULL,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
