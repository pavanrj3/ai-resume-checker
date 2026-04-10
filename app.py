import streamlit as st
from analyzer import analyze_resume
from resume_reader import read_resume
import re

st.set_page_config(page_title="AI Resume Checker", layout="wide")

# 🎨 Custom CSS (Fixed Colors)
st.markdown("""
<style>

/* Background Gradient */
.stApp {
    background: linear-gradient(135deg, #F0FAF7, #F3E8FF);
    color: #000000;
}

/* Force all text to black */
h1, h2, h3, h4, h5, h6, p, span, div, label {
    color: #000000 !important;
}

/* Navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    padding: 15px 40px;
    position: sticky;
    top: 0;
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(10px);
    border-radius: 12px;
}

.nav-links a {
    margin: 0 15px;
    text-decoration: none;
    color: #000 !important;
    font-weight: 500;
}

.nav-links a:hover {
    color: #2DCA96 !important;
}

/* CTA Button */
.cta-btn {
    background-color: #2DCA96;
    color: white !important;
    padding: 10px 20px;
    border-radius: 25px;
    font-weight: bold;
}

/* Hero Section */
.hero-text h1 {
    font-size: 48px;
    font-weight: 700;
    color: #000;
}

.hero-text p {
    color: #333;
    font-size: 18px;
}

/* Dropzone */
.dropzone {
    border: 2px dashed #2DCA96;
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    margin-top: 20px;
}

/* Right Mock UI */
.mockup {
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(10px);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
    color: #000;
}

</style>
""", unsafe_allow_html=True)

# 🔝 Navbar
st.markdown("""
<div class="navbar">
    <div><b>AI Resume Checker</b></div>
    <div class="nav-links">
        <a href="#">Resume</a>
        <a href="#">Cover Letter</a>
        <a href="#">Blog</a>
        <a href="#">For Organizations</a>
    </div>
    <div class="cta-btn">My Documents</div>
</div>
""", unsafe_allow_html=True)

# 🎯 Hero Section
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 🟣 RESUME CHECKER")
    st.markdown("# Improve Your Resume with AI 🚀")
    st.markdown("Get instant feedback, ATS score, and suggestions to land your dream job.")

    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

    if uploaded_file:
        text = read_resume(uploaded_file)

        with st.spinner("Analyzing..."):
            result = analyze_resume(text)

        score_match = re.search(r'(\d{2,3})/100', result)
        score = int(score_match.group(1)) if score_match else 70

        st.success("Analysis Complete ✅")
        st.progress(score / 100)
        st.write(f"### ATS Score: {score}/100")

        st.write(result)

with col2:
    st.markdown("""
    <div class="mockup">
        <h3>📊 Resume Score</h3>
        <p><b>78/100</b></p>
        <ul>
            <li>✔ Strong technical skills</li>
            <li>✔ Good formatting</li>
            <li>❌ Add more projects</li>
            <li>❌ Improve keywords</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
