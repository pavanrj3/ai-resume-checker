from pydantic import BaseModel

class ResumeRequest(BaseModel):
    resume: str

class ResumeResponse(BaseModel):
    skills: str
    missing_skills: str
    ats_score: str
    suggestions: str