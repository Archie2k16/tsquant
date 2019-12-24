create database tsdata;

use tsdata;

create table sec_name_change
(
    ts_code       varchar(16),
    name          varchar(32),
    start_date    date,
    end_date      date,
    ann_date      date,
    change_reason varchar(255),
    primary key (ts_code, start_date)
) engine = myisam;

create table sec_name_change_record
(
    ts_code     varchar(16),
    origin_file varchar(32),
    checksum    varchar(32),
    last_update date,
    primary key (ts_code, checksum)
) engine = myisam;


create table day_tick
(
    ts_code    varchar(16),
    trade_date date,
    open       double,
    high       double,
    low        double,
    close      double,
    pre_close  double,
    `change`   double,
    pct_chg    double,
    vol        double,
    amount     double

) engine = myisam;

create table day_tick_record
(
    trade_date  date primary key,
    origin_file varchar(32),
    checksum    varchar(32),
    last_update date
)engine =myisam;