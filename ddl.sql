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


# 日线行情
create table day_tick
(
    ts_code    varchar(16),
    trade_date date,
    open       double,
    high       double,
    low        double,
    close      double,
    pre_close  double,
    `change`   double comment '涨跌额',
    pct_chg    double comment '涨跌幅，百分比',
    vol        double comment '手;每100股',
    amount     double comment '千元'

) engine = myisam;

create table day_tick_record
(
    trade_date  date primary key,
    origin_file varchar(32),
    checksum    varchar(32),
    last_update date
) engine = myisam;

# 每日指标
create table daily_basic
(
    ts_code         varchar(16),
    trade_date      date,
    close           double,
    turnover_rate   double comment '换手率%',
    turnover_rate_f double comment '自由流通股换手率',
    volume_ratio    double comment '量比',
    pe              double,
    pe_ttm          double,
    pb              double,
    ps              double,
    ps_ttm          double,
    dv_ratio        double comment '股息率',
    dv_ttm          double,
    total_share     double comment '总股本（万股）',
    float_share     double comment '流通股本（万股）',
    free_share      double comment '自由流通股本（万股）',
    total_mv        double comment '总市值（万元）',
    circ_mv         double comment '流通市值（万元）'
) engine = myisam;

create table daily_basic_record
(
    trade_date  date primary key,
    origin_file varchar(32),
    checksum    varchar(32),
    last_update date
) engine = myisam;

create table suspend
(
    ts_code        varchar(16),
    suspend_date   date,
    resume_date    date,
    ann_date       date,
    suspend_reason varchar(128),
    reason_type    varchar(128)
) engine = myisam;

create table suspend_record
(
    trade_date  date primary key,
    origin_file varchar(32),
    checksum    varchar(32),
    last_update date
) engine = myisam;

create table money_flow
(
    ts_code         varchar(16),
    trade_date      date,
    buy_sm_vol      int comment '小单买入量（手）',
    buy_sm_amount   double comment '小单买入金额（万元）',
    sell_sm_vol     int comment '小单卖出量（手）',
    sell_sm_amount  double comment '小单卖出金额（万元）',
    buy_md_vol      int comment '中单买入量（手）',
    buy_md_amount   double comment '中单买入金额（万元）',
    sell_md_vol     int comment '中单卖出量（手）',
    sell_md_amount  double comment '中单卖出金额（万元）',
    buy_lg_vol      int comment '大单买入量（手）',
    buy_lg_amount   double comment '大单买入金额（万元）',
    sell_lg_vol     int comment '大单卖出量（手）',
    sell_lg_amount  double comment '大单卖出金额（万元）',
    buy_elg_vol     int comment '特大单买入量（手）',
    buy_elg_amount  double comment '特大单买入金额（万元）',
    sell_elg_vol    int comment '特大单卖出量（手）',
    sell_elg_amount double comment '特大单卖出金额（万元）',
    net_mf_vol      int comment '净流入量（手）',
    net_mf_amount   double comment '净流入额（万元）'

) engine = myisam;

create table money_flow_record
(
    trade_date  date primary key,
    origin_file varchar(32),
    checksum    varchar(32),
    last_update date
) engine = myisam;


create table adj_factor
(
    ts_code    varchar(16),
    trade_date date,
    adj_factor double
) engine = myisam;

create table adj_factor_record
(
    trade_date  date primary key,
    origin_file varchar(32),
    checksum    varchar(32),
    last_update date
) engine = myisam;