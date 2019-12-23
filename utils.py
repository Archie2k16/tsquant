import os, re, datetime, pickle
import tushare as ts
from conf import ts_token, start_date
from abc import abstractmethod
import termcolor


def logprop(color, title):
    def wrapper(func):
        def wrapped(msg):
            termcolor.cprint(f'{title}:{msg}', color=color)

        return wrapped

    return wrapper


class log(object):

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

    @logprop('RED', 'ERROR')
    @staticmethod
    def err(msg):
        pass


ts.set_token(ts_token)
pro = ts.pro_api()


def end_date():
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
    pickle_path = 'raw/common'
    file_name = 'trade_cal.pkl'
    file_path = os.path.join(pickle_path, file_name)
    if os.path.exists(pickle_path):
        if os.path.isfile(file_path):
            with open(os.path.join(pickle_path, file_name), 'rb') as f:
                trade_date = pickle.load(f)
                if max(trade_date) == end_date:
                    return trade_date

    else:
        os.makedirs(pickle_path)

    online_date = pro.trade_cal(start_date=start_date, end_date=end_date)
    td = online_date[online_date['is_open'] == 1]
    trade_date = set(td['cal_date'])
    with open(os.path.join(pickle_path, file_name), 'wb') as f:
        pickle.dump(trade_date, f)
    return trade_date


def stock_list():
    pickle_path = 'raw/common'
    file_name = 'stock_list.pkl'
    file_path = os.path.join(pickle_path, file_name)
    if os.path.exists(pickle_path):
        if os.path.isfile(file_path):
            with open(os.path.join(pickle_path, file_name), 'rb') as f:
                trade_date = pickle.load(f)
                if max(trade_date) == end_date:
                    return trade_date

    else:
        os.makedirs(pickle_path)

    online_date = pro.trade_cal(start_date=start_date, end_date=end_date)
    td = online_date[online_date['is_open'] == 1]
    trade_date = set(td['cal_date'])
    with open(os.path.join(pickle_path, file_name), 'wb') as f:
        pickle.dump(trade_date, f)
    return trade_date


class Spider(object):
    pickle_path = ''
    pkl_prefix = ''
    pkl_sufix = '.pkl'
    sql_table = ''

    def __init__(self):
        super(Spider, self).__init__()

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    @classmethod
    def check(cls):
        pass

    @staticmethod
    def fetch(date):
        pass

    def to_sql(self):
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

    def to_sql(self):
        pass


class SpiderStokeBased(Spider):
    pass


if __name__ == '__main__':
    log.info('helo')
