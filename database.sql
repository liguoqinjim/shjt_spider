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
    line_type int not null comment '线路类型px_line=1,pd_line=2',
    line_name varchar(20) not null comment '线路名称',
    line_actual varchar(20) not null comment '线路actual',
    line_time int not null comment '线路记录的时间'
);

select count(*) from t_line where line_type = 2;

#通过线路名字查询
select * from t_line where line_name like '871%';

insert into t_line(line_version,line_type,line_name,line_actual,line_time) values(31,2,'5路','5路',147000001);


-- 线路基本信息表
create table t_line_info(
	id int not null primary key auto_increment comment '无关逻辑的主键',
    line_id int not null,
    line_name varchar(20) not null,
    start_stop varchar(32) not null,
    start_earlytime char(5) not null,
    start_latetime char(5) not null,
    end_stop varchar(32) not null,
    end_earlytime char(5) not null,
    end_latetime char(5) not null,
    line_version int not null,
    line_type int not null
);


-- 线路站点表
create table t_line_stop(
	id int not null primary key auto_increment comment '无关逻辑的主键',
    line_id int not null comment '线路id',
    stop_num int not null comment '第几站',
    stop_direction int not null comment '站点上下行',
    stop_name varchar(32) not null comment '站点名字',
    stop_id varchar(12) not null comment '站点id,用varchar来存，int会超出范围',
    line_version int not null,
    line_type int not null
);


-- 线路时刻
CREATE TABLE t_line_time (
    id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '无关逻辑的主键',
    line_id INT NOT NULL COMMENT '线路id',
    stop_id INT NOT NULL COMMENT '在哪一站得到的时间',
    stop_dircetion int not null comment '上下行'
    log_time INT NOT NULL COMMENT '得到信息的时间,这个时间点这个stop_id最多会有三条记录',
    car_info VARCHAR(16) NOT NULL COMMENT '车牌信息',
    stop_dis INT NOT NULL COMMENT '可能是还有多少站',
    distance INT NOT NULL COMMENT '可能是距离',
    away_time INT NOT NULL COMMENT '还有多久到达'
);

insert into t_line_time(line_id,stop_id