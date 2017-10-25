DROP DATABASE if exists iplive;
CREATE DATABASE iplive;
use iplive;

DROP TABLE if exists records;
CREATE TABLE records(
    `server_id` int(11) NOT NULL AUTO_INCREMENT,
    `app_name` varchar(20) NOT NULL,
    `group_id` int(11) NOT NULL,
    `record_id` int(11) NOT NULL,
    `ip` varchar(15) NOT NULL,
    `last_status` int(11) comment "0 good, 1 connect error, 2 timeout, 1xx-5xx http code error",
    `res_time` int(11) comment "unit is ms",
    `gmt_create` datetime(6) DEFAULT NULL,
    `gmt_modify` datetime(6) DEFAULT NULL,
    `ext` int(1) NOT NULL default 0 comment "just extend field",
    PRIMARY KEY (`server_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS groups;
CREATE TABLE groups(
    `group_id` int(11) NOT NULL,
    `app_name` varchar(20) NOT NULL,

    `protocol` varchar(5) NOT NULL DEFAULT "http",
    `port` int(2) DEFAULT 80,
    `path` varchar(255) NOT NULL DEFAULT "/",
    `domain` varchar(100) NOT NULL,
    `cookies` varchar(255) NOT NULL,
    `http_code` varchar(11) NOT NULL DEFAULT "200" comment "a range of http code. example: 200,301,302",
    `timeout` int(1) NOT NULL DEFAULT 3,
    `retry_count` int(1) NOT NULL DEFAULT 2,
    `interval` int(11) NOT NULL,
    `level` int(2) DEFAULT 0,
    `node_ips` varchar(100) DEFAULT '',
    `gmt_create` datetime DEFAULT NULL,
    `gmt_modify` datetime DEFAULT NULL,
    `del_flag` int(11) DEFAULT 0,
    PRIMARY KEY(`group_id`, `app_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE if exists relation;
CREATE TABLE relation(
    `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `server_id` int(11) NOT NULL,
    `node_ip` varchar(64) NOT NULL,
    `sync` int(11) DEFAULT 0 comment "sync to client. 0 means no 1 means yes ",
    `sync_count` int(11) DEFAULT 0 comment "sync failed times",
    `reason` int(11) DEFAULT 0 comment "0 for not get. 1 for yes 2 for connecterror 3 for timeout 1xx-5xx",
    `gmt_create` datetime DEFAULT NULL,
    `gmt_modify` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE if exists nodes;
CREATE TABLE nodes(
    `node_id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `node_ip` varchar(64) UNIQUE NOT NULL,
    `status` int(11) DEFAULT 0 comment "0 for working, 1 for down",
    `gmt_create` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
