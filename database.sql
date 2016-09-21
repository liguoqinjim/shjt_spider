-- 上海公交app爬虫的数据库

create database shjt_spider;
use shjt_spider;

-- 系统版本表
create table t_version (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '无关逻辑的主见',
    version INT NOT NULL COMMENT '版本号',
    version_time INT NOT NULL COMMENT '版本号记录时间'
);

insert into t_version(version,version_time) values(67,1474115605);

select * from t_version order by id desc limit 1;

-- 线路版本表
CREATE TABLE t_line_version (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '无关逻辑的主见',
    line_type INT NOT NULL COMMENT 'px_line=1,pd_line=2',
    line_version INT NOT NULL COMMENT '线路版本',
    version_time INT NOT NULL COMMENT '版本记录时间'
);
insert into t_line_version(line_type,line_version,version_time) values(1,28,1474387371);
insert into t_line_version(line_type,line_version,version_time) values(1,29,1474387371);
insert into t_line_version(line_type,line_version,version_time) values(1,30,1474387371);

insert into t_line_version(line_type,line_version,version_time) values(2,18,1474387371);
insert into t_line_version(line_type,line_version,version_time) values(2,19,1474387371);

select * from t_line_version where line_type = 2 order by id desc limit 1;

-- 线路表
create table t_line(
	id int not null primary key auto_increment comment '无关逻辑的主键',
    line_version int not null comment '线路版本',
)

