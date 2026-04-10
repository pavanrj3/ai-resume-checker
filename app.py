import streamlit as st
from resume_reader import read_resume
from analyzer import analyze_resume

st.title("AI Resume Checker")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

if uploaded_file:
    st.write("Analyzing...")

    text = read_resume(uploaded_file)
    result = analyze_resume(text)

    st.subheader("Analysis Result")
    st.write(result)