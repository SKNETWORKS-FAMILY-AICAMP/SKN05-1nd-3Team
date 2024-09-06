drop database if exists project1;
create database project1;

use project1;

drop table if exists main;
drop table if exists sido;
drop table if exists yongdo;
drop table if exists chajong;
drop table if exists faqtbl;
drop table if exists carsalestbl;

create table main (
	year int,
    car_regi int,
    car_ic int,
    car_rat double
);

create table sido (
	year int, 
    car_regi int, 
    seoul int, 
    busan int,
    daegu int, 
    incheon int,
    gwangju int, 
    daejeon int, 
    ulsan int, 
    sejong int,
	gyeonggi int, 
	gangwon int, 
    chungbuk int,
    chungnam int, 
    jeonbuk int, 
    jeonnam int, 
    gyeongbuk int, 
    gyeongnam int,
    jeju int
);

create table yongdo (
	year int, 
    car_regi int, 
    official double, 
    private int,
    commercial int
);

create table chajong (
	year int, 
    car_regi int,
    ic_amount double,
    passenger int,
    van int, 
    truck int,
    special double
);

create table faqtbl (
	id	int not null,
    question varchar(2000) not null,
    answer	varchar(2000) not null
);

create table carsalestbl (
	year	int not null,
    car_regi	int not null,
    id	int
);

alter table main
	add constraint pk_main_year
		primary key main(year);
alter table sido
	add constraint fk_sido_year
		foreign key (year)
		references main(year);
alter table yongdo
	add constraint fk_yongdo_year
		foreign key (year)
        references main(year);
alter table chajong
	add constraint fk_chajong_year
		foreign key (year)
		references main(year);

-- 데이터 입력 후 실행
-- alter table faqtbl
-- 	add constraint fk_faqtbl_id
-- 		foreign key (id)
--         references companytbl(id);
--         
-- alter table carsalestbl
-- 	add constraint fk_carsalestbl_id
-- 		foreign key (id)
-- 		references companytbl(id);