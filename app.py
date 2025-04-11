import streamlit as st
import openai
import os
import json
from datetime import datetime

openai.api_key = st.secrets["OPENAI_API_KEY"]

os.makedirs("uploads", exist_ok=True)
os.makedirs("logs", exist_ok=True)

st.set_page_config(page_title="등기사 GPT", page_icon="📄")
st.title("📄 등기사 GPT")

with st.form("chat_form"):
    user_input = st.text_area("💬 등기 관련 질문을 입력하세요", height=100)
    uploaded_file = st.file_uploader("📎 등기부등본 PDF 파일 첨부", type=["pdf"])
    submitted = st.form_submit_button("전송")

if submitted and user_input:
    file_path = None
    if uploaded_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"uploads/{timestamp}_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    with st.spinner("등기사 GPT가 답변 중입니다..."):
        messages = [{"role": "system", "content": "당신은 친절한 부동산 등기 전문가입니다. 질문에 정확히 답변해주세요."}]
        messages.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        answer = response.choices[0].message.content
        st.markdown(f"🤖 **GPT 답변:**\n\n{answer}")

    log_data = {
        "timestamp": datetime.now().isoformat(),
        "question": user_input,
        "answer": answer,
        "pdf_file": file_path if file_path else None
    }
    with open("logs/chat_logs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data, ensure_ascii=False) + "\n")
