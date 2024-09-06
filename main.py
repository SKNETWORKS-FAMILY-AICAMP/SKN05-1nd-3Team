

import streamlit as st
import pandas as pd
from project_package.StreamlitModule import create_connection, get_tables, get_table_data, \
                                            add_faqs_to_dict, table_mapping, show_analysis_result, show_faq





# MySQL 연결 생성
connection = create_connection()
# 데이터베이스에서 테이블 목록 가져오기
tables = get_tables(connection)
# FAQ 리스트에 넣기
faqs_dict = add_faqs_to_dict(connection)






######## Streamlit 앱 시작 ########
st.set_page_config(page_title="DB Analysis", layout="wide")
st.markdown(
    """
    <h1 style='display: inline;'>전국 자동차 등록 현황 및 기업 FAQ 조회</h1>
    <br>
    <h6 style='display: inline; float: right;'>3팀:  최영민, 서장호, 남석준, 장정호</h6>
    <br> 
    """,
    unsafe_allow_html=True
)


with st.expander("원본데이터"):
    st.text("")
    selected_table = st.selectbox("원본 데이터 선택", list(table_mapping.keys()))

    data = get_table_data(connection, table_mapping[selected_table])

    if data:
        st.text("")
        st.subheader(selected_table)
        st.dataframe(pd.DataFrame(data), width=1500)
    else:
        st.text("")
        st.write("데이터를 선택하지 않았거나 찾을 수 없습니다.")


# 두 개의 수평 구역 (컨테이너 내에서 수평으로 배치)
with st.container():
    col1, col2 = st.columns([2, 1])  # 비율에 따라 구역 크기 조절
    
    with col1:
        st.subheader("분석 결과")

        # 분석 메뉴 선택
        analysis_option = st.selectbox(
            "분석 항목 검색",
            ["연도 별 '수도권'/'비수도권' 자동차 등록 대 수",
            "연도 별 자동차 등록 대 수 및 등록 증가율",
            "각 시도의 자동차 등록 대수와 증가율",
            "차종 별 등록 대 수",
            "용도 별 자동차 등록 대 수와 증가율",
            "전체 차량 연도 별 증가율",
            "연도 별 각 브랜드의 판매량 추세",
            "2022, 2023, 2024 각 브랜드의 판매량 비교",
            "각 브랜드의 총 판매량",
            "시간에 따른 브랜드별 누적 판매량"],
        )


        show_analysis_result(analysis_option=analysis_option, connection=connection)
    
    with col2:
        st.subheader("브랜드 FAQ")

        # 기업 명 선택
        selected_company = st.selectbox(
            "브랜드 별 FAQ 조회",
            [
                "없음", "현대", "제네시스", "기아", "쉐보레"
            ]
        )

        if selected_company == "없음":
            st.write("브랜드를 선택해 주세요")
        else:
            show_faq(faqs_dict=faqs_dict, selected_company=selected_company)



    
# MySQL 연결 닫기
connection.close()