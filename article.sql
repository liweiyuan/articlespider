CREATE TABLE `article` (
  `title` varchar(200) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  `url_object_id` varchar(50) default '0',
  `front_image_url` varchar(300) DEFAULT NULL,
  `front_image_path` varchar(200) DEFAULT NULL,
  `comment_nums` int(11) NOT NULL DEFAULT '0',
  `fav_nums` int(11) NOT NULL DEFAULT '0',
  `praise_nums` int(11) NOT NULL DEFAULT '0',
  `tags` varchar(200) DEFAULT NULL,
  `content` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
