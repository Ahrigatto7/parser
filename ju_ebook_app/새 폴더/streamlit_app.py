import io
import re
from collections import Counter

import pandas as pd
import pdfplumber
import streamlit as st
from openai import OpenAI


def extract_text(uploaded_file) -> str:
    """Return plain text from various document types."""
    ext = uploaded_file.name.split(".")[-1].lower()
    if ext == "pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        return "\n".join(pages)
    if ext in {"xlsx", "xls"}:
        df = pd.read_excel(uploaded_file)
        return df.to_csv(index=False)
    return uploaded_file.read().decode()


def analyze_structure(text: str) -> list[str]:
    """Extract simple heading-like structures from text."""
    headings = []
    for line in text.splitlines():
        if re.match(r"^\s*(\d+\.\s+|[#\*-])", line):
            headings.append(line.strip())
    return headings


def extract_rules(text: str) -> list[tuple[str, int]]:
    """Return the most common words in the text as simple rules."""
    tokens = re.findall(r"\b\w+\b", text.lower())
    return Counter(tokens).most_common(10)


# UI Layout
st.title("📊 메인 대시보드")
st.write(
    "문서를 업로드하고 텍스트 추출, 구조 분석, 규칙 추출을 수행할 수 있습니다."
    " OpenAI API 키를 제공하면 GPT에게 질문도 할 수 있습니다."
)

openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)
    uploaded_file = st.file_uploader(
        "문서 업로드", type=("txt", "md", "pdf", "xlsx", "xls")
    )

    text, headings, rules = "", [], []
    if uploaded_file:
        text = extract_text(uploaded_file)

        tabs = st.tabs([
            "텍스트 인식",
            "구조화 분석",
            "규칙 추출",
            "규칙 저장 & 리포트",
        ])

        with tabs[0]:
            st.subheader("텍스트 인식")
            st.text_area("추출된 텍스트", text, height=300)

        with tabs[1]:
            st.subheader("구조화 분석")
            headings = analyze_structure(text)
            st.write(headings if headings else "감지된 구조가 없습니다.")

        with tabs[2]:
            st.subheader("규칙 추출")
            rules = extract_rules(text)
            st.write(rules)

        with tabs[3]:
            st.subheader("규칙 저장 & 리포트")
            report = f"Headings:\n{'\n'.join(headings)}\n\nRules:\n" + "\n".join(
                f"{word}: {count}" for word, count in rules
            )
            st.download_button(
                "보고서 다운로드", data=report, file_name="report.txt"
            )

    question = st.text_area(
        "문서에 대해 질문하세요!",
        placeholder="예) 간단히 요약해 줘",
        disabled=not text,
    )

    if text and question:
        messages = [{
            "role": "user",
            "content": f"Here's a document: {text} \n\n---\n\n {question}",
        }]
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )
        st.write_stream(stream)
