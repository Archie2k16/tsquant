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

create index ix_ts_code_day_tick on day_tick (ts_code);
create index ix_trade_date_day_tick on day_tick (trade_date);


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
    circ_mv         double comment '流通市值（万元）',
    primary key (ts_code, trade_date)
) engine = myisam;

create index ix_ts_code_daily_basic on daily_basic (ts_code);
create index ix_trade_date_daily_basic on daily_basic (trade_date);


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

alter table suspend add  primary key (ts_code,suspend_date);
create index ix_ts_code_suspend on suspend (ts_code);
create index ix_trade_date_suspend on suspend (suspend_date);


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

) engine = myisam comment '小单：5万以下 中单：5万～20万 大单：20万～100万 特大单：成交额>=100万';
create index ix_ts_code_money_flow on money_flow (ts_code);
create index ix_trade_date_money_flow on money_flow (trade_date);



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
    adj_factor double,
    primary key (ts_code, trade_date)
) engine = myisam;

create index ix_ts_code_adj_factor on adj_factor (ts_code);
create index ix_trade_date_adj_factor on adj_factor (trade_date);


create table adj_factor_record
(
    trade_date  date primary key,
    origin_file varchar(32),
    checksum    varchar(32),
    last_update date
) engine = myisam;

create table limit_list
(
    ts_code    varchar(16),
    trade_date date,
    name       varchar(32),
    close      double,
    pct_chg    double,
    amp        double comment '振幅',
    fc_ratio   double comment '封单金额/日成交金额',
    fl_ratio   double comment '封单手数/流通股本',
    fd_amount  double comment '封单金额',
    first_time time comment '首次涨停时间',
    last_time  time comment '最后封板时间',
    open_times int comment '打开次数',
    strth      double comment '涨跌停强度',
    `limit`    varchar(8) comment 'D跌停U涨停'
) engine = myisam;

create index ix_ts_code_limit_list on limit_list (ts_code);
create index ix_trade_date_limit_list on limit_list (trade_date);

create table limit_list_record
(
    trade_date  date primary key,
    origin_file varchar(32),
    checksum    varchar(32),
    last_update date
) engine = myisam;



create table concept
(
    code varchar(16),
    name varchar(64),
    src  varchar(32)
) engine = myisam;


drop table concept_detail;

create table concept_detail
(
    id           varchar(16),
    concept_name varchar(64),
    ts_code      varchar(16),
    name         varchar(64)
) engine = myisam;

create index ix_ts_code_concept_detail on concept_detail(ts_code);




