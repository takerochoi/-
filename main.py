import os
import streamlit as st
from dotenv import load_dotenv
from utils.pdf_handler import extract_text_from_pdf, extract_images_from_pdf, extract_tables_from_pdf
from utils.openai_api import summarize_text, summarize_paper, answer_question
from utils.ocr_handler import analyze_image
from utils.keyword_extraction import extract_keywords

# .envからAPIキーを読み込む
load_dotenv()

st.title("論文分析ツール - OpenAI API版")

# チャット履歴の初期化
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# PDFファイルのアップロード
uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type="pdf")

if uploaded_file:
    # テキスト抽出
    text = extract_text_from_pdf(uploaded_file)
    st.text_area("抽出されたテキスト", text[:1000], height=300)

    # 論文要約生成
    st.subheader("論文の要約機能")
    if st.button("論文全体の要約を生成"):
        paper_summary = summarize_paper(text)
        st.subheader("論文の要約結果")
        st.write(paper_summary)

    if st.button("結論セクションの要約を生成"):
        conclusion_summary = summarize_paper(text, section="結論")
        st.subheader("結論の要約")
        st.write(conclusion_summary)

    # 質問応答
    st.subheader("質問応答機能")
    question = st.text_input("質問を入力してください", key="question_input")
    if st.button("質問する"):
        answer = answer_question(question, text[:2000])
        st.session_state.chat_history.append({"質問": question, "回答": answer})
        st.subheader("回答")
        st.write(answer)

    # キーワード抽出
    st.subheader("キーワード抽出機能")
    if st.button("キーワードを抽出"):
        keywords = extract_keywords(text)
        st.subheader("抽出されたキーワード")
        st.write(", ".join(keywords))

    # 画像抽出と解析
    st.subheader("図と表の解析")
    images = extract_images_from_pdf(uploaded_file)
    if images:
        st.subheader("抽出された図")
        for img in images:
            st.image(img, caption="抽出された画像", use_column_width=True)
            text_from_image = analyze_image(img)
            st.text_area("図の内容解析", text_from_image)
    else:
        st.warning("図が見つかりませんでした。")

    # 表抽出
    tables = extract_tables_from_pdf(uploaded_file)
    if tables:
        st.subheader("抽出された表")
        for table in tables:
            st.table(table)
    else:
        st.warning("表が見つかりませんでした。")
