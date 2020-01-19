import pickle
from conf import db_conf2
from sqlalchemy import create_engine
import pandas as pd
from functools import reduce
from sqlalchemy.exc import IntegrityError

engine = create_engine(db_conf2)

data = engine.execute('select date_format(trade_date, "%Y%m%d"),date_id from trade_date;').fetchall()
date_dict = dict(data)

work_dirs = ['day_tick', 'daily_basic', 'adj_factor', 'money_flow']
suffix = '.pkl'

for date in date_dict.keys():
    print(f'processing data on {date}')
    df_list = []
    for i in work_dirs:
        with open(f'raw/{i}/{i}_{date}{suffix}', 'rb') as f:
            dd = pickle.load(f)
            df_list.append(dd)
            f.close()
    df_list[0].drop(['trade_date'], axis=1, inplace=True)
    df_list[1].drop(['trade_date', 'close'], axis=1, inplace=True)
    df_list[2].drop(['trade_date'], axis=1, inplace=True)
    df_list[3].drop(['trade_date'], axis=1, inplace=True)
    # for i in df_list:
    #     print(i)

    df = reduce(lambda x, y: x.join(y.set_index('ts_code'), on='ts_code', how='left'), df_list)

    # df.to_sql('sz000001', con=engine, if_exists='append', index=False)

    for i in range(len(df)):
        s = df.iloc[i:i + 1, :]
        ts_code = s.iloc[0]['ts_code'].split('.')
        table_name = ts_code[1].lower() + ts_code[0]
        print(f'\tprocessing {ts_code}')
        ddd = s[['open', 'high', 'low', 'close', 'pre_close', 'change',
                 'pct_chg', 'vol', 'amount', 'turnover_rate', 'turnover_rate_f',
                 'volume_ratio', 'pe', 'pe_ttm', 'pb', 'ps', 'ps_ttm', 'total_share',
                 'float_share', 'free_share', 'total_mv', 'circ_mv', 'adj_factor',
                 'buy_sm_vol', 'buy_sm_amount', 'sell_sm_vol', 'sell_sm_amount',
                 'buy_md_vol', 'buy_md_amount', 'sell_md_vol', 'sell_md_amount',
                 'buy_lg_vol', 'buy_lg_amount', 'sell_lg_vol', 'sell_lg_amount',
                 'buy_elg_vol', 'buy_elg_amount', 'sell_elg_vol', 'sell_elg_amount',
                 'net_mf_vol', 'net_mf_amount']]
        ddd['date_id'] = date_dict[date]
        ddd['active'] = True
        try:
            ddd.to_sql(table_name, con=engine, if_exists='append', index=False)
        except Exception as e:
            if isinstance(e, IntegrityError):
                print(f'duplicate entry for {table_name} on {date}, ignored')
            else:
                print(e)
                break
