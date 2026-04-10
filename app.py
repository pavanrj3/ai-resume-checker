import streamlit as st
from resume_reader import read_resume
from analyzer import analyze_resume
import re

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("📄 AI Resume Analyzer")
st.markdown("Upload your resume and get instant analysis 🚀")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

if uploaded_file:
    st.success("Resume uploaded successfully ✅")

    text = read_resume(uploaded_file)

    with st.spinner("Analyzing your resume... 🔍"):
        result = analyze_resume(text)

    st.divider()

    score_match = re.search(r'(\d{2,3})/100', result)
    score = int(score_match.group(1)) if score_match else 70

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 ATS Score")
        st.progress(score / 100)
        st.write(f"**{score}/100**")

    with col2:
        st.subheader("📋 Summary")
        st.write("AI-generated resume insights")

    st.divider()

    st.subheader("📄 Detailed Analysis")
    st.write(result)
