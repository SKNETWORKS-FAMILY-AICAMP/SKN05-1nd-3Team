from sqlalchemy import create_engine
from project_package.GetData import get_car_regist_data, get_faq_data, get_company_data, get_car_sales_data
from project_package.DataStorage import storage_car_regist_data, storage_faq_data, storage_car_sales_data


# MySQL 데이터베이스 연결 생성
username = 'root'
password = 'choi657589!' #비밀번호 변경 필요
host = 'localhost'
database = 'project1'

# SQLAlchemy 엔진 생성
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database}')



# 전국 자동차 등록 현황 데이터 세팅
data_path = {
    'main' : './data/car_regist/sk_자동차 등록 현황.xlsx',
    'sido' : './data/car_regist/sk_시도별 자동차 등록 현황.xlsx',
    'yongdo' : './data/car_regist/sk_용도별 자동차 등록 현황.xlsx',
    'chajong' : './data/car_regist/sk_차종별 자동차 등록현황.xlsx'
}
dict_df = get_car_regist_data(path_dict=data_path)

storage_car_regist_data(dict_df=dict_df, engine=engine)



# FAQ 데이터 세팅
data_path = {
    'hyundai' : './data/faq-v2/hyundai_faq_cleaned2.csv',
    'kia' : './data/faq-v2/kia_faq_cleaned2.csv',
    'genesis' : './data/faq-v2/genesis_faq_cleaned2.csv',
    'chevrolet' : './data/faq-v2/chevrolet_faq_cleaned2.csv'
}
faq_table = get_faq_data(path_dict=data_path)
company_table = get_company_data()

storage_faq_data(faq_table=faq_table, company_table=company_table, engine=engine)



# 판매 실적 데이터 세팅
data_path = './data/car_sales/car_sales_data.csv'
car_sales_data = get_car_sales_data(data_path=data_path)

storage_car_sales_data(car_sales_data=car_sales_data, engine=engine)




# 데이터 삽입 후 연결 해제
engine.dispose()