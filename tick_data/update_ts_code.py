from utils import pro, end_date
from conf import db_conf2
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(db_conf2)

df1 = pro.stock_basic(list_status='L')
df2 = pro.stock_basic(list_status='D')
df3 = pro.stock_basic(list_status='P')
df1 = df1.append(df2)
df1 = df1.append(df3)

df1.sort_values(by=['list_date', 'ts_code'], inplace=True)

ts_data = list(df1['ts_code'])

exist_df = pd.read_sql('select ts_code from ts_code order by ts_id;', con=engine)
exist_data = list(exist_df['ts_code'])
to_update = list(ts_data)

for i in exist_data:
    if i in to_update:
        index = to_update.index(i)
        to_update.pop(index)

print(ts_data)
print(exist_data)
print(to_update)

insert_val = ','.join([f'("{i}")' for i in to_update])
if to_update:
    engine.execute(f'insert into ts_code (ts_code) VALUES {insert_val};')

