from sqlalchemy import create_engine, Table, Column, Integer, VARCHAR, MetaData
from sqlalchemy.exc import SQLAlchemyError
from project_package.GetData import get_car_regist_data
import pandas as pd



def storage_car_regist_data(dict_df, engine):
    df_main = dict_df['main']
    df_sd = dict_df['sido']
    df_yd = dict_df['yongdo']
    df_cj = dict_df['chajong']

    # DataFrame을 MySQL의 테이블로 삽입 (테이블이 없으면 생성 : replace, 이어 붙이기 : append)
    df_main.to_sql('main', con=engine, if_exists='append', index=False)
    df_sd.to_sql('sido', con=engine, if_exists='append', index=False)
    df_yd.to_sql('yongdo', con=engine, if_exists='append', index=False)
    df_cj.to_sql('chajong', con=engine, if_exists='append', index=False)


def storage_faq_data(faq_table, company_table, engine):
    # 메타데이터 및 테이블 정의
    metadata = MetaData()

    # 데이터베이스에 저장할 테이블 정의
    table = Table('companytbl', metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('comp_name', VARCHAR(150))
                )

    metadata.create_all(engine)  # 테이블 생성

    try:
        company_table.to_sql('companytbl', con=engine, if_exists='append', index=False)
        faq_table.to_sql('faqtbl', con=engine, if_exists='append', index=False)
        print("Data inserted successfully.")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")


def storage_car_sales_data(car_sales_data, engine):
    try:
        car_sales_data.to_sql('carsalestbl', con=engine, if_exists='append', index=False)
        print("Data inserted successfully.")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")