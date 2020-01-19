from utils import pro, end_date
from conf import db_conf2
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(db_conf2)
trade_date = pro.trade_cal(end_date=end_date)
td = trade_date[trade_date['is_open'] == 1]
td_data = list(td['cal_date'])
exist_df = pd.read_sql('select date_format(trade_date, "%Y%m%d") as trade_date from trade_date order by date_id;',
                       con=engine)
exist_data = list(exist_df['trade_date'])

to_update = list(td_data)

for i in exist_data:
    if i in to_update:
        index = to_update.index(i)
        to_update.pop(index)

insert_val = ','.join([f'("{i}")' for i in to_update])
if to_update:
    engine.execute(f'insert into trade_date (trade_date) VALUES {insert_val};')
