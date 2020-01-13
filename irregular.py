from utils import pro, engine
import pickle, os

pickle_path = 'raw/concept'
concept_prefix = 'concept_'
detail_prefix = 'detail_'
pkl_suffix = '.pkl'

# file_name = f'{concept_prefix}code_list{pkl_suffix}'
# file_path = os.path.join(pickle_path, file_name)
#
# if not os.path.exists(pickle_path):
#     os.makedirs(pickle_path)
#
# df = pro.concept()
# with open(file_path, 'wb') as f:
#     pickle.dump(df, f)
#
# for i in df['code']:
#     file_name = f'{detail_prefix}{i}{pkl_suffix}'
#     file_path = os.path.join(pickle_path, file_name)
#
#     df = pro.concept_detail(id=i)
#     with open(file_path, 'wb')as f:
#         pickle.dump(df, f)


# =================================================

# file_name = f'{concept_prefix}code_list{pkl_suffix}'
# file_path = os.path.join(pickle_path, file_name)
#
# with open(file_path, 'rb') as f:
#     df = pickle.load(f)
#     df.to_sql('concept', con=engine, if_exists='append', index=False)

for i in os.listdir(pickle_path):
    if i.startswith(detail_prefix) and i.endswith(pkl_suffix):
        file_name = i
        file_path = os.path.join(pickle_path, file_name)
        with open(file_path, 'rb') as f:
            df = pickle.load(f)
            # print(df)
            # print(df.columns)
            df.to_sql('concept_detail', con=engine, if_exists='append', index=False)
