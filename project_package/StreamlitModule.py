import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# MySQL 데이터베이스 연결 설정
def create_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='choi657589!',
        database='project1',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# 데이터베이스에서 테이블 목록 가져오기
def get_tables(connection):
    query = "SHOW TABLES"
    with connection.cursor() as cursor:
        cursor.execute(query)
        tables = cursor.fetchall()
    return [table['Tables_in_project1'] for table in tables]

# 선택된 테이블의 데이터를 가져오기
def get_table_data(connection, table_name):
    query = f"SELECT * FROM {table_name}"
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
    return data

# SQL 쿼리 실행 함수
def execute_query(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
    return pd.DataFrame(data)

# FAQ 데이터를 faqs_dict에 추가
def add_faqs_to_dict(connection):
    faqs_dict = {
        "현대": [],
        "제네시스": [],
        "기아": [],
        "쉐보레": []
    }
    
    # faqTBL 테이블 데이터 가져오기
    faq_data = get_table_data(connection, 'faqtbl')
    
    # 각 FAQ 항목을 faqs_dict에 추가
    for row in faq_data:
        # 쿼리에서 얻은 ID를 통해 적절한 기업 이름을 매칭
        company_name = get_company_name_by_id(connection, row['id'])
        if company_name in faqs_dict:
            faqs_dict[company_name].append({
                "question": row['question'],
                "answer": row['answer']
            })

    return faqs_dict

# 기업 ID에 따른 이름을 가져오는 함수
def get_company_name_by_id(connection, company_id):
    query = f"SELECT comp_name FROM companyTBL WHERE id = {company_id}"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
    return result['comp_name'] if result else 'Unknown'

# 선택된 분석 항목에 따라 쿼리 실행 및 결과 표시
def show_analysis_result(analysis_option, connection):
    if analysis_option:
        query = query_mapping[analysis_option]
        result = execute_query(connection, query)

        # 결과가 있는 경우 시각화
        if not result.empty:
            # 결과 컨테이너 생성
            analysis_container = st.container()

            # 분석 테이블, 분석 그래프 탭
            tab1, tab2 = st.tabs(["분석 그래프", "분석 테이블"])

            with tab2:
                st.dataframe(result, width=800, height=600)

            with tab1:
                # 분석 메뉴 1
                if analysis_option == "연도 별 '수도권'/'비수도권' 자동차 등록 대 수":
                    # 색상 맵 설정
                    color_map = {
                        'capital_region': 'rgba(0, 0, 255, 1)',  # 진한 파란색
                        'non_capital_region': 'rgba(255, 165, 0, 1)'  # 진한 주황색
                    }
                    
                    # 트렌드 라인 색상 설정 (투명도 적용)
                    trend_color_map = {
                        'capital_region': 'rgba(0, 0, 255, 1)',  # 연한 파란색
                        'non_capital_region': 'rgba(255, 165, 0, 1)'  # 연한 주황색
                    }
                    
                    # 수도권 막대 그래프 생성 (두꺼운 막대)
                    capital_trace = go.Bar(
                        x=result['year'], 
                        y=result['capital_region'], 
                        name='수도권 지역', 
                        marker=dict(color=color_map['capital_region'], line=dict(width=0.5, color='black')),
                        width=0.2  # 두꺼운 막대
                    )
                    
                    # 비수도권 막대 그래프 생성 (얇은 막대)
                    non_capital_trace = go.Bar(
                        x=result['year'], 
                        y=result['non_capital_region'], 
                        name='비수도권 지역', 
                        marker=dict(color=color_map['non_capital_region'], line=dict(width=0.5, color='black')),
                        width=0.4  # 얇은 막대
                    )
                    
                    # 트렌드 라인 추가
                    trend_capital_trace = go.Scatter(
                        x=result['year'], 
                        y=result['capital_region'], 
                        mode='lines+markers', 
                        name='수도권 지역 트렌드', 
                        line=dict(color=trend_color_map['capital_region'], width=2),  # 연한 파란색 라인
                        marker=dict(color=trend_color_map['capital_region'])  # 연한 파란색 마커
                    )
                    
                    trend_non_capital_trace = go.Scatter(
                        x=result['year'], 
                        y=result['non_capital_region'], 
                        mode='lines+markers', 
                        name='비수도권 지역 트렌드', 
                        line=dict(color=trend_color_map['non_capital_region'], width=2),  # 연한 주황색 라인
                        marker=dict(color=trend_color_map['non_capital_region'])  # 연한 주황색 마커
                    )
                    
                    # 그래프 생성
                    fig = go.Figure(data=[non_capital_trace, capital_trace, trend_capital_trace, trend_non_capital_trace])
                    
                    # 레이아웃 업데이트
                    fig.update_layout(
                        title="수도권(서울, 인천, 경기) vs 비수도권(그 외)",
                        xaxis_title="년도",
                        yaxis_title="인구수",
                        barmode='overlay',  # 막대 겹치기
                        bargap=0.2,  # 막대 사이의 간격
                        legend_title="지역 구분"
                    )

                    st.plotly_chart(fig)
                

                # 분석 메뉴 2
                elif analysis_option == "연도 별 자동차 등록 대 수 및 등록 증가율":
                    fig1 = px.line(result, x='year', y='car_regi',
                                  title="연도 별 자동차 등록 대 수 및 등록 증가율")
                    fig1.update_layout(xaxis_title="년도", yaxis_title="등록 대 수")
                    fig2 = px.line(result, x='year', y='car_ic')
                    fig2.update_layout(xaxis_title="년도", yaxis_title="전년 대비 증가 대 수")
                    fig3 = px.line(result, x='year', y='car_rat')
                    fig3.update_layout(xaxis_title="년도", yaxis_title="전년 대비 증가 비율")
                    st.plotly_chart(fig1)
                    st.plotly_chart(fig2)
                    st.plotly_chart(fig3)
                
                
                # 분석 메뉴 3
                elif analysis_option == "각 시도의 자동차 등록 대수와 증가율":

                    region_mapping = {
                        '서울' : 'seoul', '부산' : 'busan', '대구' : 'daegu', 
                        '인천' : 'incheon', '광주' : 'gwangju', '대전' : 'daejeon', 
                        '울산' : 'ulsan', '세종' : 'sejong', '경기' : 'gyeonggi', 
                        '강원' : 'gangwon', '충북' : 'chungbuk', '충남' : 'chungnam', 
                        '전북' : 'jeonbuk', '전남' : 'jeonnam', '경북' : 'gyeongbuk', 
                        '경남' : 'gyeongnam', '제주' : 'jeju'
                    }

                    selected_region = st.multiselect('지역 선택', options=['서울', '부산', '대구', '인천', '광주', '대전', 
                                                                            '울산', '세종', '경기', '강원', 
                                                                            '충북', '충남', '전북', '전남', 
                                                                            '경북', '경남', '제주'], default=['서울'])
        
                    fig_1 = px.line(result, x='year', y=[region_mapping[region] for region in selected_region], title="각 시도의 자동차 등록 대수")

                    newnames = {
                        'seoul' : '서울', 'busan' : '부산', 'daegu' : '대구', 
                        'incheon' : '인천', 'gwangju' : '광주', 'daejeon' : '대전', 
                        'ulsan' : '울산', 'sejong' : '세종', 'gyeonggi' : '경기', 
                        'gangwon' : '강원', 'chungbuk' : '충북', 'chungnam' : '충남', 
                        'jeonbuk' : '전북', 'jeonnam' : '전남', 'gyeongbuk' : '경북', 
                        'gyeongnam' : '경남', 'jeju' : '제주'
                    }
                    fig_1.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                                          legendgroup = newnames[t.name],
                                                          hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
                    
                    
                    fig_1.update_layout(xaxis_title="년도", yaxis_title="등록 대 수", legend_title="지역명")
                    st.plotly_chart(fig_1)

                    growth_mapping = {
                        '서울' : 'seoul_growth_rate', '부산' : 'busan_growth_rate', '대구' : 'daegu_growth_rate', 
                        '인천' : 'incheon_growth_rate', '광주' : 'gwangju_growth_rate', '대전' : 'daejeon_growth_rate', 
                        '울산' : 'ulsan_growth_rate', '세종' : 'sejong_growth_rate', '경기' : 'gyeonggi_growth_rate', 
                        '강원' : 'gangwon_growth_rate', '충북' : 'chungbuk_growth_rate', '충남' : 'chungnam_growth_rate', 
                        '전북' : 'jeonbuk_growth_rate', '전남' : 'jeonnam_growth_rate', '경북' : 'gyeongbuk_growth_rate', 
                        '경남' : 'gyeongnam_growth_rate', '제주' : 'jeju_growth_rate'
                    }

                    
                    fig_2 = px.line(result, x='year', y=[growth_mapping[region] for region in selected_region], title="각 시도의 자동차 등록 대수 증가율")

                    newnames = {
                        'seoul_growth_rate' : '서울', 'busan_growth_rate' : '부산', 'daegu_growth_rate' : '대구', 
                        'incheon_growth_rate' : '인천', 'gwangju_growth_rate' : '광주', 'daejeon_growth_rate' : '대전', 
                        'ulsan_growth_rate' : '울산', 'sejong_growth_rate' : '세종', 'gyeonggi_growth_rate' : '경기', 
                        'gangwon_growth_rate' : '강원', 'chungbuk_growth_rate' : '충북', 'chungnam_growth_rate' : '충남', 
                        'jeonbuk_growth_rate' : '전북', 'jeonnam_growth_rate' : '전남', 'gyeongbuk_growth_rate' : '경북', 
                        'gyeongnam_growth_rate' : '경남', 'jeju_growth_rate' : '제주'
                    }
                    fig_2.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                                          legendgroup = newnames[t.name],
                                                          hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
                    
                    fig_2.update_layout(xaxis_title="년도", yaxis_title="등록 증가율", legend_title = "지역명")
                    st.plotly_chart(fig_2)
                    

                # 분석 메뉴 4
                elif analysis_option == "차종 별 등록 대 수":
                    # selected_chajong = st.sidebar.multiselect('Select Regions', options=['passenger', 'van', 'truck', 'special'], default=['passenger'])
                    chajong_mapping = {
                        '승용차' : 'passenger', '승합차' : 'van', '화물차' : 'truck', '특수차' : 'special'
                    }

                    selected_chajong = st.multiselect('차종 선택', options=['승용차', '승합차', '화물차', '특수차'], default=['승용차'])
        
                    fig = px.line(result, x='year', y=[chajong_mapping[chajong] for chajong in selected_chajong], title="차종별 등록대수")

                    newnames = {
                        'passenger' : '승용차', 'van' : '승합차', 'truck' : '화물차', 'special' : '특수차'
                    }
                    fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                                          legendgroup = newnames[t.name],
                                                          hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
                    
                    fig.update_layout(xaxis_title="년도", yaxis_title="등록 대 수", legend_title = "차종")

                    st.plotly_chart(fig)
                

                # 분석 메뉴 5
                elif analysis_option == "용도 별 자동차 등록 대 수와 증가율":
                    fig_1 = px.line(result, x='year', y=['official_change', 'private_change', 'commercial_change'])
                    newnames = {
                        'official_change' : '관용', 'private_change' : '자가용', 'commercial_change' : '영업용'
                    }
                    fig_1.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                                          legendgroup = newnames[t.name],
                                                          hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
                    
                    fig_1.update_layout(xaxis_title="년도", yaxis_title="증가율", legend_title = "용도")


                    fig_2 = px.line(result, x='year', y=['official', 'private', 'commercial'],
                                  title="용도 별 자동차 등록 대수와 증가율")
                    newnames = {
                        'official' : '관용', 'private' : '자가용', 'commercial' : '영업용'
                    }
                    fig_2.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                                          legendgroup = newnames[t.name],
                                                          hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
                    
                    fig_2.update_layout(xaxis_title="년도", yaxis_title="등록 대 수", legend_title = "용도")

                    st.plotly_chart(fig_2)
                    st.plotly_chart(fig_1)


                # 분석 메뉴 6
                elif analysis_option == "전체 차량 연도 별 증가율":
                    fig = px.line(result, x='year', y='growth_rate', 
                                  title="전체 차량 연도 별 증가율")
                    
                    fig.update_layout(xaxis_title="년도", yaxis_title="증가율")
                    st.plotly_chart(fig)
                

                # 분석 메뉴 7
                elif analysis_option == "연도 별 각 브랜드의 판매량 추세":
                    line_fig = go.Figure()
                    new_names = {
                        "Hyundai" : '현대', "Kia" : '기아', "Genesis" : '제네시스', "Chevrolet" : '쉐보레'
                    }
                    for brand in ["Hyundai", "Kia", "Genesis", "Chevrolet"]:
                        line_fig.add_trace(go.Scatter(x=result["Year"], y=result[brand], mode='lines+markers', name=new_names[brand]))
                    
                    line_fig.update_layout(title="연도 별 각 브랜드의 판매량 추세", xaxis_title="연도", yaxis_title="판매량")
                    st.plotly_chart(line_fig)
                

                # 분석 메뉴 8
                elif analysis_option == "2022, 2023, 2024 각 브랜드의 판매량 비교":
                    bar_fig = go.Figure()
                    new_names = {
                        "Hyundai" : '현대', "Kia" : '기아', "Genesis" : '제네시스', "Chevrolet" : '쉐보레'
                    }
                    for brand in ["Hyundai", "Kia", "Genesis", "Chevrolet"]:
                        bar_fig.add_trace(go.Bar(x=result["Year"], y=result[brand], name=new_names[brand]))
                    bar_fig.update_layout(barmode='group', title="2022, 2023, 2024 각 브랜드의 판매량 비교", xaxis_title="연도", yaxis_title="판매량")
                    st.plotly_chart(bar_fig)
                

                # 분석 메뉴 9
                elif analysis_option == "각 브랜드의 총 판매량":
                    total_sales = result.set_index('Year').sum()
                    new_names = ['현대', '기아', '제네시스', '쉐보레']
                    pie_fig = go.Figure(go.Pie(labels=new_names, values=total_sales.values, hole=0.3))
                    
                    pie_fig.update_layout(title="각 브랜드의 총 판매량 (2022-2024)")
                    st.plotly_chart(pie_fig)
                

                # 분석 메뉴 10
                elif analysis_option == "시간에 따른 브랜드별 누적 판매량":
                    df_melted = result.melt(id_vars="Year", var_name="Brand", value_name="Sales")
                    fig = px.area(df_melted, x="Year", y="Sales", color="Brand",
                                  title="시간에 따른 브랜드별 누적 판매량",
                                  labels={"Sales": "누적 판매량", "Year": "연도", "Brand": "브랜드"})
                    newnames = {
                        "Hyundai" : '현대', "Kia" : '기아', "Genesis" : '제네시스', "Chevrolet" : '쉐보레'
                    }
                    fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                                          legendgroup = newnames[t.name],
                                                          hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
                    st.plotly_chart(fig)
        else:
            st.write("데이터가 없습니다.")
        

def show_faq_pages(filtered_faqs):
    items_per_page = 5
    total_pages = (len(filtered_faqs) + items_per_page - 1) // items_per_page

    if 'page' not in st.session_state:
        st.session_state.page = 1

    page = st.session_state.page

    if page < 1:
        st.session_state.page = 1
        page = 1
    elif page > total_pages:
        st.session_state.page = total_pages
        page = total_pages

    # 현재 페이지의 아이템 인덱스 계산
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    if len(filtered_faqs) < end_index:
        end_index = len(filtered_faqs)
    current_page_data = filtered_faqs[start_index:end_index]

    
    for faq in current_page_data:
        with st.expander(f"**{faq['question']}**"):
            st.write(faq['answer'])
    

    col1, col2, col3 = st.columns(3)
    with col1:
        if page > 1:
            if st.button("이전"):
                st.session_state.page -= 1
                st.rerun(scope="fragment")
    
    with col2:
        st.write(f"{page} - {total_pages}")

    with col3:
        if page < total_pages:
            if st.button("다음"):
                st.session_state.page += 1
                st.rerun(scope="fragment")


@st.fragment
def show_faq(selected_company, faqs_dict):
    if selected_company != "없음":
        faqs = faqs_dict.get(selected_company, [])
        if faqs:
            st.markdown(f"#### {selected_company}")
            
            # 질문 검색
            search_query = st.text_input('검색할 질문을 입력하세요:')
            
            # 검색어를 기준으로 FAQ 목록 필터링
            filtered_faqs = [faq for faq in faqs if search_query.lower() in faq["question"].lower()]
            
            if filtered_faqs:

                show_faq_pages(filtered_faqs=filtered_faqs)

            else:
                st.write("검색 결과가 없습니다.")
        else:
            st.write("FAQ 데이터가 없습니다.")
    else:
        st.write("기업을 선택해 주세요.")

















table_mapping = {
    '📌 브랜드 별 판매량' : 'carsalestbl',
    '📌 차종 별 등록 수' : 'chajong',
    '📌 시도 별 등록 수' : 'sido',
    '📌 용도 별 등록 수' : 'yongdo',
    '📌 자동차 등록 현황' : 'main',
}






# 쿼리 매핑
query_mapping = {
    "연도 별 '수도권'/'비수도권' 자동차 등록 대 수": """
        SELECT 
            s.year,
            (seoul + incheon + gyeonggi) AS capital_region,
            (m.car_regi - (seoul + incheon + gyeonggi)) AS non_capital_region,
            ROUND((seoul + incheon + gyeonggi) * 1.0 / (m.car_regi - (seoul + incheon + gyeonggi)), 2) AS ratio
        FROM 
            sido s
        JOIN 
            main m ON s.year = m.year;
    """,
    "연도 별 자동차 등록 대 수 및 등록 증가율": """
        select * from main;
    """,
    "각 시도의 자동차 등록 대수와 증가율": """
        SELECT 
            s.year, 
            seoul, 
            ROUND(((seoul - LAG(seoul) OVER (ORDER BY year)) / LAG(seoul) OVER (ORDER BY year)) * 100, 2) AS seoul_growth_rate,
            busan, 
            ROUND(((busan - LAG(busan) OVER (ORDER BY year)) / LAG(busan) OVER (ORDER BY year)) * 100, 2) AS busan_growth_rate,
            daegu, 
            ROUND(((daegu - LAG(daegu) OVER (ORDER BY year)) / LAG(daegu) OVER (ORDER BY year)) * 100, 2) AS daegu_growth_rate,
            incheon,
            ROUND(((incheon - LAG(incheon) OVER (ORDER BY year)) / LAG(incheon) OVER (ORDER BY year)) * 100, 2) AS incheon_growth_rate,
            gwangju,
            ROUND(((gwangju - LAG(gwangju) OVER (ORDER BY year)) / LAG(gwangju) OVER (ORDER BY year)) * 100, 2) AS gwangju_growth_rate,
            daejeon,
            ROUND(((daejeon - LAG(daejeon) OVER (ORDER BY year)) / LAG(daejeon) OVER (ORDER BY year)) * 100, 2) AS daejeon_growth_rate,
            ulsan,
            ROUND(((ulsan - LAG(ulsan) OVER (ORDER BY year)) / LAG(ulsan) OVER (ORDER BY year)) * 100, 2) AS ulsan_growth_rate,
            sejong,
            ROUND(((sejong - LAG(sejong) OVER (ORDER BY year)) / LAG(sejong) OVER (ORDER BY year)) * 100, 2) AS sejong_growth_rate,
            gyeonggi,
            ROUND(((gyeonggi - LAG(gyeonggi) OVER (ORDER BY year)) / LAG(gyeonggi) OVER (ORDER BY year)) * 100, 2) AS gyeonggi_growth_rate,
            gangwon,
            ROUND(((gangwon - LAG(gangwon) OVER (ORDER BY year)) / LAG(gangwon) OVER (ORDER BY year)) * 100, 2) AS gangwon_growth_rate,
            chungbuk,
            ROUND(((chungbuk - LAG(chungbuk) OVER (ORDER BY year)) / LAG(chungbuk) OVER (ORDER BY year)) * 100, 2) AS chungbuk_growth_rate,
            chungnam,
            ROUND(((chungnam - LAG(chungnam) OVER (ORDER BY year)) / LAG(chungnam) OVER (ORDER BY year)) * 100, 2) AS chungnam_growth_rate,
            jeonbuk,
            ROUND(((jeonbuk - LAG(jeonbuk) OVER (ORDER BY year)) / LAG(jeonbuk) OVER (ORDER BY year)) * 100, 2) AS jeonbuk_growth_rate,
            jeonnam,
            ROUND(((jeonnam - LAG(jeonnam) OVER (ORDER BY year)) / LAG(jeonnam) OVER (ORDER BY year)) * 100, 2) AS jeonnam_growth_rate,
            gyeongbuk,
            ROUND(((gyeongbuk - LAG(gyeongbuk) OVER (ORDER BY year)) / LAG(gyeongbuk) OVER (ORDER BY year)) * 100, 2) AS gyeongbuk_growth_rate,
            gyeongnam,
            ROUND(((gyeongnam - LAG(gyeongnam) OVER (ORDER BY year)) / LAG(gyeongnam) OVER (ORDER BY year)) * 100, 2) AS gyeongnam_growth_rate,
            jeju,
            ROUND(((jeju - LAG(jeju) OVER (ORDER BY year)) / LAG(jeju) OVER (ORDER BY year)) * 100, 2) AS jeju_growth_rate
        FROM 
            sido s;
    """,
    "차종 별 등록 대 수": """
        SELECT 
            year,
            passenger,
            LAG(passenger) OVER (ORDER BY year) AS prev_passenger,
            (passenger - LAG(passenger) OVER (ORDER BY year)) AS passenger_change,
            van,
            LAG(van) OVER (ORDER BY year) AS prev_van,
            (van - LAG(van) OVER (ORDER BY year)) AS van_change,
            truck,
            LAG(truck) OVER (ORDER BY year) AS prev_truck,
            (truck - LAG(truck) OVER (ORDER BY year)) AS truck_change,
            special,
            LAG(special) OVER (ORDER BY year) AS prev_special,
            (special - LAG(special) OVER (ORDER BY year)) AS special_change
        FROM 
            chajong;
    """,
    "용도 별 자동차 등록 대 수와 증가율": """
        SELECT 
            year,
            official,
            LAG(official) OVER (ORDER BY year) AS prev_official,
            (official - LAG(official) OVER (ORDER BY year)) AS official_change,
            private,
            LAG(private) OVER (ORDER BY year) AS prev_private,
            (private - LAG(private) OVER (ORDER BY year)) AS private_change,
            commercial,
            LAG(commercial) OVER (ORDER BY year) AS prev_commercial,
            (commercial - LAG(commercial) OVER (ORDER BY year)) AS commercial_change
        FROM 
            yongdo;
    """,
    "전체 차량 연도 별 증가율": """
        SELECT 
            year,
            car_regi,
            LAG(car_regi) OVER (ORDER BY year) AS prev_car_regi,
            ROUND((car_regi - LAG(car_regi) OVER (ORDER BY year)) * 1.0 / LAG(car_regi) OVER (ORDER BY year) * 100, 2) AS growth_rate
        FROM 
            main;
    """,
    "연도 별 각 브랜드의 판매량 추세": """
        with a
        as
        (
            select sales as Hyundai, year
            from carsalestbl
            where id = 1
        ), b
        as
        (
            select sales as Kia, year
            from carsalestbl
            where id = 2
        ), c
        as
        (
            select sales as Genesis, year
            from carsalestbl
            where id = 3
        ), d
        as
        (
            select sales as Chevrolet, year
            from carsalestbl
            where id = 4
        )
        select
            a.year as Year,
            a.Hyundai,
            b.Kia,
            c.Genesis,
            d.Chevrolet
        from a
            join b on a.year = b.year
            join c on b.year = c.year
            join d on c.year = d.year
        ;
    """,
    "2022, 2023, 2024 각 브랜드의 판매량 비교": """
        with a
        as
        (
            select sales as Hyundai, year
            from carsalestbl
            where id = 1
        ), b
        as
        (
            select sales as Kia, year
            from carsalestbl
            where id = 2
        ), c
        as
        (
            select sales as Genesis, year
            from carsalestbl
            where id = 3
        ), d
        as
        (
            select sales as Chevrolet, year
            from carsalestbl
            where id = 4
        )
        select
            a.year as Year,
            a.Hyundai,
            b.Kia,
            c.Genesis,
            d.Chevrolet
        from a
            join b on a.year = b.year
            join c on b.year = c.year
            join d on c.year = d.year
        ;
    """,
    "각 브랜드의 총 판매량": """
        with a
        as
        (
            select sales as Hyundai, year
            from carsalestbl
            where id = 1
        ), b
        as
        (
            select sales as Kia, year
            from carsalestbl
            where id = 2
        ), c
        as
        (
            select sales as Genesis, year
            from carsalestbl
            where id = 3
        ), d
        as
        (
            select sales as Chevrolet, year
            from carsalestbl
            where id = 4
        )
        select
            a.year as Year,
            a.Hyundai,
            b.Kia,
            c.Genesis,
            d.Chevrolet
        from a
            join b on a.year = b.year
            join c on b.year = c.year
            join d on c.year = d.year
        ;
    """,
    "시간에 따른 브랜드별 누적 판매량": """
        with a
        as
        (
            select sales as Hyundai, year
            from carsalestbl
            where id = 1
        ), b
        as
        (
            select sales as Kia, year
            from carsalestbl
            where id = 2
        ), c
        as
        (
            select sales as Genesis, year
            from carsalestbl
            where id = 3
        ), d
        as
        (
            select sales as Chevrolet, year
            from carsalestbl
            where id = 4
        )
        select
            a.year as Year,
            a.Hyundai,
            b.Kia,
            c.Genesis,
            d.Chevrolet
        from a
            join b on a.year = b.year
            join c on b.year = c.year
            join d on c.year = d.year
        ;
    """
}