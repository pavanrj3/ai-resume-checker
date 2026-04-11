import streamlit as st
import time
from resume_reader import read_resume
from analyzer import analyze_resume

st.title("AI Resume Checker")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

if uploaded_file:
    # File Info Display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("File Name", uploaded_file.name[:20] + "...")
    with col2:
        st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
    with col3:
        st.metric("Format", "PDF")
    
    st.divider()
    st.subheader("Step 2: AI Analysis")
    
    # Analysis with progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Reading resume
        status_text.text("📖 Reading resume...")
        progress_bar.progress(20)
        time.sleep(0.3)
        
        text = read_resume(uploaded_file)
        
        # AI Analysis (NO API - direct function)
        status_text.text("🤖 AI is analyzing your resume...")
        progress_bar.progress(50)
        time.sleep(0.3)
        
        result = analyze_resume(text)
        
        progress_bar.progress(75)
        status_text.text("✅ Processing results...")
        time.sleep(0.3)
        
        progress_bar.progress(100)
        status_text.text("✓ Analysis complete!")
        
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
        
        st.success("✅ Analysis completed successfully!")
        st.divider()
        
        # Display Results
        st.subheader("Step 3: Analysis Results")
        
        # Parse result
        lines = result.split('\n')
        
        sections = {
            'Skills': [],
            'Missing Skills': [],
            'ATS Score': '',
            'Suggestions': []
        }
        
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('Skills'):
                current_section = 'Skills'
            elif line.startswith('Missing'):
                current_section = 'Missing Skills'
            elif line.startswith('ATS'):
                current_section = 'ATS Score'
                sections['ATS Score'] = line.split(':')[-1].strip()
            elif line.startswith('Suggestions'):
                current_section = 'Suggestions'
            elif current_section and current_section != 'ATS Score':
                sections[current_section].append(line)
        
        # ATS Score UI
        if sections['ATS Score']:
            try:
                score = float(sections['ATS Score'].replace('%', '').strip())
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #2DCA96, #667eea); 
                                    color: white; padding: 2rem; border-radius: 10px; text-align: center;'>
                            <h3>ATS Compatibility Score</h3>
                            <h1>{score:.0f}%</h1>
                        </div>
                    """, unsafe_allow_html=True)
            except:
                st.info(f"ATS Score: {sections['ATS Score']}")
        
        st.divider()
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(
            ["💼 Skills", "⚠️ Missing", "💡 Suggestions", "📊 Full Report"]
        )
        
        with tab1:
            st.write("### Skills Found")
            for skill in sections['Skills']:
                st.success(f"✓ {skill}")
        
        with tab2:
            st.write("### Missing Skills")
            for skill in sections['Missing Skills']:
                st.warning(f"+ {skill}")
        
        with tab3:
            st.write("### Suggestions")
            for sug in sections['Suggestions']:
                st.info(sug)
        
        with tab4:
            st.text_area("Full Report", value=result, height=300)
        
        st.divider()
        
        st.subheader("🎯 Next Steps")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("✏️ Update Skills")
        with col2:
            st.warning("🔍 Improve Format")
        with col3:
            st.success("📤 Re-upload Resume")

    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ Error: {str(e)}")

else:
    st.info("👆 Upload a PDF resume to start")
