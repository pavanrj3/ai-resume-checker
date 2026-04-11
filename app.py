import streamlit as st
import requests
import time
from resume_reader import read_resume

st.title("AI Resume Checker")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

if uploaded_file:
    # File Info Display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("File Name", uploaded_file.name.split('/')[-1][:20] + "...")
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
        
        # Sending to API
        status_text.text("🤖 AI is analyzing your resume...")
        progress_bar.progress(50)
        time.sleep(0.3)
        
        response = requests.post(
            "http://127.0.0.1:8000/analyze",
            json={"resume": text},
            timeout=30
        )
        
        if response.status_code == 200:
            progress_bar.progress(75)
            status_text.text("✅ Processing results...")
            time.sleep(0.3)
            
            result = response.json()["result"]
            progress_bar.progress(100)
            status_text.text("✓ Analysis complete!")
            
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()
            
            st.success("✅ Analysis completed successfully!")
            st.divider()
            
            # Display Results
            st.subheader("Step 3: Analysis Results")
            
            # Parse the result (assuming format from ai_services.py)
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
                
                if line.startswith('Skills:'):
                    current_section = 'Skills'
                    content = line.replace('Skills:', '').strip()
                    if content:
                        sections['Skills'].append(content)
                elif line.startswith('Missing Skills:'):
                    current_section = 'Missing Skills'
                    content = line.replace('Missing Skills:', '').strip()
                    if content:
                        sections['Missing Skills'].append(content)
                elif line.startswith('ATS Score:'):
                    current_section = 'ATS Score'
                    sections['ATS Score'] = line.replace('ATS Score:', '').strip()
                elif line.startswith('Suggestions:'):
                    current_section = 'Suggestions'
                    content = line.replace('Suggestions:', '').strip()
                    if content:
                        sections['Suggestions'].append(content)
                elif current_section and current_section != 'ATS Score':
                    if current_section in ['Skills', 'Missing Skills']:
                        sections[current_section].append(line)
                    elif current_section == 'Suggestions':
                        sections['Suggestions'].append(line)
            
            # Display ATS Score prominently
            if sections['ATS Score']:
                try:
                    score = float(sections['ATS Score'].replace('%', '').strip()) if '%' in sections['ATS Score'] else float(sections['ATS Score'])
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                        color: white; padding: 2rem; border-radius: 10px; text-align: center;
                                        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);'>
                                <h3 style='margin: 0; font-size: 1rem;'>ATS Compatibility Score</h3>
                                <h1 style='margin: 0.5rem 0 0 0; font-size: 3rem;'>{score:.0f}%</h1>
                                <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
                                {'✓ Excellent - Well optimized for ATS' if score >= 80 else '△ Good - Some improvements needed' if score >= 60 else '✗ Needs improvement'}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                except:
                    st.info(f"**ATS Score:** {sections['ATS Score']}")
            
            st.divider()
            
            # Create tabs for organized display
            tab1, tab2, tab3, tab4 = st.tabs(
                ["💼 Skills Identified", "⚠️ Missing Skills", "💡 Suggestions", "📊 Full Report"]
            )
            
            with tab1:
                if sections['Skills']:
                    st.write("### Identified Technical & Soft Skills")
                    skill_text = " ".join(sections['Skills'])
                    skills = [s.strip('- •*') for s in skill_text.split(',') if s.strip()]
                    if skills:
                        cols = st.columns(3)
                        for idx, skill in enumerate(skills[:9]):
                            with cols[idx % 3]:
                                st.markdown(f"""
                                    <div class='skill-badge'>✓ {skill}</div>
                                """, unsafe_allow_html=True)
                    else:
                        st.write(skill_text)
                else:
                    st.info("No specific skills parsed.")
            
            with tab2:
                if sections['Missing Skills']:
                    st.write("### Skills to Develop")
                    missing_text = " ".join(sections['Missing Skills'])
                    missing = [s.strip('- •*') for s in missing_text.split(',') if s.strip()]
                    if missing:
                        cols = st.columns(3)
                        for idx, skill in enumerate(missing[:9]):
                            with cols[idx % 3]:
                                st.markdown(f"""
                                    <div class='missing-badge'>+ {skill}</div>
                                """, unsafe_allow_html=True)
                    else:
                        st.write(missing_text)
                else:
                    st.info("No missing skills identified.")
            
            with tab3:
                if sections['Suggestions']:
                    st.write("### Recommendations")
                    for idx, suggestion in enumerate(sections['Suggestions'][:10], 1):
                        suggestion_clean = suggestion.strip('- •*')
                        if suggestion_clean:
                            st.markdown(f"""
                                <div class='suggestion-box'>
                                <b>#{idx}</b> {suggestion_clean}
                                </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("No suggestions available.")
            
            with tab4:
                st.write("### Complete Analysis")
                st.text_area("Full AI Analysis Output", value=result, height=300, disabled=True)
            
            st.divider()
            
            # Action Items
            st.subheader("🎯 Next Steps")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("✏️ **Update Skills**\nAdd identified gaps to your resume")
            with col2:
                st.warning("🔍 **Optimize Format**\nEnsure ATS compatibility")
            with col3:
                st.success("📤 **Re-upload**\nVerify improvements")
        
        else:
            st.error(f"❌ API Error: {response.status_code}")
            st.write("Please ensure the backend API is running on http://127.0.0.1:8000")
    
    except requests.exceptions.ConnectionError:
        progress_bar.empty()
        status_text.empty()
        st.error("❌ Connection Error")
        st.write("Cannot connect to the API server. Please ensure it's running on http://127.0.0.1:8000")
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ Error: {str(e)}")
        st.write("An unexpected error occurred. Please check the logs.")

else:
    st.info("👆 Please upload a PDF resume to get started!")
