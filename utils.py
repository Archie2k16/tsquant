import os, re, datetime, pickle, time, termcolor, hashlib
import tushare as ts
import pandas as pd
from conf import ts_token, start_date, db_conf
from sqlalchemy import create_engine

engine = create_engine(db_conf)
ts.set_token(ts_token)
pro = ts.pro_api()


def logprop(color, title):
    '''
    带颜色格式输出装饰器
    :param color: 颜色
    :param title: 标志
    :return:
    '''

    def wrapper(func):
        def wrapped(msg):
            termcolor.cprint(f'{title}:{msg}', color=color)

        return wrapped

    return wrapper


class log(object):
    '''
    格式输出类
    分为四个级别：INFO、MSG、WARNING和ERROR
    '''

    @logprop('green', 'INFO')
    @staticmethod
    def info(msg):
        pass

    @logprop('white', 'MSG')
    @staticmethod
    def msg(msg):
        pass

    @logprop('yellow', 'WARNING')
    @staticmethod
    def warn(msg):
        pass

    @logprop('red', 'ERROR')
    @staticmethod
    def err(msg):
        pass


def end_date():
    '''
    用来获取最后的交易日期
    如果当前时间超过下午3点，获取当前日期
    反之获取前一天
    :return:
    'yyyymmdd'格式的字符串日期
    '''
    now = datetime.datetime.now()
    hour = now.hour
    if hour >= 15:
        year = now.year
        month = now.month
        day = now.day
    else:
        now = now - datetime.timedelta(days=1)
        year = now.year
        month = now.month
        day = now.day
    return f'{year}{month}{day}'


end_date = end_date()


def trade_cal():
    '''
    获取交易日历
    如果已获取最新的交易日历，则直接读取数据，否则从线上获取并储存
    :return:
    '''
    pickle_path = 'raw/common'
    file_name = 'trade_cal.pkl'
    file_path = os.path.join(pickle_path, file_name)
    # 判断路径是否存在
    if os.path.exists(pickle_path):
        # 判断文件是否存在
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                dstore = pickle.load(f)
                trade_date = dstore['trade_date']
                # 判断是否最近更新
                if dstore['last_update'] == end_date:
                    return trade_date
    else:
        os.makedirs(pickle_path)
    online_date = pro.trade_cal(start_date=start_date, end_date=end_date)
    td = online_date[online_date['is_open'] == 1]
    trade_date = set(td['cal_date'])
    with open(os.path.join(pickle_path, file_name), 'wb') as f:
        dstore = {'last_update': end_date,
                  'trade_date': trade_date}
        pickle.dump(dstore, f)
    return trade_date


def stock_list():
    '''
    获取股票列表
    :return:
    '''
    pickle_path = 'raw/common'
    file_name = 'stock_list.pkl'
    file_path = os.path.join(pickle_path, file_name)
    # 判断路径是否存在
    if os.path.exists(pickle_path):
        # 判断文件是否存在
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                dstore = pickle.load(f)
                trade_date = trade_cal()
                # 判断是否最近更新
                if dstore['last_update'] == end_date:
                    return dstore['stock_list']
                # 如果end_date为非交易日
                elif dstore['last_update'] >= max(trade_date):
                    f.close()
                    with open(file_path, 'wb') as f:
                        dstore['last_update'] = end_date
                        pickle.dump(dstore, f)
                else:
                    f.close()
                    from spiders import DayTick
                    DayTick.check()
                    rv = set()
                    cpoint = f'{DayTick.pkl_prefix}{dstore["last_update"]}{DayTick.pkl_sufix}'
                    for i in os.listdir(DayTick.pickle_path):
                        if i.startswith(DayTick.pkl_prefix) and i.endswith(
                                DayTick.pkl_sufix) and i > cpoint:
                            with open(os.path.join(DayTick.pickle_path, i), 'rb') as f:
                                df = pickle.load(f)
                                tscode = set(df['ts_code'])
                                rv = rv | tscode
                    with open(os.path.join(pickle_path, file_name), 'wb') as f:
                        dstore = {'last_update': end_date,
                                  'stock_list': rv}
                        pickle.dump(dstore, f)
    else:
        os.makedirs(pickle_path)
    # todo 此处循环引用，降低代码复用效率，暂时没有更好的解决方案
    from spiders import DayTick
    req = DayTick.check()
    rv = set()
    if req['diff']:
        DayTick.update()
    for i in os.listdir(DayTick.pickle_path):
        if i.startswith(DayTick.pkl_prefix) and i.endswith(DayTick.pkl_sufix):
            with open(os.path.join(DayTick.pickle_path, i), 'rb') as f:
                df = pickle.load(f)
                tscode = set(df['ts_code'])
                rv = rv | tscode
    with open(os.path.join(pickle_path, file_name), 'wb') as f:
        dstore = {'last_update': end_date,
                  'stock_list': rv}
        pickle.dump(dstore, f)
    return rv


class Spider(object):
    pickle_path = ''
    pkl_prefix = ''
    pkl_sufix = '.pkl'
    sql_table = ''
    sql_record_table = ''

    def __init__(self):
        super(Spider, self).__init__()

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    @classmethod
    def check(cls):
        pass

    @staticmethod
    def fetch(val):
        pass

    @classmethod
    def to_sql(cls):
        pass


class SpiderTimeBased(Spider):

    @classmethod
    def check(cls):
        if os.path.exists(cls.pickle_path):
            file_list = [i for i in os.listdir(cls.pickle_path) if
                         i.startswith(cls.pkl_prefix) and i.endswith(cls.pkl_sufix)]
            rep = f'{cls.pkl_prefix}(\d+)\{cls.pkl_sufix}'
            pattern = re.compile(rep)
            exist_date = set([pattern.findall(i)[0] for i in file_list])

        else:
            os.makedirs(cls.pickle_path)
            exist_date = set()
        trade_date = trade_cal()
        diff = trade_date - exist_date

        rv = {'online_data': len(trade_date),
              'local_data': len(exist_date),
              'max_local': max(exist_date) if exist_date else None,
              'max_online': max(trade_date),
              'diff': diff
              }
        return rv

    @classmethod
    def update(cls):
        log.info(f'UPDATING {cls.__name__}')
        req = cls.check()
        diff = req['diff']
        if diff:
            log.info(f'{len(diff)} dataset(s) to update')
            for i in diff:
                df = cls.fetch(i)
                file_name = f'{cls.pkl_prefix}{i}{cls.pkl_sufix}'
                file_path = os.path.join(cls.pickle_path, file_name)
                with open(file_path, 'wb') as f:
                    pickle.dump(df, f)
                log.info(f'{file_name} updated')
        else:
            log.info(f'data updated to the latest')

    @classmethod
    def update_db(cls):
        log.info(f'UPDATING DATABASE for {cls.__name__}')
        record = pd.read_sql(f'select * from {cls.sql_record_table};', engine)
        for item in os.listdir(cls.pickle_path):
            if item.startswith(cls.pkl_prefix) and item.endswith(cls.pkl_sufix):
                file_path = os.path.join(cls.pickle_path, item)
                with open(file_path, 'rb') as f:
                    content = f.read()
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                    if mtime.hour < 15:
                        mtime = mtime + datetime.timedelta(days=-1)
                    mt = mtime.strftime('%Y-%m-%d')
                    checksum = hashlib.md5(content).hexdigest()
                    rep = f'{cls.pkl_prefix}(\d+)\{cls.pkl_sufix}'
                    pattern = re.compile(rep)
                    trade_date = pattern.findall(item)[0]
                    # print(item, checksum, mt)
                    df = pickle.loads(content)
                    dd = record[record['origin_file'] == item]
                    if dd.empty:
                        df.to_sql(cls.sql_table, con=engine, if_exists='append', index=False)
                        engine.execute(f'insert into {cls.sql_record_table} (trade_date, origin_file, checksum, '
                                       f'last_update) values ("{trade_date}","{item}","{checksum}","{mt}");')
                        log.info(f'inserting {trade_date}')
                    else:
                        pass


class SpiderStokeBased(Spider):
    update_limit = 100

    @classmethod
    def check(cls):
        if os.path.exists(cls.pickle_path):
            file_list = [i for i in os.listdir(cls.pickle_path) if
                         i.startswith(cls.pkl_prefix) and i.endswith(cls.pkl_sufix)]
            rep = f'{cls.pkl_prefix}(\d+\.\w+)\{cls.pkl_sufix}'
            pattern = re.compile(rep)
            exist_stocks = set([pattern.findall(i)[0] for i in file_list])

        else:
            os.makedirs(cls.pickle_path)
            exist_stocks = set()
        slist = stock_list()
        diff = slist - exist_stocks

        rv = {'online_data': len(slist),
              'local_data': len(exist_stocks),
              'diff': diff
              }
        return rv

    @classmethod
    def update(cls):
        log.info(f'UPDATING {cls.__name__}')
        req = cls.check()
        diff = req['diff']
        length = len(diff)
        if diff:
            log.info(f'{len(diff)} dataset(s) to update')
            t0 = time.time()
            for i, item in enumerate(diff):
                df = cls.fetch(item)
                file_name = f'{cls.pkl_prefix}{item}{cls.pkl_sufix}'
                file_path = os.path.join(cls.pickle_path, file_name)
                with open(file_path, 'wb') as f:
                    pickle.dump(df, f)
                log.info(f'{file_name} updated')
                deltaT = time.time() - t0
                log.msg(f'{i + 1} out of {length} finished, time elapsed {round(deltaT, 2)}s,'
                        f'remaining {round(deltaT * (length - i) / (i + 1), 2)}s')
                if i / deltaT > (cls.update_limit * 0.9 / 60):
                    log.warn('TOO FAST, SLEEP FOR A WHILE')
                    time.sleep(1)
        else:
            log.info(f'data updated to the latest')

    @classmethod
    def update_db(cls):
        log.info(f'UPDATING DATABASE for {cls.__name__}')
        record = pd.read_sql(f'select * from {cls.sql_record_table};', engine)
        for item in os.listdir(cls.pickle_path):
            if item.startswith(cls.pkl_prefix) and item.endswith(cls.pkl_sufix):
                file_path = os.path.join(cls.pickle_path, item)
                with open(file_path, 'rb') as f:
                    content = f.read()
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                    if mtime.hour < 15:
                        mtime = mtime + datetime.timedelta(days=-1)
                    mt = mtime.strftime('%Y-%m-%d')
                    checksum = hashlib.md5(content).hexdigest()
                    rep = f'{cls.pkl_prefix}(\d+\.\w+)\{cls.pkl_sufix}'
                    pattern = re.compile(rep)
                    ts_code = pattern.findall(item)[0]
                    # print(item, checksum, mt)
                    df = pickle.loads(content)
                    dd = record[record['origin_file'] == item]
                    if dd.empty:
                        df.to_sql(cls.sql_table, con=engine, if_exists='append', index=False)
                        engine.execute(f'insert into {cls.sql_record_table} (ts_code, origin_file, checksum, '
                                       f'last_update) values ("{ts_code}","{item}","{checksum}","{mt}");')
                        log.info(f'inserting {ts_code}')
                    else:
                        pass

                # df.to_sql(cls.sql_table, con=engine, if_exists='append', index=False)


if __name__ == '__main__':
    print(stock_list())
    print(len(stock_list()))
