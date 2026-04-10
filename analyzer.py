import os

def analyze_resume(resume_text):

    text = resume_text.lower()

    # 🔍 Detect domain
    if any(word in text for word in ["python", "sql", "excel", "data", "analysis"]):
        domain = "Data Analyst"
        required_skills = ["python", "sql", "excel", "power bi", "statistics"]

    elif any(word in text for word in ["java", "c++", "developer", "spring", "api"]):
        domain = "Software Developer"
        required_skills = ["java", "c++", "api", "data structures", "git"]

    elif any(word in text for word in ["html", "css", "javascript", "react", "frontend"]):
        domain = "Web Developer"
        required_skills = ["html", "css", "javascript", "react", "node.js"]

    elif any(word in text for word in ["aws", "docker", "kubernetes", "devops"]):
        domain = "DevOps Engineer"
        required_skills = ["aws", "docker", "kubernetes", "ci/cd", "linux"]

    elif any(word in text for word in ["machine learning", "ai", "deep learning"]):
        domain = "AI/ML Engineer"
        required_skills = ["python", "machine learning", "tensorflow", "pytorch", "data"]

    else:
        domain = "General"
        required_skills = ["communication", "teamwork", "problem solving"]

    # ✅ Extract skills found
    found_skills = [skill for skill in required_skills if skill in text]

    # ❌ Missing skills
    missing_skills = [skill for skill in required_skills if skill not in text]

    # 📊 ATS Score
    score = int((len(found_skills) / len(required_skills)) * 100)

    # 💡 Suggestions
    suggestions = []
    if missing_skills:
        suggestions.append("Add missing skills relevant to your domain")
    if "project" not in text:
        suggestions.append("Include project experience")
    if "experience" not in text:
        suggestions.append("Add work experience details")
    if "achievement" not in text:
        suggestions.append("Mention measurable achievements")

    # 🧪 Demo Mode (no API key)
    if os.getenv("OPENAI_API_KEY") is None:
        return f"""
        🔍 Domain Detected: {domain}

        ✅ Skills found:
        {", ".join(found_skills) if found_skills else "No major skills detected"}

        ❌ Missing skills:
        {", ".join(missing_skills)}

        📊 ATS Score: {score}/100

        💡 Suggestions:
        {"; ".join(suggestions)}
        """

    # 🔥 Real AI Mode
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
    Analyze this resume for the role of {domain}:

    {resume_text}

    Give:
    1. Skills found
    2. Missing skills
    3. ATS score out of 100
    4. Improvement suggestions
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
