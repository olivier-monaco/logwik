CREATE TABLE IF NOT EXISTS `access_day` (
  `date` date NOT NULL,
  `hosting_id` smallint(6) unsigned NOT NULL,
  `domain_id` smallint(6) unsigned NOT NULL,
  `verb_id` tinyint(2) unsigned NOT NULL,
  `responder_id` tinyint(3) unsigned NOT NULL,
  `os_id` tinyint(3) unsigned NOT NULL,
  `os_version_id` tinyint(3) unsigned NOT NULL,
  `ua_id` smallint(5) unsigned NOT NULL,
  `ua_version_id` smallint(5) unsigned NOT NULL,
  `device_id` smallint(5) unsigned NOT NULL,
  `type` enum('','application','archive','audio','css','document','font','image','javascript','other','page','video') NOT NULL,
  `status` smallint(3) unsigned NOT NULL,
  `total_duration` decimal(20,6) unsigned NOT NULL,
  `delay_duration` decimal(20,6) unsigned NOT NULL,
  `responder_duration` decimal(20,6) unsigned NOT NULL,
  `number` int(11) unsigned NOT NULL,
  `bytes` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`hosting_id`,`date`,`domain_id`,`verb_id`,`responder_id`,`os_id`,`os_version_id`,`ua_id`,`ua_version_id`,`device_id`,`type`,`status`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=utf8 PAGE_CHECKSUM=1;

CREATE TABLE IF NOT EXISTS `access_hour` (
  `date` datetime NOT NULL,
  `hosting_id` smallint(6) unsigned NOT NULL,
  `domain_id` smallint(6) unsigned NOT NULL,
  `verb_id` tinyint(2) unsigned NOT NULL,
  `responder_id` tinyint(3) unsigned NOT NULL,
  `os_id` tinyint(3) unsigned NOT NULL,
  `os_version_id` tinyint(3) unsigned NOT NULL,
  `ua_id` smallint(5) unsigned NOT NULL,
  `ua_version_id` smallint(5) unsigned NOT NULL,
  `device_id` smallint(5) unsigned NOT NULL,
  `type` enum('','application','archive','audio','css','document','font','image','javascript','other','page','video') NOT NULL,
  `status` smallint(3) unsigned NOT NULL,
  `total_duration` decimal(20,6) unsigned NOT NULL,
  `delay_duration` decimal(20,6) unsigned NOT NULL,
  `responder_duration` decimal(20,6) unsigned NOT NULL,
  `number` int(11) unsigned NOT NULL,
  `bytes` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`hosting_id`,`date`,`domain_id`,`verb_id`,`responder_id`,`os_id`,`os_version_id`,`ua_id`,`ua_version_id`,`device_id`,`type`,`status`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=utf8 PAGE_CHECKSUM=1;

CREATE TABLE IF NOT EXISTS `access_minute` (
  `date` datetime NOT NULL,
  `hosting_id` smallint(6) unsigned NOT NULL,
  `domain_id` smallint(6) unsigned NOT NULL,
  `verb_id` tinyint(2) unsigned NOT NULL,
  `responder_id` tinyint(3) unsigned NOT NULL,
  `os_id` tinyint(3) unsigned NOT NULL,
  `os_version_id` tinyint(3) unsigned NOT NULL,
  `ua_id` smallint(5) unsigned NOT NULL,
  `ua_version_id` smallint(5) unsigned NOT NULL,
  `device_id` smallint(5) unsigned NOT NULL,
  `type` enum('','application','archive','audio','css','document','font','image','javascript','other','page','video') NOT NULL,
  `status` smallint(3) unsigned NOT NULL,
  `total_duration` decimal(20,6) unsigned NOT NULL,
  `delay_duration` decimal(20,6) unsigned NOT NULL,
  `responder_duration` decimal(20,6) unsigned NOT NULL,
  `number` int(11) unsigned NOT NULL,
  `bytes` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`hosting_id`,`date`,`domain_id`,`verb_id`,`responder_id`,`os_id`,`os_version_id`,`ua_id`,`ua_version_id`,`device_id`,`type`,`status`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=utf8 PAGE_CHECKSUM=1;

CREATE TABLE IF NOT EXISTS `access_quarter` (
  `date` datetime NOT NULL,
  `hosting_id` smallint(6) unsigned NOT NULL,
  `domain_id` smallint(6) unsigned NOT NULL,
  `verb_id` tinyint(2) unsigned NOT NULL,
  `responder_id` tinyint(3) unsigned NOT NULL,
  `os_id` tinyint(3) unsigned NOT NULL,
  `os_version_id` tinyint(3) unsigned NOT NULL,
  `ua_id` smallint(5) unsigned NOT NULL,
  `ua_version_id` smallint(5) unsigned NOT NULL,
  `device_id` smallint(5) unsigned NOT NULL,
  `type` enum('','application','archive','audio','css','document','font','image','javascript','other','page','video') NOT NULL,
  `status` smallint(3) unsigned NOT NULL,
  `total_duration` decimal(20,6) unsigned NOT NULL,
  `delay_duration` decimal(20,6) unsigned NOT NULL,
  `responder_duration` decimal(20,6) unsigned NOT NULL,
  `number` int(11) unsigned NOT NULL,
  `bytes` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`hosting_id`,`date`,`domain_id`,`verb_id`,`responder_id`,`os_id`,`os_version_id`,`ua_id`,`ua_version_id`,`device_id`,`type`,`status`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=utf8 PAGE_CHECKSUM=1;

CREATE TABLE IF NOT EXISTS `device` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(96) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `BUSINESS` (`name`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=utf8 PAGE_CHECKSUM=1 ROW_FORMAT=PAGE;

CREATE TABLE IF NOT EXISTS `domain` (
  `id` smallint(6) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `BUSINESS` (`name`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=utf8 PAGE_CHECKSUM=1 ROW_FORMAT=PAGE;


CREATE TABLE IF NOT EXISTS `hosting` (
  `id` smallint(6) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `BUSINESS` (`name`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=utf8 PAGE_CHECKSUM=1 ROW_FORMAT=PAGE;

CREATE TABLE IF NOT EXISTS `os` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `BUSINESS` (`name`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=utf8 PAGE_CHECKSUM=1;

CREATE TABLE IF NOT EXISTS `os_version` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `version` varchar(16) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `BUSINESS` (`version`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=utf8 PAGE_CHECKSUM=1 ROW_FORMAT=PAGE;

CREATE TABLE IF NOT EXISTS `responder` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `BUSINESS` (`name`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=utf8 PAGE_CHECKSUM=1 ROW_FORMAT=PAGE;

CREATE TABLE IF NOT EXISTS `type` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(96) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `BUSINESS` (`name`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=utf8 PAGE_CHECKSUM=1 ROW_FORMAT=PAGE;

CREATE TABLE IF NOT EXISTS `ua` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `BUSINESS` (`name`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=utf8 PAGE_CHECKSUM=1 ROW_FORMAT=PAGE;

CREATE TABLE IF NOT EXISTS `ua_version` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `version` varchar(16) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `BUSINESS` (`version`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=utf8 PAGE_CHECKSUM=1 ROW_FORMAT=PAGE;

CREATE TABLE IF NOT EXISTS `verb` (
  `id` tinyint(2) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(12) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `BUSINESS` (`name`) USING BTREE
) ENGINE=Aria DEFAULT CHARSET=utf8 PAGE_CHECKSUM=1;
