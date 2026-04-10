import os

def analyze_resume(resume_text):
    # Demo mode (no API key)
    if os.getenv("OPENAI_API_KEY") is None:
        return """
        🔍 Demo Analysis

        ✅ Skills found:
        - Python
        - SQL
        - Excel

        ❌ Missing skills:
        - Machine Learning
        - Power BI

        📊 ATS Score: 75/100

        💡 Suggestions:
        - Add more projects
        - Use action verbs
        - Improve formatting
        """

    # Real mode (if API key exists)
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": resume_text}]
    )

    return response.choices[0].message.content