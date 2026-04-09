from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============ User Profile Schemas ============

class UserProfileCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, example="John")
    last_name: str = Field(..., min_length=1, max_length=100, example="Doe")
    email: str = Field(..., example="john.doe@email.com")
    phone: Optional[str] = Field(None, example="+1-555-0123")
    location: Optional[str] = Field(None, example="New York, USA")
    linkedin: Optional[str] = Field(None, example="https://linkedin.com/in/johndoe")
    github: Optional[str] = Field(None, example="https://github.com/johndoe")
    portfolio: Optional[str] = Field(None, example="https://johndoe.dev")
    professional_title: Optional[str] = Field(None, example="Senior Software Engineer")
    summary: Optional[str] = Field(None, example="Experienced developer...")


class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    professional_title: Optional[str] = None
    summary: Optional[str] = None


class UserProfileResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    location: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]
    portfolio: Optional[str]
    professional_title: Optional[str]
    summary: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============ Resume Schemas ============

class SkillItem(BaseModel):
    name: str = Field(..., example="Python")
    level: Optional[str] = Field(None, example="Advanced")
    category: Optional[str] = Field(None, example="Technical")


class ExperienceItem(BaseModel):
    company: str = Field(..., example="Tech Corp")
    position: str = Field(..., example="Software Engineer")
    start_date: Optional[str] = Field(None, example="Jan 2020")
    end_date: Optional[str] = Field(None, example="Present")
    location: Optional[str] = Field(None, example="New York")
    description: Optional[str] = Field(None, example="Led development of...")
    achievements: Optional[str] = Field(None, example="• Increased performance by 40%\n• Reduced bugs by 25%")


class EducationItem(BaseModel):
    institution: str = Field(..., example="MIT")
    degree: str = Field(..., example="Bachelor of Science")
    field_of_study: Optional[str] = Field(None, example="Computer Science")
    graduation_date: Optional[str] = Field(None, example="May 2019")
    gpa: Optional[str] = Field(None, example="3.8/4.0")
    honors: Optional[str] = Field(None, example="Magna Cum Laude")


class ProjectItem(BaseModel):
    name: str = Field(..., example="AI Chatbot")
    description: str = Field(..., example="Built an AI-powered chatbot...")
    technologies: List[str] = Field(default_factory=list, example=["Python", "FastAPI"])
    link: Optional[str] = Field(None, example="https://github.com/project")
    start_date: Optional[str] = Field(None, example="Jan 2023")
    end_date: Optional[str] = Field(None, example="Present")


class ResumeGenerateRequest(BaseModel):
    """Request to generate a polished resume."""
    user_id: int = Field(..., example=1)
    title: Optional[str] = Field(None, example="Software Engineer Resume")
    summary: Optional[str] = Field(None, example="My professional summary...")
    skills: List[SkillItem] = Field(default_factory=list)
    experience: List[ExperienceItem] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    job_description: Optional[str] = Field(None, description="Optional job description to optimize against")


class ResumeGenerateResponse(BaseModel):
    resume_id: int
    pdf_url: str
    message: str


class ResumeHistoryResponse(BaseModel):
    id: int
    user_id: int
    title: Optional[str]
    summary: Optional[str]
    skills_json: Optional[list]
    experience_json: Optional[list]
    education_json: Optional[list]
    projects_json: Optional[list]
    pdf_filename: Optional[str]
    pdf_url: Optional[str]
    job_description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Optimization Schemas ============

class OptimizeRequest(BaseModel):
    user_id: int = Field(..., example=1)
    job_description: str = Field(..., min_length=50, example="We are looking for a senior Python developer...")
    current_resume: Optional[str] = Field(None, description="Current resume text")


class OptimizeResponse(BaseModel):
    resume_id: int
    optimized_summary: str
    optimized_skills: List[SkillItem]
    optimized_experience: List[ExperienceItem]
    optimized_education: List[EducationItem]
    pdf_url: str
    keyword_match_score: float = Field(..., example=85.5)


# ============ Interview Schemas ============

class InterviewStartRequest(BaseModel):
    user_id: int = Field(..., example=1)
    role: str = Field(..., example="Senior Backend Developer")
    experience_level: str = Field(..., example="Senior")
    focus_areas: Optional[List[str]] = Field(None, example=["System Design", "Python", "Databases"])


class InterviewStartResponse(BaseModel):
    session_id: str
    first_question: str


class InterviewAnswerRequest(BaseModel):
    session_id: str = Field(..., example="abc-123")
    answer: str = Field(..., min_length=10, example="I would approach this by...")


class InterviewAnswerResponse(BaseModel):
    feedback: str
    score: int = Field(..., ge=0, le=10, example=7)
    next_question: Optional[str] = None
    is_complete: bool


class InterviewSession(BaseModel):
    session_id: str
    user_id: int
    role: str
    question_number: int
    total_questions: int = 10
    is_complete: bool = False
