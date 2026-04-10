import streamlit as st
import requests
from resume_reader import read_resume
import re

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# 🎯 Title
st.title("📄 AI Resume Analyzer")
st.markdown("Upload your resume and get instant analysis 🚀")

# 📂 Upload file
uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

if uploaded_file:
    st.success("Resume uploaded successfully ✅")

    # 📄 Read resume
    text = read_resume(uploaded_file)

    # 🔍 Call FastAPI
    with st.spinner("Analyzing your resume... 🔍"):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                json={"resume": text}
            )

            result = response.json()["result"]

        except:
            st.error("❌ Backend not running. Please start FastAPI.")
            st.stop()

    st.divider()

    # 📊 Extract ATS score
    score_match = re.search(r'(\d{2,3})/100', result)
    score = int(score_match.group(1)) if score_match else 70

    # 📊 Layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 ATS Score")
        st.progress(score / 100)
        st.write(f"**{score}/100**")

    with col2:
        st.subheader("📋 Summary")
        st.write("AI-generated resume insights")

    st.divider()

    # 📋 Full result
    st.subheader("📄 Detailed Analysis")
    st.write(result)
