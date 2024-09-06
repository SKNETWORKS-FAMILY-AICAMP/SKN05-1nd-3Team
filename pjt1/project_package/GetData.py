
# import library
import pandas as pd



def clean_main(data:pd.DataFrame) -> pd.DataFrame:
    '''

    >> cleaning "자동차 등록 현황"

    [input] : data(pd.DataFrame)
    [output] : cleaned_data(pd.DataFrame)

    [cleaned data column name]
    1. year : 연도
    2. car_regi : 자동차 등록대수 (만대)
    3. car_ic : 전년대비 증가대수 (천대)
    4. car_rat : 전년대비 증감비율 (%)

    '''
    data_t = data.loc[1:4][:].transpose()
    data_t = data_t[1:]
    data_clean = data_t.reset_index(drop=True)
    data_clean.columns = ['year', 'car_regi', 'car_ic', 'car_rat']

    for idx in range(len(data_clean['car_regi'])):
        tmp = data_clean['car_regi'][idx].split(',')
        data_clean.loc[idx, 'car_regi'] = int(tmp[0] + tmp[1])

    return data_clean



def clean_sido(data:pd.DataFrame)->pd.DataFrame :
    '''

    >> cleaning "시도별 자동차 등록 현황"

    [input] : data(pd.DataFrame)
    [output] : cleaned_data(pd.DataFrame)

    [cleaned data column name]
    1. year : 연도
    2. car_regi : 자동차 등록대수 (만대)
    3. etc.. : 시도별 이름
    
    '''
    data_t = data.loc[1:19].transpose()
    data_t = data_t[1:]
    data_clean = data_t.reset_index(drop=True)
    data_clean.columns = ['year', 'car_regi', 'seoul', 'busan', 'daegu', 'incheon', 'gwangju', 'daejeon', 'ulsan', 'sejong',
                            'gyeonggi', 'gangwon', 'chungbuk', 'chungnam', 'jeonbuk', 'jeonnam', 'gyeongbuk', 'gyeongnam', 'jeju']
    
    for idx in range(len(data_clean['car_regi'])):
        tmp = data_clean['car_regi'][idx].split(',')
        data_clean.loc[idx, 'car_regi'] = int(tmp[0] + tmp[1])

    data_clean = data_clean[data_clean['year'].astype(int) >= 2014]
    
    return data_clean



def clean_yongdo(data:pd.DataFrame)->pd.DataFrame:
    '''

    >> cleaning "용도별 자동차 등록 현황"

    [input] : data(pd.DataFrame)
    [output] : cleaned_data(pd.DataFrame)

    [cleaned data column name]
    1. year : 연도
    2. car_regi : 자동차 등록대수 (만대)
    3. official : 관용차
    4. private : 자가용
    5. commercial : 영업용
    
    '''
    data_t = data.loc[1:5].transpose()
    data_t = data_t[1:]
    data_clean = data_t.reset_index(drop=True)
    data_clean.columns = ['year', 'car_regi', 'official', 'private', 'commercial']

    for idx in range(len(data_clean['car_regi'])):
        tmp = data_clean['car_regi'][idx].split(',')
        data_clean.loc[idx, 'car_regi'] = int(tmp[0] + tmp[1])
    
    for idx in range(len(data_clean['private'])):
        tmp = data_clean['private'][idx].split(',')
        data_clean.loc[idx, 'private'] = int(tmp[0] + tmp[1])
    
    data_clean = data_clean[data_clean['year'].astype(int) >= 2014]
    
    return data_clean



def clean_chajong(data:pd.DataFrame)->pd.DataFrame:
    '''

    >> cleaning "차종별 자동차 등록 현황"

    [input] : data(pd.DataFrame)
    [output] : cleaned_data(pd.DataFrame)

    [cleaned data column name]
    1. year : 연도
    2. car_regi : 자동차 등록대수 (만대)
    3. passenger : 승용차
    4. van : 승합차
    5. truck : 화물차
    6. special : 특수차
    
    '''
    data_t = data.loc[1:7].transpose()
    data_t = data_t[1:]
    data_clean = data_t.reset_index(drop=True)
    data_clean.columns = ['year', 'car_regi', 'ic_amount', 'passenger', 'van', 'truck', 'special']

    for idx in range(len(data_clean['car_regi'])):
        tmp = data_clean['car_regi'][idx].split(',')
        data_clean.loc[idx, 'car_regi'] = int(tmp[0] + tmp[1])
    
    for idx in range(len(data_clean['passenger'])):
        tmp = data_clean['passenger'][idx].split(',')
        data_clean.loc[idx, 'passenger'] = int(tmp[0] + tmp[1])
    
    data_clean = data_clean[data_clean['year'].astype(int) >= 2014]
    
    return data_clean



def get_car_regist_data(path_dict):

    path_sd = path_dict['sido']
    path_yd = path_dict['yongdo']
    path_main = path_dict['main']
    path_cj = path_dict['chajong']

    df_sd = pd.read_excel(path_sd)
    df_yd = pd.read_excel(path_yd)
    df_main = pd.read_excel(path_main)
    df_cj = pd.read_excel(path_cj)

    df_main = clean_main(df_main)
    df_sd = clean_sido(df_sd)
    df_yd = clean_yongdo(df_yd)
    df_cj = clean_chajong(df_cj)

    return {
        'main' : df_main,
        'sido' : df_sd,
        'yongdo' : df_yd,
        'chajong' : df_cj
    }


def get_faq_data(path_dict):

    path_h = path_dict['hyundai']
    path_k = path_dict['kia']
    path_g = path_dict['genesis']
    path_c = path_dict['chevrolet']

    hyundai = pd.read_csv(path_h, encoding='utf-8', index_col='Unnamed: 0')
    kia = pd.read_csv(path_k, encoding='utf-8', index_col='Unnamed: 0')
    genesis = pd.read_csv(path_g, encoding='utf-8', index_col='Unnamed: 0')
    chevrolet = pd.read_csv(path_c, encoding='utf-8', index_col='Unnamed: 0')

    hyundai['id'] = 1
    kia['id'] = 2
    genesis['id'] = 3
    chevrolet['id'] = 4

    faq_data = pd.concat([hyundai, kia, genesis, chevrolet])

    return faq_data

def get_company_data():
    company_table = [
        {'comp_name' : '현대'},
        {'comp_name' : '기아'},
        {'comp_name' : '제네시스'},
        {'comp_name' : '쉐보레'}
    ]

    company_data = pd.DataFrame(company_table)

    return company_data

def get_car_sales_data(data_path):
    path = data_path
    car_sales = pd.read_csv(path, index_col='Unnamed: 0')
    car_sales = car_sales.reset_index()
    car_sales = car_sales.rename(columns={
                    'index' : 'year',
                    '현대' : 'hyundai',
                    '기아' : 'kia',
                    '제네시스' : 'genesis',
                    '쉐보레' : 'chevorlet'
                })

    hyundai = car_sales[['year', 'hyundai']].copy()
    hyundai = hyundai.rename(columns={'hyundai' : 'car_regi'})
    hyundai['id'] = 1

    kia = car_sales[['year', 'kia']].copy()
    kia = kia.rename(columns={'kia' : 'car_regi'})
    kia['id'] = 2

    genesis = car_sales[['year', 'genesis']].copy()
    genesis = genesis.rename(columns={'genesis' : 'car_regi'})
    genesis['id'] = 3

    chevrolet = car_sales[['year', 'chevorlet']].copy()
    chevrolet = chevrolet.rename(columns={'chevorlet' : 'car_regi'})
    chevrolet['id'] = 4

    df_car_sales = pd.concat([hyundai, kia, genesis, chevrolet])

    return df_car_sales