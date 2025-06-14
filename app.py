
import streamlit as st
import pandas as pd

# 사례 데이터
data = [{
    "사례번호": 80,
    "제목": "쌍방 도화, 바람둥이(옹녀)",
    "사주원국": "癸癸丁癸 / 亥丑巳卯",
    "해석순서": "癸卯년 丁巳월 癸丑일 癸亥시",
    "격국": "食神生財格",
    "제압수단": "金水勢가 木火勢를 제압",
    "공망": "寅卯, 辰巳",
    "직업": "陰木(卯)이 火(巳)를 生하니 의류업 종사. 食神生財格에 火가 財 → 의류 판매업.",
    "육친해석": "夫宮: 丑 / 夫星: 巳火 (丑 중 합입) / 比劫: 癸水 (丑 중장) → 쌍방 외도성, 桃花 작용.",
    "운세흐름": "己未운: 혼인 운. 丑未冲 → 남녀 관계. 己巳년: 예술가 남자 친구. 癸酉년: 인성운 → 가게 운영 등..."
}]

df = pd.DataFrame(data)

st.title("📘 사주 사례 검색 MVP")

# 키워드 검색
query = st.text_input("사례 키워드 검색 (제목, 직업, 격국 등)")
filtered = df[df.apply(lambda row: query in row["제목"] or query in row["직업"] or query in row["격국"], axis=1)] if query else df

# 사례 리스트
for _, row in filtered.iterrows():
    with st.expander(f"📌 {row['사례번호']} - {row['제목']}"):
        st.markdown(f"**사주 원국:** {row['사주원국']}  
**해석 순서:** {row['해석순서']}")
        st.markdown(f"**격국:** {row['격국']} / **제압수단:** {row['제압수단']} / **공망:** {row['공망']}")
        st.markdown(f"**직업 해석:** {row['직업']}")
        st.markdown(f"**육친 해석:** {row['육친해석']}")
        st.markdown(f"**운세 흐름:** {row['운세흐름']}")
